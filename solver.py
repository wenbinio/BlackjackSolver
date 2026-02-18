"""
Chinese New Year Blackjack Solver

Main solver interface that provides optimal play recommendations for every hand.
"""

from typing import List, Dict, Optional
from blackjack_game import Card, Hand, Suit, create_deck
from probability_calculator import ProbabilityCalculator


class BlackjackSolver:
    """Probability-based solver for Chinese New Year blackjack"""
    
    def __init__(self):
        self.calculator = ProbabilityCalculator()
    
    def solve_hand(self, player_cards: List[Card], dealer_upcard: Card) -> Dict:
        """
        Solve a specific hand and return optimal strategy
        
        Args:
            player_cards: List of cards in player's hand
            dealer_upcard: Dealer's visible card
        
        Returns:
            Dictionary with strategy information
        """
        player_hand = Hand(player_cards)
        known_cards = player_cards + [dealer_upcard]
        
        action, stand_ev, hit_ev = self.calculator.get_optimal_action(
            player_hand, dealer_upcard, known_cards
        )
        
        result = {
            'player_hand': str(player_hand),
            'player_value': player_hand.get_best_value() if not player_hand.is_bust() else 'BUST',
            'possible_values': player_hand.get_possible_values(),
            'dealer_upcard': str(dealer_upcard),
            'optimal_action': action,
            'stand_ev': round(stand_ev, 4),
            'hit_ev': round(hit_ev, 4),
            'best_ev': round(max(stand_ev, hit_ev), 4),
            'special_hand': self._get_special_hand_type(player_hand),
            'payout_multiplier': player_hand.get_payout_multiplier()
        }
        
        return result
    
    def _get_special_hand_type(self, hand: Hand) -> Optional[str]:
        """Identify special hand type"""
        if hand.is_ban_ban():
            return 'Ban Ban (3×)'
        if hand.is_triple_sevens():
            return 'Triple 7s (7×)'
        
        is_bj, is_suited = hand.is_blackjack()
        if is_bj:
            if is_suited:
                return 'Suited Blackjack (3×)'
            else:
                return 'Blackjack (2×)'
        
        if hand.is_five_card_charlie():
            return '5-Card Charlie (2×)'
        
        return None
    
    def generate_strategy_table(self, player_total: int, num_cards: int) -> Dict:
        """
        Generate strategy recommendations for a given player total
        against all possible dealer upcards
        """
        results = {}
        
        # Create a sample hand with the given total
        # This is simplified - we'll show general strategy
        for dealer_rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
            dealer_card = Card(dealer_rank, Suit.SPADES)
            
            # Create a simple hand that sums to the target
            # (This is a simplification for strategy table generation)
            player_cards = self._create_hand_with_total(player_total, num_cards)
            if player_cards:
                result = self.solve_hand(player_cards, dealer_card)
                results[dealer_rank] = {
                    'action': result['optimal_action'],
                    'ev': result['best_ev']
                }
        
        return results
    
    def _create_hand_with_total(self, target: int, num_cards: int) -> Optional[List[Card]]:
        """
        Create a sample hand with given total and card count
        Note: This is a simplified helper for strategy table generation
        """
        if num_cards == 2:
            # Try to create a 2-card hand
            if target <= 11 and target >= 3:
                # Use Ace + another card (e.g., A+2=3 to A+10=11)
                first_val = target - 1
                if first_val < 2:
                    first_val = 2
                if first_val > 10:
                    first_val = 10
                cards = [Card(str(first_val), Suit.SPADES), Card('A', Suit.HEARTS)]
            elif target <= 20 and target >= 12:
                first = target - 10
                if first < 2:
                    first = 2
                if first > 10:
                    first = 10
                cards = [Card(str(first), Suit.SPADES), Card('10', Suit.HEARTS)]
            elif target == 21:
                cards = [Card('10', Suit.SPADES), Card('A', Suit.HEARTS)]
            else:
                return None
            return cards
        elif num_cards == 3:
            # Create a 3-card hand
            if target <= 12 and target >= 6:
                remainder = target - 4
                if remainder < 2:
                    remainder = 2
                if remainder > 10:
                    remainder = 10
                cards = [Card('2', Suit.SPADES), Card('2', Suit.HEARTS), Card(str(remainder), Suit.CLUBS)]
            elif target >= 13:
                remainder = target - 10
                if remainder < 2:
                    remainder = 2
                if remainder > 10:
                    remainder = 10
                cards = [Card('5', Suit.SPADES), Card('5', Suit.HEARTS), Card(str(remainder), Suit.CLUBS)]
            else:
                return None
            return cards
        else:
            # For 4+ cards, distribute evenly
            base = target // num_cards
            remainder = target % num_cards
            cards = []
            for i in range(num_cards):
                val = base + (1 if i < remainder else 0)
                if val < 2:
                    val = 2
                if val > 10:
                    val = 10
                cards.append(Card(str(val), list(Suit)[i % 4]))
            return cards
    
    def print_strategy(self, result: Dict):
        """Pretty print strategy recommendation"""
        print("=" * 60)
        print(f"Player Hand: {result['player_hand']}")
        print(f"Best Value: {result['player_value']}")
        if len(result['possible_values']) > 1:
            print(f"Possible Values: {result['possible_values']}")
        print(f"Dealer Upcard: {result['dealer_upcard']}")
        print(f"\nSpecial Hand: {result['special_hand'] or 'None'}")
        print(f"Payout Multiplier: {result['payout_multiplier']}×")
        print("\n" + "-" * 60)
        print(f"OPTIMAL ACTION: {result['optimal_action'].upper()}")
        print(f"Expected Value (Stand): {result['stand_ev']}")
        print(f"Expected Value (Hit): {result['hit_ev']}")
        print(f"Best EV: {result['best_ev']}")
        print("=" * 60)


