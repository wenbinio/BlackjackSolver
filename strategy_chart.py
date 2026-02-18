"""
Strategy Chart Generator

Creates basic strategy charts for Chinese New Year Blackjack.
"""

from solver import BlackjackSolver, Card, Suit


def generate_basic_strategy_chart():
    """Generate a basic strategy chart for common situations"""
    solver = BlackjackSolver()
    
    print("\n" + "=" * 80)
    print(" " * 20 + "BASIC STRATEGY CHART")
    print("=" * 80)
    print("\nPlayer Hand vs Dealer Upcard")
    print("H = Hit, S = Stand")
    print("-" * 80)
    
    # Hard totals (no Ace or Ace counted as 1)
    print("\nHARD TOTALS:")
    print("Player | 2   3   4   5   6   7   8   9   10  A")
    print("-------+----------------------------------------")
    
    hard_hands = [
        (17, [Card('10', Suit.SPADES), Card('7', Suit.HEARTS)]),
        (16, [Card('10', Suit.SPADES), Card('6', Suit.HEARTS)]),
        (15, [Card('10', Suit.SPADES), Card('5', Suit.HEARTS)]),
        (14, [Card('10', Suit.SPADES), Card('4', Suit.HEARTS)]),
        (13, [Card('10', Suit.SPADES), Card('3', Suit.HEARTS)]),
        (12, [Card('10', Suit.SPADES), Card('2', Suit.HEARTS)]),
    ]
    
    for total, cards in hard_hands:
        actions = []
        for dealer_rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']:
            dealer_card = Card(dealer_rank, Suit.CLUBS)
            result = solver.solve_hand(cards, dealer_card)
            action = 'H' if result['optimal_action'] == 'hit' else 'S'
            actions.append(action)
        
        print(f"  {total:2d}   | " + "   ".join(actions))
    
    # Soft totals (Ace counted as 11)
    print("\nSOFT TOTALS (with Ace):")
    print("Player | 2   3   4   5   6   7   8   9   10  A")
    print("-------+----------------------------------------")
    
    soft_hands = [
        ('A,8', [Card('A', Suit.SPADES), Card('8', Suit.HEARTS)]),
        ('A,7', [Card('A', Suit.SPADES), Card('7', Suit.HEARTS)]),
        ('A,6', [Card('A', Suit.SPADES), Card('6', Suit.HEARTS)]),
        ('A,5', [Card('A', Suit.SPADES), Card('5', Suit.HEARTS)]),
        ('A,4', [Card('A', Suit.SPADES), Card('4', Suit.HEARTS)]),
        ('A,3', [Card('A', Suit.SPADES), Card('3', Suit.HEARTS)]),
        ('A,2', [Card('A', Suit.SPADES), Card('2', Suit.HEARTS)]),
    ]
    
    for label, cards in soft_hands:
        actions = []
        for dealer_rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']:
            dealer_card = Card(dealer_rank, Suit.CLUBS)
            result = solver.solve_hand(cards, dealer_card)
            action = 'H' if result['optimal_action'] == 'hit' else 'S'
            actions.append(action)
        
        print(f" {label:5s} | " + "   ".join(actions))
    
    # Pairs
    print("\nPAIRS (note: no splitting allowed in this variant):")
    print("Player | 2   3   4   5   6   7   8   9   10  A")
    print("-------+----------------------------------------")
    
    pair_hands = [
        ('A,A', [Card('A', Suit.SPADES), Card('A', Suit.HEARTS)]),  # Ban Ban
        ('10,10', [Card('10', Suit.SPADES), Card('10', Suit.HEARTS)]),
        ('9,9', [Card('9', Suit.SPADES), Card('9', Suit.HEARTS)]),
        ('8,8', [Card('8', Suit.SPADES), Card('8', Suit.HEARTS)]),
        ('7,7', [Card('7', Suit.SPADES), Card('7', Suit.HEARTS)]),
    ]
    
    for label, cards in pair_hands:
        actions = []
        for dealer_rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']:
            dealer_card = Card(dealer_rank, Suit.CLUBS)
            result = solver.solve_hand(cards, dealer_card)
            action = 'H' if result['optimal_action'] == 'hit' else 'S'
            # Special notation for Ban Ban
            if label == 'A,A':
                action = 'BB'  # Ban Ban - automatic stand
            actions.append(action)
        
        print(f" {label:5s} | " + "  ".join(actions))
    
    print("\nBB = Ban Ban (automatic 3× payout)")
    print("=" * 80)
    
    # Special hands section
    print("\n" + "=" * 80)
    print(" " * 25 + "SPECIAL HANDS")
    print("=" * 80)
    print("\n1. Ban Ban (A♠ A♥, A♦ A♣, etc.) → Always STAND → 3× payout")
    print("2. Blackjack (A + 10/J/Q/K):")
    print("   - Same suit → Always STAND → 3× payout")
    print("   - Different suits → Always STAND → 2× payout")
    print("3. Triple 7s (7♠ 7♥ 7♣, etc.) → Always STAND → 7× payout")
    print("4. 5-Card Charlie (5 cards, not bust) → Always STAND → 2× payout")
    print("=" * 80)
    
    # Key insights
    print("\n" + "=" * 80)
    print(" " * 25 + "KEY INSIGHTS")
    print("=" * 80)
    print("\n• Custom Ace Rules:")
    print("  - 2 cards: Ace = 1, 10, or 11")
    print("  - 3 cards: Ace = 1 or 10")
    print("  - 4+ cards: Ace = 1 only")
    print("\n• No Splitting or Doubling:")
    print("  - Pair of Aces = Ban Ban (3×) - better than splitting!")
    print("  - Play pairs as their total value")
    print("\n• 5-Card Strategy:")
    print("  - Getting to 5 cards without busting = automatic 2× payout")
    print("  - Consider hitting on lower totals to reach 5 cards")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    generate_basic_strategy_chart()
