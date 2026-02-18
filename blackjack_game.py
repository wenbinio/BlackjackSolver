"""
Chinese New Year Blackjack Game Logic

This module implements the core game logic for a custom Chinese New Year blackjack variant.
"""

from typing import List, Tuple, Optional
from enum import Enum
from itertools import combinations


class Suit(Enum):
    """Card suits"""
    SPADES = '♠'
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'


class Card:
    """Represents a playing card"""
    
    def __init__(self, rank: str, suit: Suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        return f"{self.rank}{self.suit.value}"
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))


class Hand:
    """Represents a blackjack hand"""
    
    def __init__(self, cards: Optional[List[Card]] = None):
        self.cards = cards if cards else []
    
    def add_card(self, card: Card):
        """Add a card to the hand"""
        self.cards.append(card)
    
    def is_ban_ban(self) -> bool:
        """Check if hand is Ban Ban (AA) - two Aces"""
        return (len(self.cards) == 2 and 
                all(card.rank == 'A' for card in self.cards))
    
    def is_blackjack(self) -> Tuple[bool, bool]:
        """
        Check if hand is blackjack (A + 10/J/Q/K)
        Returns (is_blackjack, is_suited)
        """
        if len(self.cards) != 2:
            return False, False
        
        has_ace = any(card.rank == 'A' for card in self.cards)
        has_ten = any(card.rank in ['10', 'J', 'Q', 'K'] for card in self.cards)
        
        if has_ace and has_ten:
            is_suited = self.cards[0].suit == self.cards[1].suit
            return True, is_suited
        
        return False, False
    
    def is_triple_sevens(self) -> bool:
        """Check if hand is triple 7s"""
        return (len(self.cards) == 3 and 
                all(card.rank == '7' for card in self.cards))
    
    def is_five_card_charlie(self) -> bool:
        """Check if hand is 5-Card Charlie (5 cards without busting)"""
        return len(self.cards) == 5 and not self.is_bust()
    
    def get_ace_count(self) -> int:
        """Get number of Aces in hand"""
        return sum(1 for card in self.cards if card.rank == 'A')
    
    def get_possible_values(self) -> List[int]:
        """
        Get all possible hand values according to custom Ace rules:
        - 2 cards: Ace = 1/10/11
        - 3 cards: Ace = 1/10
        - 4+ cards: Ace = 1
        """
        num_cards = len(self.cards)
        ace_count = self.get_ace_count()
        non_ace_value = sum(self._get_card_value(card) for card in self.cards if card.rank != 'A')
        
        if num_cards == 2:
            # Ace can be 1, 10, or 11
            ace_values_per_ace = [1, 10, 11]
        elif num_cards == 3:
            # Ace can be 1 or 10
            ace_values_per_ace = [1, 10]
        else:
            # Ace can only be 1
            ace_values_per_ace = [1]
        
        # Generate all combinations of ace values
        if ace_count == 0:
            return [non_ace_value]
        
        values = set()
        if ace_count == 1:
            for val in ace_values_per_ace:
                values.add(non_ace_value + val)
        elif ace_count == 2:
            for val1 in ace_values_per_ace:
                for val2 in ace_values_per_ace:
                    values.add(non_ace_value + val1 + val2)
        else:
            # For 3+ aces, they all must be 1
            values.add(non_ace_value + ace_count)
        
        return sorted(list(values))
    
    def _get_card_value(self, card: Card) -> int:
        """Get base value of a non-ace card"""
        if card.rank == 'A':
            return 0  # Handle separately
        elif card.rank in ['J', 'Q', 'K']:
            return 10
        else:
            return int(card.rank)
    
    def get_best_value(self) -> int:
        """Get the best non-busting value, or lowest value if all bust"""
        values = self.get_possible_values()
        non_bust = [v for v in values if v <= 21]
        return max(non_bust) if non_bust else min(values)
    
    def is_bust(self) -> bool:
        """Check if all possible values exceed 21"""
        return all(v > 21 for v in self.get_possible_values())
    
    def get_payout_multiplier(self) -> float:
        """Get the payout multiplier for special hands"""
        if self.is_bust():
            return 0.0
        
        if self.is_ban_ban():
            return 3.0
        
        if self.is_triple_sevens():
            return 7.0
        
        is_bj, is_suited = self.is_blackjack()
        if is_bj:
            return 3.0 if is_suited else 2.0
        
        if self.is_five_card_charlie():
            return 2.0
        
        return 1.0
    
    def __repr__(self):
        return f"Hand({', '.join(str(card) for card in self.cards)})"


def create_deck() -> List[Card]:
    """Create a standard 52-card deck"""
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = list(Suit)
    return [Card(rank, suit) for rank in ranks for suit in suits]


def compare_hands(player_hand: Hand, dealer_hand: Hand) -> str:
    """
    Compare player and dealer hands
    Returns: 'win', 'lose', 'push'
    """
    player_bust = player_hand.is_bust()
    dealer_bust = dealer_hand.is_bust()
    
    # Player busts = loss
    if player_bust:
        return 'lose'
    
    # Dealer busts = win (if player didn't bust)
    if dealer_bust:
        return 'win'
    
    # Compare best values
    player_value = player_hand.get_best_value()
    dealer_value = dealer_hand.get_best_value()
    
    if player_value > dealer_value:
        return 'win'
    elif player_value < dealer_value:
        return 'lose'
    else:
        return 'push'
