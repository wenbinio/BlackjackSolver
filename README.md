# Chinese New Year Blackjack Solver

A probability-based solver for a custom Chinese New Year blackjack variant that provides optimal play recommendations for every hand.

## Game Rules

This solver implements the following custom blackjack rules:

- **Deck**: 1 standard deck (52 cards)
- **Betting**: $2 per hand, ties push
- **Restrictions**: No splitting, no doubling, no free hit
- **Dealer Strategy**: Banker chooses freely, plays blind (doesn't see player hands), acts after all players

### Ace Valuation (Custom Rules)
- **2 cards**: Ace can be 1, 10, or 11
- **3 cards**: Ace can be 1 or 10
- **4+ cards**: Ace can only be 1

### Special Hands

| Hand | Payout |
|------|--------|
| Ban Ban (AA) | 3× |
| Blackjack (A + 10/J/Q/K) | 2× |
| Suited Blackjack | 3× |
| Triple 7s | 7× |
| 5-Card Charlie | 2× |

## Installation

No external dependencies required! This solver uses only Python standard library.

```bash
git clone https://github.com/wenbinio/BlackjackSolver.git
cd BlackjackSolver
```

## Usage

### Interactive Mode (Recommended)

Run the interactive solver to analyze your own hands:

```bash
python interactive_solver.py
```

This will prompt you to enter your cards and the dealer's upcard, then provide optimal strategy recommendations.

Example session:
```
Your cards: KS 6H
Dealer's card: 10C

OPTIMAL ACTION: HIT
Expected Value (Stand): -0.5803
Expected Value (Hit): -0.5404
```

### Demo Mode

Run the solver with example hands:

```bash
python solver.py
```

This will display optimal strategies for several example hands including special hands like Ban Ban, Blackjack, Triple 7s, and more.

### Use as a Module

```python
from solver import BlackjackSolver, Card, Suit

# Create solver
solver = BlackjackSolver()

# Define a hand
player_cards = [Card('K', Suit.SPADES), Card('6', Suit.HEARTS)]
dealer_upcard = Card('10', Suit.CLUBS)

# Get optimal strategy
result = solver.solve_hand(player_cards, dealer_upcard)

# Display recommendation
solver.print_strategy(result)
```

### Output Format

The solver provides:
- **Player Hand**: Your cards and their value(s)
- **Dealer Upcard**: Dealer's visible card
- **Special Hand**: Any special hand type detected
- **Payout Multiplier**: Potential payout for winning
- **Optimal Action**: Whether to HIT or STAND
- **Expected Values**: EV for both standing and hitting
- **Best EV**: The highest expected value

## Example Output

```
============================================================
Player Hand: Hand(10♠, 6♥)
Best Value: 16
Dealer Upcard: 10♣

Special Hand: None
Payout Multiplier: 1.0×

------------------------------------------------------------
OPTIMAL ACTION: HIT
Expected Value (Stand): -0.5803
Expected Value (Hit): -0.5404
Best EV: -0.5404
============================================================
```

## Testing

Run the unit tests to verify the implementation:

```bash
python -m unittest test_blackjack.py -v
```

All tests cover:
- Card and deck creation
- Special hand detection (Ban Ban, Blackjack, Triple 7s, 5-Card Charlie)
- Custom Ace valuation rules
- Hand comparison logic
- Payout calculations

## Architecture

The solver consists of three main modules:

1. **blackjack_game.py**: Core game logic
   - Card and Hand classes
   - Special hand detection
   - Ace valuation according to custom rules
   - Hand comparison and payout calculation

2. **probability_calculator.py**: Probability engine
   - Expected value calculations
   - Optimal dealer strategy simulation
   - Hit/Stand decision analysis

3. **solver.py**: Main interface
   - User-friendly solver interface
   - Strategy recommendation display
   - Example hand demonstrations

## Algorithm

The solver uses a recursive probability-based approach:

1. **Card Counting**: Tracks remaining cards in the deck
2. **Recursive EV Calculation**: Computes expected values for all possible outcomes
3. **Dealer Simulation**: Models optimal dealer play
4. **Strategy Recommendation**: Chooses action with highest expected value

The algorithm assumes optimal play from the dealer and calculates probabilities based on the remaining cards in the deck after accounting for known cards (player hand + dealer upcard).

## License

MIT License - See LICENSE file for details

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed usage examples including:
- Basic usage patterns
- All special hands (Ban Ban, Blackjack, Triple 7s, 5-Card Charlie)
- Custom Ace valuation examples
- Interactive mode examples
- Common game scenarios

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.