# Phase 1: Bot Logic - Implementation Guide

**Status:** In Progress
**Target Completion:** Week of 2026-02-24

---

## What This Phase Delivers

- Hand Evaluator: Evaluates poker hands (5-card draw and Texas Hold'em)
- Card Representation: Card objects with suit and rank
- Unit Tests: Comprehensive test coverage for all logic
- No external dependencies: Pure Python

---

## Project Structure

```
poker_engine/
├── __init__.py          # Package initialisation
├── card.py              # Card class
├── hand_evaluator.py    # Hand ranking and evaluation logic
└── dealer_engine.py     # Placeholder for Phase 2

tests/
├── test_card.py         # Card tests
└── test_hand_evaluator.py # Hand evaluator tests

requirements.txt         # Python dependencies
```

---

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_hand_evaluator.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=poker_engine --cov-report=html
```

---

## Key Classes

### Card
Represents a playing card with suit (hearts, diamonds, clubs, spades) and rank (2-10, J, Q, K, A).

```python
from poker_engine.card import Card

card = Card("hearts", "A")
print(card)  # A of hearts
```

### HandEvaluator
Evaluates poker hands and ranks them.

```python
from poker_engine.hand_evaluator import HandEvaluator
from poker_engine.card import Card

evaluator = HandEvaluator()

cards = [
    Card("hearts", "A"),
    Card("spades", "A"),
    Card("diamonds", "K"),
    Card("clubs", "Q"),
    Card("hearts", "J"),
]

result = evaluator.evaluate(cards)
print(result['rank'])  # 2 (One Pair)
print(result['name'])  # "One Pair"
```

---

## Hand Rankings (Highest to Lowest)

1. Royal Flush (10-J-Q-K-A, same suit)
2. Straight Flush
3. Four of a Kind
4. Full House
5. Flush
6. Straight
7. Three of a Kind
8. Two Pair
9. One Pair
10. High Card

---

## Next Steps (Phase 2)

- Implement DealerEngine class
- Game state management
- Betting logic
- Pot calculation
- Winner determination

---

## Coding Standards

All code follows CODING_STANDARDS.md:
- KISS, YAGNI, DRY principles
- SOLID principles
- Python naming conventions
- Type hints where beneficial
- Comprehensive docstrings

---

## Git Workflow

Feature branches are prefixed with `feature/` and created from `develop`.

```bash
git checkout -b feature/2026-02-20_your-feature
# ... make commits ...
git push origin feature/2026-02-20_your-feature
# Create PR to develop
```

See GITFLOW.md for full details.

---

**Last Updated:** 2026-02-20 00:00 GMT+13
