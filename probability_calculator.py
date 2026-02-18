"""
Probability Calculator for Chinese New Year Blackjack

This module calculates probabilities and expected values for optimal play.
"""

from typing import List, Tuple, Dict
from itertools import combinations
import math
from blackjack_game import Card, Hand, create_deck, compare_hands, Suit


class ProbabilityCalculator:
    """Calculates probabilities and expected values for blackjack hands"""
    
    def __init__(self):
        self.deck = create_deck()
        self.deck_size = len(self.deck)
    
    def calculate_card_probabilities(self, remaining_cards: List[Card]) -> Dict[str, float]:
        """Calculate probability of drawing each rank"""
        total = len(remaining_cards)
        if total == 0:
            return {}
        
        rank_counts = {}
        for card in remaining_cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        
        return {rank: count / total for rank, count in rank_counts.items()}
    
    def get_remaining_cards(self, known_cards: List[Card]) -> List[Card]:
        """Get list of remaining cards in deck"""
        remaining = self.deck.copy()
        for card in known_cards:
            if card in remaining:
                remaining.remove(card)
        return remaining
    
    def calculate_dealer_bust_probability(self, dealer_hand: Hand, remaining_cards: List[Card]) -> float:
        """Calculate probability that dealer will bust"""
        if dealer_hand.is_bust():
            return 1.0
        
        if len(dealer_hand.cards) >= 5:
            return 0.0  # 5-card charlie
        
        dealer_value = dealer_hand.get_best_value()
        if dealer_value >= 17:
            return 0.0  # Dealer stands
        
        # Calculate probability recursively
        bust_prob = 0.0
        total_cards = len(remaining_cards)
        
        if total_cards == 0:
            return 0.0
        
        # Group cards by rank for efficiency
        rank_counts = {}
        for card in remaining_cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        
        for rank, count in rank_counts.items():
            prob = count / total_cards
            
            # Try adding this card
            test_card = Card(rank, Suit.SPADES)  # Suit doesn't matter for value
            new_hand = Hand(dealer_hand.cards.copy())
            new_hand.add_card(test_card)
            
            # Get new remaining cards
            new_remaining = remaining_cards.copy()
            # Remove one card of this rank
            for i, card in enumerate(new_remaining):
                if card.rank == rank:
                    new_remaining.pop(i)
                    break
            
            if new_hand.is_bust():
                bust_prob += prob * 1.0
            else:
                bust_prob += prob * self.calculate_dealer_bust_probability(new_hand, new_remaining)
        
        return bust_prob
    
    def calculate_hit_ev(self, player_hand: Hand, dealer_upcard: Card, remaining_cards: List[Card]) -> float:
        """Calculate expected value of hitting"""
        if player_hand.is_bust():
            return -1.0
        
        if len(player_hand.cards) >= 5:
            # Can't hit with 5 cards (5-card charlie)
            return self.calculate_stand_ev(player_hand, dealer_upcard, remaining_cards)
        
        total_cards = len(remaining_cards)
        if total_cards == 0:
            return -1.0
        
        ev = 0.0
        
        # Group cards by rank
        rank_counts = {}
        for card in remaining_cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        
        for rank, count in rank_counts.items():
            prob = count / total_cards
            
            # Create new hand with this card
            test_card = Card(rank, Suit.SPADES)
            new_hand = Hand(player_hand.cards.copy())
            new_hand.add_card(test_card)
            
            # Update remaining cards
            new_remaining = remaining_cards.copy()
            for i, card in enumerate(new_remaining):
                if card.rank == rank:
                    new_remaining.pop(i)
                    break
            
            if new_hand.is_bust():
                # Bust = lose
                ev += prob * -1.0
            else:
                # Check for special hands that auto-win
                if new_hand.is_five_card_charlie():
                    ev += prob * new_hand.get_payout_multiplier()
                else:
                    # Recursively calculate best play
                    stand_ev = self.calculate_stand_ev(new_hand, dealer_upcard, new_remaining)
                    hit_ev = self.calculate_hit_ev(new_hand, dealer_upcard, new_remaining)
                    ev += prob * max(stand_ev, hit_ev)
        
        return ev
    
    def calculate_stand_ev(self, player_hand: Hand, dealer_upcard: Card, remaining_cards: List[Card]) -> float:
        """Calculate expected value of standing"""
        if player_hand.is_bust():
            return -1.0
        
        player_multiplier = player_hand.get_payout_multiplier()
        
        # Simulate all possible dealer outcomes
        ev = 0.0
        
        # For efficiency, we'll sample or use a simplified dealer strategy
        # Dealer plays optimally trying to beat the player
        dealer_hand = Hand([dealer_upcard])
        
        # Calculate probability of each dealer outcome
        ev = self._calculate_dealer_outcomes(player_hand, dealer_hand, remaining_cards)
        
        return ev * player_multiplier
    
    def _calculate_dealer_outcomes(self, player_hand: Hand, dealer_hand: Hand, remaining_cards: List[Card]) -> float:
        """Calculate expected value against dealer's optimal play"""
        # Simplified: assume dealer follows basic strategy
        # Dealer hits until reaching 17 or busting
        
        if dealer_hand.is_bust():
            return 1.0  # Player wins
        
        dealer_value = dealer_hand.get_best_value()
        
        # Check for dealer special hands
        if dealer_hand.is_five_card_charlie() or dealer_value >= 17:
            result = compare_hands(player_hand, dealer_hand)
            if result == 'win':
                return 1.0
            elif result == 'lose':
                return -1.0
            else:
                return 0.0
        
        # Dealer must hit
        total_cards = len(remaining_cards)
        if total_cards == 0:
            # No cards left, compare current hands
            result = compare_hands(player_hand, dealer_hand)
            if result == 'win':
                return 1.0
            elif result == 'lose':
                return -1.0
            else:
                return 0.0
        
        ev = 0.0
        
        # Group by rank for efficiency
        rank_counts = {}
        for card in remaining_cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        
        for rank, count in rank_counts.items():
            prob = count / total_cards
            
            test_card = Card(rank, Suit.SPADES)
            new_dealer_hand = Hand(dealer_hand.cards.copy())
            new_dealer_hand.add_card(test_card)
            
            new_remaining = remaining_cards.copy()
            for i, card in enumerate(new_remaining):
                if card.rank == rank:
                    new_remaining.pop(i)
                    break
            
            ev += prob * self._calculate_dealer_outcomes(player_hand, new_dealer_hand, new_remaining)
        
        return ev
    
    def get_optimal_action(self, player_hand: Hand, dealer_upcard: Card, known_cards: List[Card]) -> Tuple[str, float, float]:
        """
        Get optimal action for player
        Returns: (action, stand_ev, hit_ev)
        """
        remaining_cards = self.get_remaining_cards(known_cards)
        
        # Check for automatic situations
        if player_hand.is_bust():
            return 'bust', -1.0, -1.0
        
        if player_hand.is_ban_ban() or player_hand.is_triple_sevens():
            # These are automatic wins, stand
            return 'stand', player_hand.get_payout_multiplier(), 0.0
        
        is_bj, _ = player_hand.is_blackjack()
        if is_bj:
            return 'stand', player_hand.get_payout_multiplier(), 0.0
        
        if player_hand.is_five_card_charlie():
            return 'stand', player_hand.get_payout_multiplier(), 0.0
        
        if len(player_hand.cards) >= 5:
            # Can't hit beyond 5 cards
            stand_ev = self.calculate_stand_ev(player_hand, dealer_upcard, remaining_cards)
            return 'stand', stand_ev, 0.0
        
        # Calculate EVs for both actions
        stand_ev = self.calculate_stand_ev(player_hand, dealer_upcard, remaining_cards)
        hit_ev = self.calculate_hit_ev(player_hand, dealer_upcard, remaining_cards)
        
        if hit_ev > stand_ev:
            return 'hit', stand_ev, hit_ev
        else:
            return 'stand', stand_ev, hit_ev
