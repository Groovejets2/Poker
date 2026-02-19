# Coding Standards - OpenClaw Poker Project

**Version:** 1.0
**Date:** 2026-02-19

---

## Core Principles

### KISS (Keep It Simple, Stupid)
Simplicity is the primary goal. Avoid unnecessary complexity. Code should be readable and maintainable by any developer on the team.

**Guidelines:**
- Write code for clarity first, performance second
- Avoid over-engineering solutions
- Use straightforward logic before clever tricks
- Break complex problems into smaller, simple parts

### YAGNI (You Aren't Gonna Need It)
Do not add functionality until it is absolutely necessary.

**Guidelines:**
- Implement only what the specification requires
- Do not anticipate future needs beyond the current task
- Remove dead code and unused features
- Ask: "Is this required for this task?" before writing it

### DRY (Don't Repeat Yourself)
Do not repeat code patterns. Use abstractions, functions, classes, and libraries to eliminate duplication.

**Guidelines:**
- Extract repeated logic into shared functions
- Create helper classes for common operations
- Reuse existing libraries before writing new code
- If you copy-paste code, refactor into a function

### SOLID Principles

#### SRP (Single Responsibility Principle)
A class or function should have one reason to change. Each module should do one thing well.

**Example:**
- Dealer class manages game flow
- Hand Evaluator class evaluates hands only
- Bot Decision class handles decision logic only

#### OCP (Open/Closed Principle)
Code should be open for extension but closed for modification.

**Example:**
- Use interfaces or base classes so new strategies can be added without changing existing code
- Plugin architecture for new betting strategies

#### LSP (Liskov Substitution Principle)
Subtypes must be substitutable for their base types without breaking functionality.

**Example:**
- If you create multiple bot types, they should all implement the same interface
- A subclass should not break the contract of its parent class

#### ISP (Interface Segregation Principle)
Clients should not depend on interfaces they do not use. Keep interfaces focused and small.

**Example:**
- Do not force a bot to implement methods it does not need
- Separate interfaces for different concerns (decision-making, logging, etc.)

#### DIP (Dependency Inversion Principle)
Depend on abstractions, not concrete implementations.

**Example:**
- The dealer should depend on a Bot interface, not a specific bot class
- Use dependency injection where appropriate

---

## Code Style

### Python

**Naming Conventions:**
- Class names: PascalCase (e.g., `HandEvaluator`, `PokerDealer`)
- Function/method names: snake_case (e.g., `evaluate_hand`, `get_winner`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_PLAYERS`, `HAND_RANKS`)
- Private methods: prefix with single underscore (e.g., `_validate_hand`)

**Formatting:**
- Indentation: 4 spaces (never tabs)
- Line length: Maximum 100 characters
- Imports: Grouped (stdlib, third-party, local); one import per line
- Docstrings: Google-style for all classes and public methods

**Example:**
```python
class HandEvaluator:
    """Evaluates poker hands and compares them."""
    
    MAX_HAND_SIZE = 5
    
    def evaluate_hand(self, cards):
        """Evaluate hand value.
        
        Args:
            cards: List of Card objects
            
        Returns:
            int: Hand rank value
        """
        return self._calculate_rank(cards)
    
    def _calculate_rank(self, cards):
        """Private method to calculate hand rank."""
        pass
```

### Git Commits

**Format:** `[CATEGORY] Brief description`

**Categories:**
- `FEAT`: New feature
- `FIX`: Bug fix
- `REFACTOR`: Code restructure without feature change
- `TEST`: Test additions or modifications
- `DOCS`: Documentation changes
- `CHORE`: Build, config, or tooling changes

**Examples:**
```
FEAT: Add hand evaluation engine
FIX: Correct kicker comparison in high card hands
TEST: Add unit tests for flush detection
DOCS: Add docstrings to HandEvaluator class
```

**Commit Guidelines:**
- Commits should be atomic (single logical change)
- Commit frequently (every 30 minutes to 1 hour)
- Write clear, descriptive messages
- Reference task ID if applicable (e.g., `FEAT: Task 1.1 - Hand evaluation`)

---

## Testing

**Framework:** pytest

**Standards:**
- All public methods must have unit tests
- Test file naming: `test_<module_name>.py`
- Test function naming: `test_<functionality_being_tested>`
- Minimum 80% code coverage for core logic
- Run tests before every commit

**Example:**
```python
# test_hand_evaluator.py
import pytest
from hand_evaluator import HandEvaluator

class TestHandEvaluator:
    def setup_method(self):
        self.evaluator = HandEvaluator()
    
    def test_royal_flush_detection(self):
        """Test that royal flush is correctly identified."""
        cards = [Card(Suit.SPADES, Rank.ACE), ...]
        assert self.evaluator.evaluate_hand(cards) == HandRank.ROYAL_FLUSH
    
    def test_high_card_comparison(self):
        """Test high card comparison with kickers."""
        hand1 = [...]
        hand2 = [...]
        assert self.evaluator.compare(hand1, hand2) > 0
```

---

## Documentation

**Required Documentation:**
- Module docstring at the top of each file
- Class docstrings explaining purpose and usage
- Function docstrings with Args, Returns, Raises
- Complex logic: inline comments explaining why, not what
- README for each phase in code/ folder

**Example:**
```python
"""Hand evaluation module for poker games.

This module provides hand ranking and comparison logic for both
5-card draw and Texas Hold'em poker.
"""

class HandEvaluator:
    """Evaluates and ranks poker hands.
    
    Supports standard poker hand rankings from high card to royal flush.
    Handles both 5-card and 7-card hand evaluation.
    
    Attributes:
        hand_ranks: Dict mapping rank names to numeric values
    """
    
    def evaluate_hand(self, cards):
        """Determine the rank of a poker hand.
        
        Args:
            cards (list): List of 5 Card objects
            
        Returns:
            HandRank: Enum representing the hand's rank
            
        Raises:
            ValueError: If cards list is invalid
        """
```

---

## Code Review Checklist

Before committing code, verify:

- [ ] Does it follow KISS?
- [ ] No YAGNI violations (extra features)?
- [ ] No code duplication (DRY)?
- [ ] Each class has single responsibility (SRP)?
- [ ] Open for extension, closed for modification (OCP)?
- [ ] Code follows naming conventions?
- [ ] Line length under 100 characters?
- [ ] Unit tests written and passing?
- [ ] Docstrings complete?
- [ ] No commented-out code?
- [ ] Commit message follows format?

---

**Document Created:** 2026-02-19
**Version:** 1.0
**Status:** APPROVED
