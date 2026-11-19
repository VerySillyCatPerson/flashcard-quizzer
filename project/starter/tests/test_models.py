"""Tests for immutable card values and portable, unambiguous content identity."""

import re
from dataclasses import FrozenInstanceError

import pytest

from utils.models import Flashcard, normalize_text


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (" \tDEF\n", "def"),
        ("Stra\u00dfe", "strasse"),
        ("  two  words  ", "two  words"),
        ("\u2003\t", ""),
    ],
)
def test_normalization_preserves_internal_spacing(value: str, expected: str) -> None:
    """Normalization trims and casefolds, including non-ASCII whitespace/casing."""
    assert normalize_text(value) == expected


def test_card_is_immutable() -> None:
    """A card's answer cannot change in place after identity/validation."""
    card = Flashcard("API", "Application Programming Interface")
    with pytest.raises(FrozenInstanceError):
        setattr(card, "back", "changed")
    assert card.back == "Application Programming Interface"


def test_card_identity_normalizes_both_fields() -> None:
    """Whitespace/casing variants share content identity across decks."""
    first = Flashcard(" Stra\u00dfe ", " ANSWER ")
    second = Flashcard("STRASSE", "answer")
    assert first.normalized_pair == ("strasse", "answer")
    assert first.card_id == second.card_id
    assert re.fullmatch(r"card-v1:[0-9a-f]{64}", first.card_id)


@pytest.mark.parametrize(
    "other",
    [Flashcard("different", "answer"), Flashcard("question", "different")],
)
def test_meaningful_content_edits_change_identity(other: Flashcard) -> None:
    """Editing either side creates fresh learning identity."""
    assert Flashcard("question", "answer").card_id != other.card_id


def test_identity_preserves_field_boundaries_and_internal_whitespace() -> None:
    """Concatenation lookalikes and internal-space edits remain distinct cards."""
    assert Flashcard("ab", "c").card_id != Flashcard("a", "bc").card_id
    assert Flashcard("a b", "c").card_id != Flashcard("a  b", "c").card_id


def test_identity_ignores_case_and_outer_whitespace_but_keeps_punctuation() -> None:
    """Punctuation survives normalization in both sides of an identity key."""
    first = Flashcard("  What's API?\t", " A-B, C!\n")
    second = Flashcard("WHAT'S API?", "a-b, c!")
    assert first.normalized_pair == ("what's api?", "a-b, c!")
    assert first.card_id == second.card_id


@pytest.mark.parametrize("field", ["front", "back"])
@pytest.mark.parametrize(
    ("original", "edited"),
    [("two words", "two  words"), ("answer!", "answer"), ('"quoted"', "quoted")],
)
def test_identity_distinguishes_internal_space_and_punctuation_edits(
    field: str, original: str, edited: str
) -> None:
    """Neither field silently loses punctuation or internal space differences."""
    first = Flashcard(
        original if field == "front" else "front",
        original if field == "back" else "back",
    )
    second = Flashcard(
        edited if field == "front" else "front",
        edited if field == "back" else "back",
    )
    assert first.card_id != second.card_id
