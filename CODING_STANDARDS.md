# Coding Standards - OpenClaw Poker Project

**Effective Date:** 2026-02-20
**Version:** 1.0

---

## Core Principles

### KISS (Keep It Simple, Stupid)
- Favour simplicity over complexity
- Avoid over-engineering solutions
- Write code that is easy to understand
- If a simple solution exists, use it

### YAGNI (You Aren't Gonna Need It)
- Do not add features until they are absolutely necessary
- Do not code for hypothetical future requirements
- Build only what is currently specified
- Refactor when actual requirements change

### DRY (Don't Repeat Yourself)
- Extract common logic into reusable functions or classes
- Use abstraction to eliminate duplication
- Maintain a single source of truth for each piece of logic
- If you write similar code twice, refactor into a shared function

### SOLID Principles

#### SRP: Single Responsibility Principle
- A class or function should have exactly one reason to change
- Each module should do one thing and do it well
- Example: A Hand class evaluates poker hands. A Dealer class manages game flow. Not the same class.

#### OCP: Open/Closed Principle
- Code should be open for extension, closed for modification
- Use inheritance and composition to extend functionality
- Avoid changing existing code; add new code instead

#### LSP: Liskov Substitution Principle
- Subtypes must be substitutable for their parent types
- If a class inherits from another, it must not break the parent contract
- A derived class must fulfill the base class contract

#### ISP: Interface Segregation Principle
- Clients should not depend on methods they do not use
- Create focused, specific interfaces
- Do not force a class to implement methods it does not need

#### DIP: Dependency Inversion Principle
- Depend on abstractions, not concretions
- High-level modules should not depend on low-level modules
- Both should depend on abstractions (interfaces or abstract classes)

---

## Python-Specific Standards

### Naming Conventions

**Modules and Files:** lowercase with underscores
```
hand_evaluator.py
dealer_engine.py
pot_manager.py
```

**Classes:** PascalCase
```
class HandEvaluator:
class DealerEngine:
class PotManager:
```

**Functions and Methods:** lowercase with underscores
```
def evaluate_hand():
def manage_pot():
def determine_winner():
```

**Constants:** UPPERCASE with underscores
```
MAX_PLAYERS = 8
MIN_BET = 1
HAND_RANK_HIGH_CARD = 1
```

**Private Methods:** Leading underscore
```
def _calculate_hand_rank():
def _validate_bet():
```

### Code Style

- **Line Length:** Maximum 100 characters
- **Indentation:** 4 spaces (no tabs)
- **Imports:** Group standard library, third-party, then local imports
- **Docstrings:** Use triple quotes for all public functions and classes
- **Type Hints:** Use when clarity is improved (optional but encouraged)

### Documentation

Every public function must include a docstring:

```python
def evaluate_hand(cards):
    """
    Evaluate the rank and strength of a poker hand.
    
    Args:
        cards (list): List of Card objects representing the hand.
    
    Returns:
        dict: Dictionary containing rank, kickers, and strength value.
    
    Raises:
        ValueError: If cards list is not exactly 5 cards.
    """
```

### Testing

- All logic must have unit tests
- Use pytest as the testing framework
- Minimum 80% code coverage for core modules
- Test file naming: `test_<module_name>.py`
- Test function naming: `test_<function_name>_<scenario>`

Example:
```python
def test_evaluate_hand_with_royal_flush():
    """Test that a royal flush is correctly identified as rank 10."""

def test_evaluate_hand_with_low_pair():
    """Test that a pair is correctly ranked."""
```

### Code Review Checklist

Before committing code:

- [ ] Code follows naming conventions
- [ ] No code duplication (DRY applied)
- [ ] Single responsibility per function/class
- [ ] All public functions documented
- [ ] Unit tests written and passing
- [ ] No hardcoded values (use constants)
- [ ] Error handling implemented
- [ ] No TODO comments without context

---

## Error Handling

- Use specific exception types, not generic Exception
- Provide meaningful error messages
- Log errors at appropriate levels (debug, info, warning, error)
- Example:

```python
class InvalidHandError(Exception):
    """Raised when a hand does not contain exactly 5 cards."""

def evaluate_hand(cards):
    if len(cards) != 5:
        raise InvalidHandError(f"Expected 5 cards, got {len(cards)}")
```

---

## Logging

Use Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)

def evaluate_hand(cards):
    logger.debug(f"Evaluating hand with cards: {cards}")
    # ... code ...
    logger.info(f"Hand rank determined: {rank}")
```

Log levels:
- **DEBUG:** Detailed info for debugging
- **INFO:** General informational messages
- **WARNING:** Something unexpected but non-critical
- **ERROR:** An error occurred but the program continues
- **CRITICAL:** A severe error; program may not continue

---

## Performance Considerations

- Avoid nested loops where possible
- Cache results when appropriate
- Profile code before optimising
- Comment why an optimisation was necessary
- Example:

```python
# Cache hand ranks to avoid recalculating for the same cards
self._hand_cache = {}

def evaluate_hand(self, cards):
    key = tuple(cards)
    if key in self._hand_cache:
        return self._hand_cache[key]
    # ... calculate rank ...
    self._hand_cache[key] = result
    return result
```

---

## Collaboration

- Write code for readability first
- Future maintainers may not be familiar with your logic
- Use clear variable names: `player_stack` not `ps`
- Comment non-obvious decisions
- Ask for code review before merging

---

**Document Created:** 2026-02-20 00:00 GMT+13
**Version:** 1.0
**Status:** APPROVED
