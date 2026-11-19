"""Permutation, copying, and controlled-randomness contracts for quiz ordering."""

import random
from collections import Counter
from random import Random

import pytest

from utils.models import Flashcard
from utils.strategies import AdaptiveStrategy, RandomStrategy, SequentialStrategy


@pytest.mark.parametrize("size", [0, 1, 3])
def test_sequential_returns_a_copy_in_deck_order(
    cards: list[Flashcard], size: int
) -> None:
    """Sequential selection preserves both list and tuple inputs."""
    source = cards[:size]
    before = source.copy()
    ordered = SequentialStrategy().order(source)
    assert ordered == before
    assert ordered is not source
    ordered.clear()
    assert source == before
    assert SequentialStrategy().order(tuple(source)) == before


@pytest.mark.parametrize("size", [0, 1, 3])
@pytest.mark.parametrize("seed", [0, 7, 42])
def test_random_preserves_every_card_and_source_deck(
    cards: list[Flashcard], size: int, seed: int
) -> None:
    """A permutation is valid even when its order happens to be unchanged."""
    source = cards[:size]
    before = source.copy()
    ordered = RandomStrategy(Random(seed)).order(source)
    assert len(ordered) == len(source)
    assert Counter(ordered) == Counter(source)
    assert ordered is not source
    assert source == before
    ordered.clear()
    assert source == before


def test_same_seed_reproduces_order(cards: list[Flashcard]) -> None:
    """Independent RNGs with the same seed reproduce ordering in this runtime."""
    first = RandomStrategy(Random(23)).order(tuple(cards))
    second = RandomStrategy(Random(23)).order(tuple(cards))
    assert first == second
    assert Counter(first) == Counter(cards)


def test_private_rng_does_not_consume_global_state(cards: list[Flashcard]) -> None:
    """The default generator does not interfere with unrelated random behavior."""
    before = random.getstate()
    ordered = RandomStrategy().order(cards)
    assert Counter(ordered) == Counter(cards)
    assert random.getstate() == before


def test_unchanged_shuffle_is_valid(
    cards: list[Flashcard], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A controlled no-op shuffle still returns a valid independent permutation."""
    rng = Random(1)

    def keep_order(values: list[Flashcard]) -> None:
        """Represent the valid shuffle outcome that keeps source ordering."""

    monkeypatch.setattr(rng, "shuffle", keep_order)
    ordered = RandomStrategy(rng).order(cards)
    assert ordered == cards
    assert ordered is not cards


def test_adaptive_descending_scores_and_deck_order_ties(cards: list[Flashcard]) -> None:
    """Score rank takes precedence, while tied cards keep their input order."""
    scores = {cards[2].card_id: 3, cards[1].card_id: 1, cards[0].card_id: 1}
    before = cards.copy()
    ordered = AdaptiveStrategy(scores).order(cards)
    assert ordered == [cards[2], cards[0], cards[1]]
    assert cards == before


@pytest.mark.parametrize("size", [0, 1, 3])
def test_adaptive_missing_scores_preserve_deck_order(
    cards: list[Flashcard], size: int
) -> None:
    """New cards and fresh profiles are a stable zero-score permutation."""
    source = cards[:size]
    ordered = AdaptiveStrategy({}).order(source)
    assert ordered == source
    assert ordered is not source


def test_adaptive_snapshots_scores_and_respects_reordered_ties(
    cards: list[Flashcard],
) -> None:
    """Later mapping edits cannot change a strategy's selection snapshot."""
    scores = {card.card_id: 1 for card in reversed(cards)}
    strategy = AdaptiveStrategy(scores)
    scores[cards[2].card_id] = 100
    assert strategy.order(cards) == cards
    assert strategy.order(list(reversed(cards))) == list(reversed(cards))
