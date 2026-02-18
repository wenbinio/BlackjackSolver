# Chinese New Year Blackjack Examples

This document provides examples of using the BlackjackSolver.

## Example 1: Basic Usage

```python
from solver import BlackjackSolver, Card, Suit

solver = BlackjackSolver()

# Create a hand: King and 6 (hard 16)
player_cards = [Card('K', Suit.SPADES), Card('6', Suit.HEARTS)]
dealer_upcard = Card('10', Suit.CLUBS)

# Get optimal strategy
result = solver.solve_hand(player_cards, dealer_upcard)
solver.print_strategy(result)
```

## Example 2: Special Hands

### Ban Ban (Pair of Aces)
```python
# Ban Ban automatically pays 3×
player_cards = [Card('A', Suit.SPADES), Card('A', Suit.HEARTS)]
dealer_upcard = Card('K', Suit.CLUBS)

result = solver.solve_hand(player_cards, dealer_upcard)
print(f"Special Hand: {result['special_hand']}")  # Ban Ban (3×)
print(f"Optimal Action: {result['optimal_action']}")  # stand
```

### Suited Blackjack
```python
# Suited blackjack pays 3×
player_cards = [Card('A', Suit.HEARTS), Card('Q', Suit.HEARTS)]
dealer_upcard = Card('9', Suit.CLUBS)

result = solver.solve_hand(player_cards, dealer_upcard)
print(f"Payout: {result['payout_multiplier']}×")  # 3.0×
```

### Triple 7s
```python
# Triple 7s pays 7×
player_cards = [
    Card('7', Suit.SPADES),
    Card('7', Suit.HEARTS),
    Card('7', Suit.CLUBS)
]
dealer_upcard = Card('10', Suit.DIAMONDS)

result = solver.solve_hand(player_cards, dealer_upcard)
print(f"Payout: {result['payout_multiplier']}×")  # 7.0×
```

### 5-Card Charlie
```python
# 5 cards without busting pays 2×
player_cards = [
    Card('2', Suit.SPADES),
    Card('3', Suit.HEARTS),
    Card('4', Suit.CLUBS),
    Card('5', Suit.DIAMONDS),
    Card('A', Suit.SPADES)
]
dealer_upcard = Card('K', Suit.CLUBS)

result = solver.solve_hand(player_cards, dealer_upcard)
print(f"Payout: {result['payout_multiplier']}×")  # 2.0×
```

## Example 3: Custom Ace Rules

### Two Cards - Ace can be 1, 10, or 11
```python
player_cards = [Card('A', Suit.SPADES), Card('7', Suit.HEARTS)]
dealer_upcard = Card('9', Suit.CLUBS)

result = solver.solve_hand(player_cards, dealer_upcard)
print(f"Possible values: {result['possible_values']}")  # [8, 17, 18]
print(f"Best value: {result['player_value']}")  # 18
```

### Three Cards - Ace can be 1 or 10
```python
player_cards = [
    Card('A', Suit.SPADES),
    Card('5', Suit.HEARTS),
    Card('3', Suit.CLUBS)
]
dealer_upcard = Card('6', Suit.DIAMONDS)

result = solver.solve_hand(player_cards, dealer_upcard)
print(f"Possible values: {result['possible_values']}")  # [9, 18]
```

### Four+ Cards - Ace can only be 1
```python
player_cards = [
    Card('A', Suit.SPADES),
    Card('5', Suit.HEARTS),
    Card('3', Suit.CLUBS),
    Card('4', Suit.DIAMONDS)
]
dealer_upcard = Card('7', Suit.CLUBS)

result = solver.solve_hand(player_cards, dealer_upcard)
print(f"Possible values: {result['possible_values']}")  # [13]
```

## Example 4: Interactive Mode

Run the interactive solver:
```bash
python interactive_solver.py
```

Example session:
```
Your cards: AS KH
Dealer's card: 9D

OPTIMAL ACTION: STAND
Expected Value (Stand): 2.0
Expected Value (Hit): -0.5
Best EV: 2.0
Special Hand: Blackjack (2×)
```

## Example 5: Strategy Chart

Generate a basic strategy chart:
```bash
python strategy_chart.py
```

This displays optimal actions for various hand totals against all dealer upcards.

## Tips

1. **Always check for special hands** - They provide bonus payouts
2. **Consider the 5-Card Charlie** - Sometimes hitting low hands is better to reach 5 cards
3. **Remember the Ace rules** - They change based on card count
4. **Ban Ban is powerful** - No need to split aces; you get 3× automatically!
5. **Use the interactive mode** - Great for learning the game strategy

## Common Scenarios

### Hard 16 vs Dealer 10
```python
# Classic difficult decision
player_cards = [Card('10', Suit.SPADES), Card('6', Suit.HEARTS)]
dealer_upcard = Card('10', Suit.CLUBS)

result = solver.solve_hand(player_cards, dealer_upcard)
# Solver will recommend the optimal action based on probability
```

### Soft 18 vs Dealer 9
```python
# Ace gives flexibility
player_cards = [Card('A', Suit.SPADES), Card('7', Suit.HEARTS)]
dealer_upcard = Card('9', Suit.CLUBS)

result = solver.solve_hand(player_cards, dealer_upcard)
# Can treat as 8 or 18
```

### Low 4-Card Hand
```python
# Going for 5-Card Charlie
player_cards = [
    Card('2', Suit.SPADES),
    Card('3', Suit.HEARTS),
    Card('4', Suit.CLUBS),
    Card('5', Suit.DIAMONDS)
]
dealer_upcard = Card('10', Suit.CLUBS)

result = solver.solve_hand(player_cards, dealer_upcard)
# Hitting is often good to try for 5-Card Charlie
```
