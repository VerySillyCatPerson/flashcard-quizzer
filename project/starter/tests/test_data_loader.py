"""File, schema, normalization, and duplicate validation for both deck formats."""

import json
from pathlib import Path

import pytest

from utils.data_loader import FlashcardLoadError, load_flashcards
from utils.models import Flashcard


def _write_deck(tmp_path: Path, value: object) -> Path:
    """Serialize a test deck into a real temporary UTF-8 file."""
    path = tmp_path / "deck.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


@pytest.mark.parametrize("wrapped", [False, True])
def test_loads_both_shapes_in_source_order(tmp_path: Path, wrapped: bool) -> None:
    """The wrapper and bare-array contracts produce the same typed cards."""
    entries = [
        {"front": "  API\t", "back": " Application Programming Interface\n"},
        {"front": "CPU", "back": "Central  Processing Unit"},
    ]
    value: object = {"cards": entries} if wrapped else entries
    path = _write_deck(tmp_path, value)
    before = path.read_bytes()
    assert load_flashcards(str(path)) == [
        Flashcard("API", "Application Programming Interface"),
        Flashcard("CPU", "Central  Processing Unit"),
    ]
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    ("filename", "count", "first", "last"),
    [
        ("glossary.json", 10, "API", "VPN"),
        (
            "python_basics.json",
            8,
            "Which keyword defines a function?",
            "Which keyword imports a module?",
        ),
    ],
)
def test_existing_sample_decks(
    filename: str, count: int, first: str, last: str
) -> None:
    """Preserve compatibility with the actual, unmodified starter samples."""
    path = Path(__file__).resolve().parents[1] / "data" / filename
    before = path.read_bytes()
    cards = load_flashcards(path)
    assert len(cards) == count
    assert cards[0].front == first
    assert cards[-1].front == last
    assert path.read_bytes() == before


def test_unicode_and_utf8_bom(tmp_path: Path) -> None:
    """A UTF-8 BOM and literal non-ASCII text are accepted without case loss."""
    path = tmp_path / "unicode.json"
    path.write_text(
        '[{"front":"\u2003\u6708 ","back":"Stra\u00dfe"}]', encoding="utf-8-sig"
    )
    assert load_flashcards(path) == [Flashcard("\u6708", "Stra\u00dfe")]


def test_matching_fronts_with_different_backs_are_valid(tmp_path: Path) -> None:
    """Repeated questions do not merge their distinct expected answers."""
    path = _write_deck(
        tmp_path,
        [
            {"front": "bank", "back": "financial institution"},
            {"front": " BANK ", "back": "river edge"},
        ],
    )
    cards = load_flashcards(path)
    assert cards == [
        Flashcard("bank", "financial institution"),
        Flashcard("BANK", "river edge"),
    ]
    assert cards[0].card_id != cards[1].card_id


def test_metadata_is_ignored(tmp_path: Path) -> None:
    """Unrecognized card/wrapper metadata does not extend the model contract."""
    path = _write_deck(
        tmp_path,
        {"title": "Deck", "cards": [{"front": "A", "back": "B", "tag": [1]}]},
    )
    assert load_flashcards(path) == [Flashcard("A", "B")]


def test_identity_survives_rename_reorder_and_additions(tmp_path: Path) -> None:
    """Unchanged content retains identity independently of its deck location."""
    path = _write_deck(
        tmp_path, [{"front": "A", "back": "B"}, {"front": "C", "back": "D"}]
    )
    before = load_flashcards(path)
    renamed = path.rename(tmp_path / "renamed.json")
    assert load_flashcards(renamed)[0].card_id == before[0].card_id
    added = _write_deck(
        tmp_path,
        {
            "cards": [
                {"front": "C", "back": "D"},
                {"front": "A", "back": "B"},
                {"front": "E", "back": "F"},
            ]
        },
    )
    after = load_flashcards(added)
    assert after[0].card_id == before[1].card_id
    assert after[1].card_id == before[0].card_id
    assert after[2].card_id not in {card.card_id for card in before}


def test_missing_file(tmp_path: Path) -> None:
    """A missing file becomes a structured loader exception."""
    path = tmp_path / "missing.json"
    with pytest.raises(FlashcardLoadError, match="File does not exist") as captured:
        load_flashcards(path)
    assert captured.value.path == path
    assert isinstance(captured.value.__cause__, FileNotFoundError)
    assert str(path) in str(captured.value)


