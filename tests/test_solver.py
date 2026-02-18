import unittest

from solver import best_total, is_bust, solve_hand, special_multiplier


class SolverRuleTests(unittest.TestCase):
    def test_two_card_ace_can_be_eleven(self):
        self.assertEqual(best_total(("A", "9")), 20)

    def test_three_card_ace_cannot_be_eleven(self):
        self.assertEqual(best_total(("A", "9", "9")), 19)

    def test_four_card_ace_is_one_only(self):
        self.assertEqual(best_total(("A", "9", "9", "2")), 21)
        self.assertTrue(is_bust(("A", "10", "10", "2")))

    def test_special_multipliers(self):
        self.assertEqual(special_multiplier(("A", "A")), 3)
        self.assertEqual(special_multiplier(("A", "K"), suited_blackjack=False), 2)
        self.assertEqual(special_multiplier(("A", "K"), suited_blackjack=True), 3)
        self.assertEqual(special_multiplier(("7", "7", "7")), 7)
        self.assertEqual(special_multiplier(("2", "3", "4", "5", "6")), 2)

    def test_solver_returns_action_and_ev(self):
        result = solve_hand(("AS", "KH"))
        self.assertIn(result.best_action, {"hit", "stand"})
        self.assertIsInstance(result.expected_value, float)


if __name__ == "__main__":
    unittest.main()
