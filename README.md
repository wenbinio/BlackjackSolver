# BlackjackSolver

Probability solver for a custom Chinese New Year blackjack variant:

- 1 deck, ties push
- No splitting, no doubling
- Dealer acts after player and chooses hit/stand to minimize player EV
- Ace values by hand size:
  - 2 cards: 1 / 10 / 11
  - 3 cards: 1 / 10
  - 4+ cards: 1
- Special hand multipliers (player payout on win):
  - Ban Ban (AA): 3x
  - Blackjack (A + 10/J/Q/K): 2x (suited: 3x)
  - Triple 7s: 7x
  - 5-Card Charlie: 2x

## Usage

Solve one starting hand:

```bash
python solver.py AS KH
```

Run all two-card starting hands (1326 combos):

```bash
python solver.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Build all-in-one Windows `.exe`

From Windows command prompt:

```bat
build_exe.bat
```

The executable is generated at:

```text
dist\BlackjackSolver.exe
```
