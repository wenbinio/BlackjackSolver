#!/usr/bin/env python3
"""
Interactive CLI for Chinese New Year Blackjack Solver

Allows users to input hands and get optimal strategy recommendations.
"""

from solver import BlackjackSolver, Card, Suit


def parse_card_input(card_str: str) -> Card:
    """
    Parse a card string like 'AS' (Ace of Spades), 'KH' (King of Hearts), etc.
    Format: <rank><suit>
    Ranks: A, 2-10, J, Q, K
    Suits: S (Spades), H (Hearts), D (Diamonds), C (Clubs)
    """
    card_str = card_str.strip().upper()
    
    # Parse suit (last character)
    suit_char = card_str[-1]
    suit_map = {
        'S': Suit.SPADES,
        'H': Suit.HEARTS,
        'D': Suit.DIAMONDS,
        'C': Suit.CLUBS
    }
    
    if suit_char not in suit_map:
        raise ValueError(f"Invalid suit: {suit_char}. Use S, H, D, or C.")
    
    # Parse rank (everything except last character)
    rank = card_str[:-1]
    valid_ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    if rank not in valid_ranks:
        raise ValueError(f"Invalid rank: {rank}. Use A, 2-10, J, Q, or K.")
    
    return Card(rank, suit_map[suit_char])


def print_header():
    """Print the application header"""
    print("\n" + "=" * 70)
    print(" " * 15 + "Chinese New Year Blackjack Solver")
    print("=" * 70)
    print("\nRules:")
    print("  • 1 deck, $2/hand, ties push")
    print("  • No splitting, no doubling, no free hit")
    print("  • Ace = 1/10/11 (2 cards), 1/10 (3 cards), 1 (4+ cards)")
    print("\nSpecial Hands:")
    print("  • Ban Ban (AA) → 3×")
    print("  • Blackjack (A + 10/J/Q/K) → 2× (suited → 3×)")
    print("  • Triple 7s → 7×")
    print("  • 5-Card Charlie → 2×")
    print("=" * 70)


def get_player_hand() -> list:
    """Get player hand from user input"""
    print("\nEnter your hand (e.g., 'AS KH' for Ace of Spades, King of Hearts):")
    print("Card format: <rank><suit>")
    print("  Ranks: A, 2-10, J, Q, K")
    print("  Suits: S (♠), H (♥), D (♦), C (♣)")
    print("  Example: AS 10H 5D")
    
    while True:
        try:
            cards_input = input("\nYour cards: ").strip()
            if not cards_input:
                print("Please enter at least one card.")
                continue
            
            card_strings = cards_input.split()
            if len(card_strings) < 2:
                print("Please enter at least 2 cards.")
                continue
            
            cards = [parse_card_input(cs) for cs in card_strings]
            return cards
        
        except ValueError as e:
            print(f"Error: {e}")
            print("Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Please try again.")


def get_dealer_card() -> Card:
    """Get dealer's upcard from user input"""
    print("\nEnter dealer's upcard (e.g., '10C' for 10 of Clubs):")
    
    while True:
        try:
            card_input = input("Dealer's card: ").strip()
            if not card_input:
                print("Please enter a card.")
                continue
            
            card = parse_card_input(card_input)
            return card
        
        except ValueError as e:
            print(f"Error: {e}")
            print("Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Please try again.")


def main():
    """Main interactive CLI"""
    print_header()
    
    solver = BlackjackSolver()
    
    while True:
        try:
            # Get player hand
            player_cards = get_player_hand()
            
            # Get dealer upcard
            dealer_card = get_dealer_card()
            
            # Solve
            print("\n" + "─" * 70)
            print("Calculating optimal strategy...")
            print("─" * 70)
            
            result = solver.solve_hand(player_cards, dealer_card)
            solver.print_strategy(result)
            
            # Ask if user wants to continue
            print("\n" + "─" * 70)
            continue_input = input("\nAnalyze another hand? (y/n): ").strip().lower()
            if continue_input not in ['y', 'yes']:
                print("\nThank you for using the Chinese New Year Blackjack Solver!")
                print("Good luck at the tables! 🎲🃏\n")
                break
        
        except KeyboardInterrupt:
            print("\n\nExiting solver. Good luck! 🎲🃏\n")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please try again.\n")


if __name__ == '__main__':
    main()