@pytest.mark.parametrize(
    ("failure", "message"),
    [
        (PermissionError("denied"), "Permission denied"),
        (OSError("device unavailable"), "Could not read file: device unavailable"),
    ],
)
def test_unreadable_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: OSError,
    message: str,
) -> None:
    """Deterministically simulate OS errors, including elevated Windows runs."""
    path = _write_deck(tmp_path, [{"front": "A", "back": "B"}])

    def fail_read(
        self: Path, encoding: str | None = None, errors: str | None = None
    ) -> str:
        """Fail at the filesystem boundary rather than relying on chmod."""
        raise failure

    monkeypatch.setattr(Path, "read_text", fail_read)
    with pytest.raises(FlashcardLoadError, match=message) as captured:
        load_flashcards(path)
    assert captured.value.path == path
    assert captured.value.__cause__ is failure


def test_directory_is_not_a_deck(tmp_path: Path) -> None:
    """A real directory read error is translated without platform assumptions."""
    with pytest.raises(FlashcardLoadError) as captured:
        load_flashcards(tmp_path)
    assert isinstance(captured.value.__cause__, OSError)


def test_invalid_utf8(tmp_path: Path) -> None:
    """Invalid source bytes report an encoding failure, not a raw decode error."""
    path = tmp_path / "bad-encoding.json"
    path.write_bytes(b"\xff\xfeinvalid")
    with pytest.raises(FlashcardLoadError, match="UTF-8") as captured:
        load_flashcards(path)
    assert isinstance(captured.value.__cause__, UnicodeDecodeError)


@pytest.mark.parametrize("text", ["", "   ", "not json", '[\n{"front": "A",}\n]'])
def test_malformed_json(tmp_path: Path, text: str) -> None:
    """Malformed and empty files include actionable line/column information."""
    path = tmp_path / "malformed.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(
        FlashcardLoadError, match=r"Invalid JSON at line \d+, column \d+"
    ) as captured:
        load_flashcards(path)
    assert isinstance(captured.value.__cause__, json.JSONDecodeError)


@pytest.mark.parametrize(
    "value",
    [
        None,
        True,
        42,
        1.5,
        "text",
        {},
        {"wrong": []},
        {"cards": None},
        {"cards": {}},
        {"cards": "text"},
    ],
)
def test_invalid_top_level_structures(tmp_path: Path, value: object) -> None:
    """Only arrays and objects with an array-valued cards key are accepted."""
    path = _write_deck(tmp_path, value)
    with pytest.raises(FlashcardLoadError, match="array"):
        load_flashcards(path)


@pytest.mark.parametrize("value", [[], {"cards": []}])
def test_empty_decks(tmp_path: Path, value: object) -> None:
    """Both supported formats require at least one card."""
    path = _write_deck(tmp_path, value)
    with pytest.raises(FlashcardLoadError, match="at least one card"):
        load_flashcards(path)


@pytest.mark.parametrize("value", [None, True, 42, 1.5, "text", ["A", "B"]])
def test_cards_must_be_objects(tmp_path: Path, value: object) -> None:
    """Card positions are one-based, even after a valid preceding card."""
    path = _write_deck(tmp_path, [{"front": "A", "back": "B"}, value])
    with pytest.raises(FlashcardLoadError, match="Card 2 must be a JSON object"):
        load_flashcards(path)


@pytest.mark.parametrize("field", ["front", "back"])
def test_missing_required_fields(tmp_path: Path, field: str) -> None:
    """A missing field is named together with its card position."""
    entry = {"front": "A", "back": "B"}
    del entry[field]
    path = _write_deck(tmp_path, [entry])
    with pytest.raises(
        FlashcardLoadError, match=f"Card 1: missing required field '{field}'"
    ):
        load_flashcards(path)


@pytest.mark.parametrize("field", ["front", "back"])
@pytest.mark.parametrize("value", [None, True, 42, 1.5, [], {}])
def test_wrong_field_types(tmp_path: Path, field: str, value: object) -> None:
    """Untrusted JSON is not coerced to strings by annotations or the loader."""
    entry: dict[str, object] = {"front": "A", "back": "B"}
    entry[field] = value
    path = _write_deck(tmp_path, [entry])
    with pytest.raises(
        FlashcardLoadError, match=f"Card 1: '{field}' must be a non-empty string"
    ):
        load_flashcards(path)