def parse_card(card_str: str) -> Card:
    """Parse a card string like 'AS' (Ace of Spades) into a Card object"""
    rank = card_str[:-1]
    suit_char = card_str[-1]
    
    suit_map = {
        'S': Suit.SPADES,
        'H': Suit.HEARTS,
        'D': Suit.DIAMONDS,
        'C': Suit.CLUBS
    }
    
    return Card(rank, suit_map[suit_char])


def main():
    """Main solver interface"""
    print("\n" + "=" * 60)
    print("Chinese New Year Blackjack Solver")
    print("=" * 60)
    print("\nRules:")
    print("- 1 deck, $2/hand, ties push")
    print("- No splitting, no doubling, no free hit")
    print("- Ace = 1/10/11 (2 cards), 1/10 (3 cards), 1 (4+ cards)")
    print("\nSpecial Hands:")
    print("- Ban Ban (AA) → 3×")
    print("- Blackjack (A + 10/J/Q/K) → 2× (suited → 3×)")
    print("- Triple 7s → 7×")
    print("- 5-Card Charlie → 2×")
    print("=" * 60)
    
    solver = BlackjackSolver()
    
    # Example hands
    examples = [
        {
            'name': 'Ban Ban (Pair of Aces)',
            'player': [Card('A', Suit.SPADES), Card('A', Suit.HEARTS)],
            'dealer': Card('10', Suit.DIAMONDS)
        },
        {
            'name': 'Suited Blackjack',
            'player': [Card('A', Suit.HEARTS), Card('K', Suit.HEARTS)],
            'dealer': Card('7', Suit.CLUBS)
        },
        {
            'name': 'Regular Blackjack',
            'player': [Card('A', Suit.SPADES), Card('Q', Suit.HEARTS)],
            'dealer': Card('9', Suit.DIAMONDS)
        },
        {
            'name': 'Hard 16',
            'player': [Card('10', Suit.SPADES), Card('6', Suit.HEARTS)],
            'dealer': Card('10', Suit.CLUBS)
        },
        {
            'name': 'Soft 17 (with Ace)',
            'player': [Card('A', Suit.SPADES), Card('6', Suit.HEARTS)],
            'dealer': Card('5', Suit.DIAMONDS)
        },
        {
            'name': 'Triple 7s',
            'player': [Card('7', Suit.SPADES), Card('7', Suit.HEARTS), Card('7', Suit.CLUBS)],
            'dealer': Card('8', Suit.DIAMONDS)
        },
        {
            'name': '4-Card Hand (Ace values = 1)',
            'player': [Card('A', Suit.SPADES), Card('5', Suit.HEARTS), Card('3', Suit.CLUBS), Card('4', Suit.DIAMONDS)],
            'dealer': Card('6', Suit.CLUBS)
        }
    ]
    
    print("\n\nExample Hands and Optimal Strategies:\n")
    
    for example in examples:
        print(f"\n{example['name']}:")
        result = solver.solve_hand(example['player'], example['dealer'])
        solver.print_strategy(result)
        print()


if __name__ == '__main__':
    main()
