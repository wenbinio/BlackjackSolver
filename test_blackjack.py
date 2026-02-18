"""
Unit tests for Chinese New Year Blackjack Solver
"""

import unittest
from blackjack_game import Card, Hand, Suit, create_deck, compare_hands


class TestCard(unittest.TestCase):
    """Test Card class"""
    
    def test_card_creation(self):
        card = Card('A', Suit.SPADES)
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, Suit.SPADES)
    
    def test_card_equality(self):
        card1 = Card('K', Suit.HEARTS)
        card2 = Card('K', Suit.HEARTS)
        card3 = Card('K', Suit.SPADES)
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)


class TestHand(unittest.TestCase):
    """Test Hand class"""
    
    def test_ban_ban(self):
        """Test Ban Ban detection (AA)"""
        hand = Hand([Card('A', Suit.SPADES), Card('A', Suit.HEARTS)])
        self.assertTrue(hand.is_ban_ban())
        self.assertEqual(hand.get_payout_multiplier(), 3.0)
    
    def test_suited_blackjack(self):
        """Test suited blackjack detection"""
        hand = Hand([Card('A', Suit.HEARTS), Card('K', Suit.HEARTS)])
        is_bj, is_suited = hand.is_blackjack()
        self.assertTrue(is_bj)
        self.assertTrue(is_suited)
        self.assertEqual(hand.get_payout_multiplier(), 3.0)
    
    def test_regular_blackjack(self):
        """Test regular blackjack detection"""
        hand = Hand([Card('A', Suit.SPADES), Card('Q', Suit.HEARTS)])
        is_bj, is_suited = hand.is_blackjack()
        self.assertTrue(is_bj)
        self.assertFalse(is_suited)
        self.assertEqual(hand.get_payout_multiplier(), 2.0)
    
    def test_triple_sevens(self):
        """Test triple 7s detection"""
        hand = Hand([Card('7', Suit.SPADES), Card('7', Suit.HEARTS), Card('7', Suit.CLUBS)])
        self.assertTrue(hand.is_triple_sevens())
        self.assertEqual(hand.get_payout_multiplier(), 7.0)
    
    def test_five_card_charlie(self):
        """Test 5-card charlie detection"""
        hand = Hand([
            Card('2', Suit.SPADES),
            Card('3', Suit.HEARTS),
            Card('4', Suit.CLUBS),
            Card('5', Suit.DIAMONDS),
            Card('6', Suit.SPADES)
        ])
        self.assertTrue(hand.is_five_card_charlie())
        self.assertEqual(hand.get_payout_multiplier(), 2.0)
    
    def test_ace_values_two_cards(self):
        """Test Ace can be 1/10/11 with 2 cards"""
        hand = Hand([Card('A', Suit.SPADES), Card('5', Suit.HEARTS)])
        values = hand.get_possible_values()
        # A=1: 1+5=6, A=10: 10+5=15, A=11: 11+5=16
        self.assertIn(6, values)
        self.assertIn(15, values)
        self.assertIn(16, values)
    
    def test_ace_values_three_cards(self):
        """Test Ace can be 1/10 with 3 cards"""
        hand = Hand([Card('A', Suit.SPADES), Card('5', Suit.HEARTS), Card('3', Suit.CLUBS)])
        values = hand.get_possible_values()
        # A=1: 1+5+3=9, A=10: 10+5+3=18
        self.assertIn(9, values)
        self.assertIn(18, values)
        self.assertNotIn(19, values)  # A cannot be 11 with 3 cards
    
    def test_ace_values_four_cards(self):
        """Test Ace can only be 1 with 4+ cards"""
        hand = Hand([Card('A', Suit.SPADES), Card('5', Suit.HEARTS), 
                     Card('3', Suit.CLUBS), Card('4', Suit.DIAMONDS)])
        values = hand.get_possible_values()
        # A=1: 1+5+3+4=13
        self.assertEqual(values, [13])
    
    def test_double_ace_two_cards(self):
        """Test two Aces with 2 cards - possible unique values: 2, 11, 12, 20, 21, 22"""
        hand = Hand([Card('A', Suit.SPADES), Card('A', Suit.HEARTS)])
        values = hand.get_possible_values()
        # Each Ace can be 1, 10, or 11, giving combinations:
        # 1+1=2, 1+10=11, 1+11=12, 10+10=20, 10+11=21, 11+11=22
        self.assertIn(2, values)
        self.assertIn(11, values)
        self.assertIn(12, values)
        self.assertIn(20, values)
        self.assertIn(21, values)
        self.assertIn(22, values)
    
    def test_best_value(self):
        """Test getting best non-bust value"""
        hand = Hand([Card('K', Suit.SPADES), Card('9', Suit.HEARTS)])
        self.assertEqual(hand.get_best_value(), 19)
        
        # Soft hand
        hand2 = Hand([Card('A', Suit.SPADES), Card('8', Suit.HEARTS)])
        self.assertEqual(hand2.get_best_value(), 19)  # 11+8=19
    
    def test_bust(self):
        """Test bust detection"""
        hand = Hand([Card('K', Suit.SPADES), Card('Q', Suit.HEARTS), Card('5', Suit.CLUBS)])
        self.assertTrue(hand.is_bust())
        self.assertEqual(hand.get_payout_multiplier(), 0.0)


class TestCompareHands(unittest.TestCase):
    """Test hand comparison"""
    
    def test_player_wins(self):
        player = Hand([Card('K', Suit.SPADES), Card('9', Suit.HEARTS)])
        dealer = Hand([Card('10', Suit.CLUBS), Card('8', Suit.DIAMONDS)])
        self.assertEqual(compare_hands(player, dealer), 'win')
    
    def test_dealer_wins(self):
        player = Hand([Card('K', Suit.SPADES), Card('8', Suit.HEARTS)])
        dealer = Hand([Card('10', Suit.CLUBS), Card('9', Suit.DIAMONDS)])
        self.assertEqual(compare_hands(player, dealer), 'lose')
    
    def test_push(self):
        player = Hand([Card('K', Suit.SPADES), Card('9', Suit.HEARTS)])
        dealer = Hand([Card('10', Suit.CLUBS), Card('9', Suit.DIAMONDS)])
        self.assertEqual(compare_hands(player, dealer), 'push')
    
    def test_player_bust(self):
        player = Hand([Card('K', Suit.SPADES), Card('Q', Suit.HEARTS), Card('5', Suit.CLUBS)])
        dealer = Hand([Card('10', Suit.CLUBS), Card('9', Suit.DIAMONDS)])
        self.assertEqual(compare_hands(player, dealer), 'lose')
    
    def test_dealer_bust(self):
        player = Hand([Card('10', Suit.SPADES), Card('9', Suit.HEARTS)])
        dealer = Hand([Card('K', Suit.CLUBS), Card('Q', Suit.DIAMONDS), Card('5', Suit.CLUBS)])
        self.assertEqual(compare_hands(player, dealer), 'win')


class TestDeck(unittest.TestCase):
    """Test deck creation"""
    
    def test_deck_size(self):
        deck = create_deck()
        self.assertEqual(len(deck), 52)
    
    def test_deck_composition(self):
        deck = create_deck()
        ranks = set(card.rank for card in deck)
        suits = set(card.suit for card in deck)
        
        expected_ranks = {'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'}
        expected_suits = set(Suit)
        
        self.assertEqual(ranks, expected_ranks)
        self.assertEqual(suits, expected_suits)


if __name__ == '__main__':
    unittest.main()
