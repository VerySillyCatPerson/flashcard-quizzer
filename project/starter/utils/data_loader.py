"""Load and validate JSON decks without terminal output or process exits."""

import json
from pathlib import Path
from typing import NoReturn

from utils.models import Flashcard


class FlashcardLoadError(Exception):
    """An expected deck-loading failure, with path and presentation-free detail."""

    def __init__(self, path: Path, detail: str) -> None:
        """Retain structured error information for callers such as the later CLI."""
        self.path = path
        self.detail = detail
        super().__init__(f"Cannot load flashcards from '{path}': {detail}")


class _DeckFormatError(ValueError):
    """Internal JSON/validation failure, wrapped with the path by the loader."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject repeated JSON object keys rather than silently keeping the last."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DeckFormatError(f"Duplicate JSON object key {key!r}.")
        result[key] = value
    return result


def _reject_constant(value: str) -> NoReturn:
    """Reject NaN/Infinity extensions, which are not valid JSON numbers."""
    raise _DeckFormatError(f"Invalid JSON constant {value!r}.")


def _card_text(value: object, field: str, position: int) -> str:
    """Validate and trim one card field while retaining its display casing."""
    if not isinstance(value, str) or not value.strip():
        raise _DeckFormatError(
            f"Card {position}: '{field}' must be a non-empty string."
        )
    return value.strip()


def _parse_card(value: object, position: int) -> Flashcard:
    """Narrow unknown JSON values into a validated front/back record."""
    if not isinstance(value, dict):
        raise _DeckFormatError(f"Card {position} must be a JSON object.")
    for field in ("front", "back"):
        if field not in value:
            raise _DeckFormatError(
                f"Card {position}: missing required field '{field}'."
            )
    return Flashcard(
        front=_card_text(value["front"], "front", position),
        back=_card_text(value["back"], "back", position),
    )


def _parse_deck(value: object) -> list[Flashcard]:
    """Accept both starter shapes and reject identical normalized card pairs."""
    raw_cards: object = value
    if isinstance(value, dict):
        if "cards" not in value:
            raise _DeckFormatError("Deck object must contain a 'cards' array.")
        raw_cards = value["cards"]
    if not isinstance(raw_cards, list):
        raise _DeckFormatError(
            "Expected a JSON array or an object containing a 'cards' array."
        )
    if not raw_cards:
        raise _DeckFormatError("Deck must contain at least one card.")

    cards: list[Flashcard] = []
    seen: dict[tuple[str, str], int] = {}
    for position, raw_card in enumerate(raw_cards, start=1):
        card = _parse_card(raw_card, position)
        pair = card.normalized_pair
        if pair in seen:
            raise _DeckFormatError(
                f"Cards {seen[pair]} and {position} have identical normalized "
                "(front, back) content."
            )
        seen[pair] = position
        cards.append(card)
    return cards


def load_flashcards(path: str | Path) -> list[Flashcard]:
    """Load a nonempty UTF-8 deck, optionally prefixed by a UTF-8 BOM.

    Accept either a card array or an object containing a ``cards`` array.
    Extra metadata is ignored. Return cards in source order without changing
    the file. Raise FlashcardLoadError for expected I/O, encoding, JSON, or
    validation failures; this function never prints or exits the process.
    """
    source = Path(path)
    try:
        text = source.read_text(encoding="utf-8-sig")
    except FileNotFoundError as error:
        raise FlashcardLoadError(source, "File does not exist.") from error
    except PermissionError as error:
        raise FlashcardLoadError(source, "Permission denied reading file.") from error
    except UnicodeDecodeError as error:
        raise FlashcardLoadError(source, "File must use UTF-8 encoding.") from error
    except OSError as error:
        detail = error.strerror or str(error)
        raise FlashcardLoadError(source, f"Could not read file: {detail}") from error

    try:
        payload: object = json.loads(
            text, object_pairs_hook=_unique_object, parse_constant=_reject_constant
        )
    except json.JSONDecodeError as error:
        detail = (
            f"Invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}"
        )
        raise FlashcardLoadError(source, detail) from error
    except _DeckFormatError as error:
        raise FlashcardLoadError(source, str(error)) from error
    except ValueError as error:
        raise FlashcardLoadError(source, f"Invalid JSON value: {error}") from error
    except RecursionError as error:
        raise FlashcardLoadError(source, "JSON nesting is too deep.") from error

    try:
        return _parse_deck(payload)
    except _DeckFormatError as error:
        raise FlashcardLoadError(source, str(error)) from error
