from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from math import comb
from typing import Dict, Iterable, List, Sequence, Tuple

RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
TEN_VALUE_RANKS = {"10", "J", "Q", "K"}
FULL_DECK = [f"{rank}{suit}" for suit in "SHDC" for rank in RANKS]


@dataclass(frozen=True)
class HandSolution:
    hand: Tuple[str, ...]
    best_action: str
    expected_value: float


def _rank(card: str) -> str:
    card = card.strip().upper()
    if not card:
        raise ValueError("Empty card")
    if len(card) >= 2 and card[:-1] in RANKS and card[-1] in "SHDC":
        return card[:-1]
    if card in RANKS:
        return card
    raise ValueError(f"Unsupported card format: {card}")


def _ace_options(card_count: int) -> Tuple[int, ...]:
    if card_count <= 2:
        return (1, 10, 11)
    if card_count == 3:
        return (1, 10)
    return (1,)


def _hand_totals(hand_ranks: Sequence[str]) -> Tuple[int, ...]:
    card_count = len(hand_ranks)
    base = 0
    aces = 0
    for rank in hand_ranks:
        if rank == "A":
            aces += 1
        elif rank in TEN_VALUE_RANKS:
            base += 10
        else:
            base += int(rank)

    if aces == 0:
        return (base,)

    totals = {base}
    for _ in range(aces):
        options = _ace_options(card_count)
        totals = {partial + option for partial in totals for option in options}
    return tuple(sorted(totals))


def best_total(hand_ranks: Sequence[str]) -> int:
    totals = _hand_totals(hand_ranks)
    under = [total for total in totals if total <= 21]
    return max(under) if under else min(totals)


def is_bust(hand_ranks: Sequence[str]) -> bool:
    return all(total > 21 for total in _hand_totals(hand_ranks))


def special_multiplier(hand_ranks: Sequence[str], suited_blackjack: bool = False) -> int:
    if is_bust(hand_ranks):
        return 1

    if len(hand_ranks) == 3 and all(rank == "7" for rank in hand_ranks):
        return 7
    if len(hand_ranks) == 2 and all(rank == "A" for rank in hand_ranks):
        return 3
    if len(hand_ranks) == 2 and "A" in hand_ranks and any(rank in TEN_VALUE_RANKS for rank in hand_ranks):
        return 3 if suited_blackjack else 2
    if len(hand_ranks) == 5:
        return 2
    return 1


def _player_beats_dealer(
    player_ranks: Sequence[str],
    dealer_ranks: Sequence[str],
    player_suited_blackjack: bool,
) -> int:
    if is_bust(player_ranks):
        return -1
    if is_bust(dealer_ranks):
        return special_multiplier(player_ranks, player_suited_blackjack)

    player_special = special_multiplier(player_ranks, player_suited_blackjack)
    if player_special > 1:
        return player_special

    player_total = best_total(player_ranks)
    dealer_total = best_total(dealer_ranks)
    if player_total > dealer_total:
        return 1
    if player_total < dealer_total:
        return -1
    return 0


def _draw_probabilities(counts: Tuple[int, ...]) -> Iterable[Tuple[int, float]]:
    total = sum(counts)
    for idx, count in enumerate(counts):
        if count:
            yield idx, count / total


def _remove_rank(counts: Tuple[int, ...], rank_idx: int) -> Tuple[int, ...]:
    mutable = list(counts)
    mutable[rank_idx] -= 1
    return tuple(mutable)


def _remove_two_ranks(counts: Tuple[int, ...], i: int, j: int) -> Tuple[int, ...]:
    mutable = list(counts)
    mutable[i] -= 1
    mutable[j] -= 1
    return tuple(mutable)


@lru_cache(maxsize=None)
def _dealer_value(
    player_ranks: Tuple[str, ...],
    player_suited_blackjack: bool,
    dealer_ranks: Tuple[str, ...],
    counts: Tuple[int, ...],
) -> float:
    stand_value = _player_beats_dealer(player_ranks, dealer_ranks, player_suited_blackjack)

    if is_bust(dealer_ranks) or len(dealer_ranks) >= 5 or sum(counts) == 0:
        return float(stand_value)

    hit_value = 0.0
    for idx, prob in _draw_probabilities(counts):
        next_counts = _remove_rank(counts, idx)
        next_hand = tuple(sorted(dealer_ranks + (RANKS[idx],)))
        hit_value += prob * _dealer_value(player_ranks, player_suited_blackjack, next_hand, next_counts)

    # Dealer chooses action that minimizes player EV.
    return min(float(stand_value), hit_value)