@pytest.mark.parametrize("field", ["front", "back"])
@pytest.mark.parametrize("value", ["", " ", "\t\n", "\u2003"])
def test_blank_field_values(tmp_path: Path, field: str, value: str) -> None:
    """Whitespace-only fields are rejected before card construction."""
    entry = {"front": "A", "back": "B"}
    entry[field] = value
    path = _write_deck(tmp_path, [entry])
    with pytest.raises(
        FlashcardLoadError, match=f"'{field}' must be a non-empty string"
    ):
        load_flashcards(path)


@pytest.mark.parametrize(
    ("front", "back"), [("A", "B"), (" a ", " b\t"), ("STRASSE", "B")]
)
def test_duplicate_pairs_report_both_positions(
    tmp_path: Path, front: str, back: str
) -> None:
    """Identical normalized pairs are rejected rather than silently removed."""
    original = "Stra\u00dfe" if front == "STRASSE" else "A"
    path = _write_deck(
        tmp_path,
        [
            {"front": original, "back": "B", "tag": "first"},
            {"front": "other", "back": "different"},
            {"front": front, "back": back, "tag": "different metadata"},
        ],
    )
    with pytest.raises(FlashcardLoadError, match=r"Cards 1 and 3.*normalized"):
        load_flashcards(path)


@pytest.mark.parametrize(
    "text",
    [
        '[{"front":"A","front":"C","back":"B"}]',
        '{"cards":[],"cards":[{"front":"A","back":"B"}]}',
        '[{"front":"A","back":"B","tag":{"x":1,"x":2}}]',
    ],
)
def test_duplicate_json_object_keys(tmp_path: Path, text: str) -> None:
    """Duplicate object keys are distinct from the allowed repeated fronts."""
    path = tmp_path / "duplicate-key.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(FlashcardLoadError, match="Duplicate JSON object key"):
        load_flashcards(path)


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_nonstandard_json_constants(tmp_path: Path, constant: str) -> None:
    """The stdlib's optional nonfinite-number extensions are not accepted JSON."""
    path = tmp_path / "nonfinite.json"
    path.write_text(f'{{"cards":[],"metadata":{constant}}}', encoding="utf-8")
    with pytest.raises(FlashcardLoadError, match="Invalid JSON constant"):
        load_flashcards(path)


def test_excessive_json_nesting(tmp_path: Path) -> None:
    """A decoder recursion limit becomes an expected loader error."""
    path = tmp_path / "nested.json"
    path.write_text("[" * 5000 + "0" + "]" * 5000, encoding="utf-8")
    with pytest.raises(FlashcardLoadError, match="JSON nesting is too deep"):
        load_flashcards(path)


def test_oversized_integer_field_is_a_loader_error(tmp_path: Path) -> None:
    """Decoder digit limits must not leak ValueError for an invalid back field."""
    path = tmp_path / "large-number.json"
    path.write_text('[{"front":"A","back":' + "9" * 10000 + "}]", encoding="utf-8")
    with pytest.raises(FlashcardLoadError) as captured:
        load_flashcards(path)
    assert captured.value.path == path
    assert captured.value.detail


@pytest.mark.parametrize("failure", [ValueError("validation bug"), RuntimeError("bug")])
def test_unexpected_validation_errors_are_not_disguised(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: Exception
) -> None:
    """Decoder handling must not relabel unexpected card-validation failures."""
    path = _write_deck(tmp_path, [{"front": "A", "back": "B"}])

    def broken_validation(value: object) -> list[Flashcard]:
        """Simulate an unexpected programming error after JSON decoding."""
        raise failure

    monkeypatch.setattr("utils.data_loader._parse_deck", broken_validation)
    with pytest.raises(type(failure)) as captured:
        load_flashcards(path)
    assert captured.value is failure


@pytest.mark.parametrize("valid", [False, True])
def test_loader_never_prints(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], valid: bool
) -> None:
    """A terminal adapter can choose presentation without loader side effects."""
    path = _write_deck(tmp_path, [{"front": "A", "back": "B"}] if valid else [])
    if valid:
        load_flashcards(path)
    else:
        with pytest.raises(FlashcardLoadError):
            load_flashcards(path)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