@lru_cache(maxsize=None)
def _player_value(
    player_ranks: Tuple[str, ...],
    player_suited_blackjack: bool,
    counts: Tuple[int, ...],
) -> float:
    stand_value = _dealer_start_value(player_ranks, player_suited_blackjack, counts)

    if is_bust(player_ranks) or len(player_ranks) >= 5 or sum(counts) == 0:
        return stand_value

    hit_value = 0.0
    for idx, prob in _draw_probabilities(counts):
        next_counts = _remove_rank(counts, idx)
        next_hand = tuple(sorted(player_ranks + (RANKS[idx],)))
        # Any hit removes 2-card suited-blackjack status.
        hit_value += prob * _player_value(next_hand, False, next_counts)

    return max(stand_value, hit_value)


@lru_cache(maxsize=None)
def _dealer_start_value(
    player_ranks: Tuple[str, ...],
    player_suited_blackjack: bool,
    counts: Tuple[int, ...],
) -> float:
    total_cards = sum(counts)
    if total_cards < 2:
        return float(_player_beats_dealer(player_ranks, tuple(), player_suited_blackjack))

    total_two_card_combos = comb(total_cards, 2)
    expected_value = 0.0

    for i, c_i in enumerate(counts):
        if c_i == 0:
            continue
        for j in range(i, len(counts)):
            c_j = counts[j]
            if c_j == 0:
                continue
            if i == j and c_i < 2:
                continue

            ways = comb(c_i, 2) if i == j else c_i * c_j
            prob = ways / total_two_card_combos
            next_counts = _remove_two_ranks(counts, i, j)
            dealer_ranks = tuple(sorted((RANKS[i], RANKS[j])))
            expected_value += prob * _dealer_value(player_ranks, player_suited_blackjack, dealer_ranks, next_counts)

    return expected_value


def _initial_rank_counts(hand_cards: Sequence[str]) -> Tuple[int, ...]:
    counts = {rank: 4 for rank in RANKS}
    for card in hand_cards:
        counts[_rank(card)] -= 1
    return tuple(counts[rank] for rank in RANKS)


def solve_hand(hand_cards: Sequence[str]) -> HandSolution:
    if len(hand_cards) != 2:
        raise ValueError("Expected exactly two starting cards")

    ranks = tuple(sorted(_rank(card) for card in hand_cards))
    suited_blackjack = (
        len(hand_cards[0]) >= 2
        and len(hand_cards[1]) >= 2
        and hand_cards[0][-1].upper() in "SHDC"
        and hand_cards[1][-1].upper() in "SHDC"
        and hand_cards[0][-1].upper() == hand_cards[1][-1].upper()
        and "A" in ranks
        and any(rank in TEN_VALUE_RANKS for rank in ranks)
    )
    counts = _initial_rank_counts(hand_cards)

    stand_value = _dealer_start_value(ranks, suited_blackjack, counts)
    hit_value = 0.0
    for idx, prob in _draw_probabilities(counts):
        next_counts = _remove_rank(counts, idx)
        next_hand = tuple(sorted(ranks + (RANKS[idx],)))
        hit_value += prob * _player_value(next_hand, False, next_counts)

    if hit_value > stand_value:
        return HandSolution(tuple(hand_cards), "hit", hit_value)
    return HandSolution(tuple(hand_cards), "stand", stand_value)


def solve_all_two_card_hands() -> Dict[Tuple[str, str], HandSolution]:
    solutions: Dict[Tuple[str, str], HandSolution] = {}
    for card_a, card_b in combinations(FULL_DECK, 2):
        hand = tuple(sorted((card_a, card_b)))
        solutions[hand] = solve_hand(hand)
    return solutions


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) == 3:
        result = solve_hand((sys.argv[1], sys.argv[2]))
        print(json.dumps(result.__dict__, indent=2))
    else:
        all_results = solve_all_two_card_hands()
        print(json.dumps({"hands": len(all_results)}, indent=2))
