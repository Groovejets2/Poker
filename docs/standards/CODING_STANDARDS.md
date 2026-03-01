# Coding Standards - OpenClaw Poker Project

**Effective Date:** 2026-02-20
**Version:** 1.1

---

## Foundational Principles (Required Before Every Coding Session)

### KISS (Keep It Simple, Stupid)
- Favour simplicity over complexity
- Avoid over-engineering solutions
- Write code that is easy to understand
- If a simple solution exists, use it
- **Conflict Resolution:** When KISS conflicts with DRY, choose KISS first (simple code beats clever)

### YAGNI (You Aren't Gonna Need It)
- Do not add features until they are absolutely necessary
- Do not code for hypothetical future requirements
- Build only what is currently specified
- Refactor when actual requirements change
- **Application:** Write for Phase 2.2 requirements only; don't anticipate Phase 3 needs

### DRY (Don't Repeat Yourself)
- Extract common logic into reusable functions or classes
- Use abstraction to eliminate duplication
- Maintain a single source of truth for each piece of logic
- If you write similar code twice, refactor into a shared function
- **Related:** See DYC below

### DYC (Don't You Copy)
- Never copy-paste code (even if "just this once")
- Every copy creates a maintenance liability
- If code exists elsewhere, import or reuse it
- If reuse is difficult, refactor the original code
- **Example:** Copy-pasted validation logic in 2 places = bug in 2 places when updated

### SLAP (Single Level of Abstraction Principle)
- All code in a function should operate at the same level of abstraction
- Do not mix high-level logic with low-level implementation details
- **Example (Bad):**
  ```python
  def process_hand(cards):
      # High-level logic
      if len(cards) == 5:
          # Low-level bit manipulation mixed in
          value = cards[0].rank_value << 4 | cards[1].rank_value
      ...
  ```
- **Example (Good):**
  ```python
  def process_hand(cards):
      if is_valid_hand(cards):
          value = calculate_hand_value(cards)  # Abstracted
  ```

### SOC (Separation of Concerns)
- Each class/module should have a single, well-defined responsibility
- Do not mix unrelated functionality
- **Example:**
  - `HandEvaluator` — evaluates hands (no game logic)
  - `DealerEngine` — manages game flow (no hand evaluation)
  - `PotManager` — tracks pot (no game rules)

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

## Principle Conflict Resolution

When two standards or principles conflict, use this priority order (world-leading consensus):

1. **Safety & Correctness** (non-negotiable)
   - Prevents bugs and data loss
   - Example: Add error checking even if it adds complexity

2. **KISS** (simplicity)
   - Simple code is easier to debug and maintain
   - Example: Prefer simple loop over clever algorithm

3. **SOLID (SRP + SOC)** (separation of concerns)
   - Well-separated code prevents cascading failures
   - Example: Split a large class into smaller ones

4. **DRY** (eliminate duplication)
   - Once code is simple and separated, then eliminate duplication
   - Example: Extract common method after confirming pattern

5. **Performance** (last priority)
   - Only optimize after profiling shows bottleneck
   - "Premature optimization is the root of all evil" — Knuth

**Conflict Example:**
- **Scenario:** A function repeats 3 lines of validation. Do you extract to a helper (DRY) or keep it simple (KISS)?
- **Decision:** If it's 3 lines and the pattern is obvious, keep it simple. If it repeats in 5+ places, extract (DRY wins).
- **Rule:** Extract when the duplication becomes a maintenance burden, not on first occurrence.

---

## Pre-Coding Checklist

**MANDATORY: Read before starting any task**

- [ ] Have I read STANDARDS_MAP.md to find relevant standards?
- [ ] Have I read this CODING_STANDARDS.md?
- [ ] Have I identified which principles apply to this task?
- [ ] Have I anticipated any principle conflicts and decided resolution?
- [ ] Do I have clear test cases before writing code?
- [ ] Have I identified potential DRY/DYC opportunities (shared functions)?
- [ ] Have I verified the architecture/design before starting?

**If any checkbox fails:** Stop. Re-read or ask for clarification before coding.

---

## Python-Specific Standards

### Naming Conventions

#### Application-Level Naming (Packages & Modules)

**Packages:** lowercase, single word or hyphenated (directory structure)
```
poker_engine/          # Package directory
├── hand_evaluator.py  # Module file
├── dealer_engine.py
└── pot_manager.py
```

**Module Files:** lowercase with underscores, descriptive names
```
hand_evaluator.py      # What it does: evaluates hands
dealer_engine.py       # What it does: manages dealing
betting_validator.py   # What it does: validates bets
```

**Application Components:** PascalCase for app-level identifiers
```
class PokerApplication
class GameService
class PlayerRegistry
```

---

#### Class Naming

**Format:** PascalCase (no underscores)
```
class HandEvaluator:        # Describes what it evaluates
class DealerEngine:         # Describes what it manages
class PotManager:           # Describes what it manages
class BettingValidator:     # Describes what it validates
```

**Convention:** Noun-based names describing the object's responsibility
- ✓ `HandEvaluator` (what does it do? evaluate hands)
- ✓ `PotManager` (what does it do? manage pots)
- ✗ `ProcessHand` (this is a function, not a class)

---

#### Method & Function Naming

**Format:** lowercase with underscores (snake_case)

**Query Methods** (return data, no side effects):
```
def get_player_stack():      # Returns a value
def is_hand_valid():         # Returns boolean (question form)
def has_folded():            # Returns boolean (question form)
def calculate_pot_total():   # Returns calculated value
def find_winner():           # Returns result of search
```

**Command Methods** (perform action, may have side effects):
```
def post_blinds():           # Do something
def process_action():        # Do something
def update_game_state():     # Do something
def distribute_pot():        # Do something
```

**Constructor Methods:**
```
def __init__():              # Python constructor
def setup():                 # Initialization helper (if needed)
def initialize():            # Alternative init (less common)
```

**Conversion Methods:**
```
def to_dict():               # Convert to dictionary
def from_json():             # Create from JSON (class method)
def to_string():             # Convert to string (use __str__ instead)
```

**Pattern Examples:**
```python
# Good method naming (clear intent)
class Game:
    def get_current_player(self):        # What does it return?
    def is_game_active(self):            # Boolean question
    def process_player_action(self):     # What does it do?
    def calculate_hand_winner(self):     # What does it return?
    def fold_current_player(self):       # What does it do?

# Avoid (unclear intent)
class Game:
    def get(self):                       # Get what?
    def check(self):                     # Check what?
    def handle(self):                    # Handle what?
    def process(self):                   # Process what?
```

---

#### Variable Naming

**Local Variables:** lowercase with underscores, descriptive
```python
def process_hand(cards):
    hand_rank = evaluate_hand(cards)       # What is it? hand rank
    player_stack = player.stack            # What is it? player's stack
    total_pot = sum_pots()                 # What is it? total pot amount
    action_is_valid = validate_action()    # What is it? validity flag
```

**Instance Variables (Attributes):** lowercase with underscores, prefixed with `self.`
```python
class Player:
    def __init__(self, player_id, starting_stack):
        self.player_id = player_id              # WHO is this player?
        self.stack = starting_stack             # HOW MUCH do they have?
        self.hole_cards = []                    # WHAT cards do they have?
        self.is_active = True                   # ARE they still playing?
        self.current_bet = 0                    # HOW MUCH did they bet?
```

**Boolean Variables:** Prefix with `is_`, `has_`, `can_`, `should_`
```python
is_valid = True                    # Is it valid?
has_folded = False                 # Has it folded?
can_raise = True                   # Can it raise?
should_check = True                # Should it check?
is_all_in = False                  # Is it all-in?
```

**Loop Variables:** Single letter only for simple iterations; descriptive for complex ones
```python
# Simple iteration: OK to use single letter
for i in range(len(players)):
    players[i].update()

# Complex iteration: Use descriptive name
for player in players:
    for card in player.hole_cards:
        validate_card(card)
```

**Temporary/Scratch Variables:** Avoid. Use descriptive names instead.
```python
# Avoid
temp = calculate_value()
x = get_stack()
result = foo()

# Use
pot_total = calculate_pot_value()
player_stack = get_current_player_stack()
hand_rank = evaluate_hand(cards)
```

---

#### Constants Naming

**Format:** UPPERCASE with underscores, grouped logically
```python
# Game rules (what are the rules?)
MAX_PLAYERS = 8
MIN_BET = 1
BIG_BLIND = 20
SMALL_BLIND = 10

# Hand rankings (what are the ranks?)
HAND_RANK_ROYAL_FLUSH = 10
HAND_RANK_STRAIGHT_FLUSH = 9
HAND_RANK_FOUR_OF_A_KIND = 8

# Game states (what are the states?)
GAME_STATE_WAITING = "WAITING_PLAYERS"
GAME_STATE_BLINDS = "BLINDS_POSTED"
GAME_STATE_PRE_FLOP = "PRE_FLOP"
```

---

#### Private/Protected Naming

**Private Methods (class-internal only):** Single leading underscore
```python
def _validate_bet(self, amount):       # Not called externally
def _calculate_hand_rank(self):        # Helper, not public API
def _update_game_state(self):          # Internal update
```

**Private Variables (class-internal only):** Single leading underscore
```python
class Game:
    def __init__(self):
        self._current_player = None    # Internal state
        self._pot = 0                  # Internal state
        self._game_state = None        # Internal state
```

**Note:** Double leading underscore (`__`) is for name mangling. Avoid unless you have a specific reason.

---

#### Naming Anti-Patterns (Avoid These)

| Anti-Pattern | Bad Example | Good Example |
|--------------|-------------|--------------|
| **Abbreviations** | `calc_hand_val()` | `calculate_hand_value()` |
| **Single-letter vars** | `x = get_stack()` | `player_stack = get_current_player_stack()` |
| **Generic names** | `process()`, `handle()` | `process_player_action()`, `handle_fold()` |
| **Misleading names** | `get_value()` (what value?) | `get_pot_total()` |
| **Redundant prefixes** | `player_player_id` | `player_id` (already in Player class) |
| **Unclear booleans** | `active`, `checked` | `is_active`, `has_checked` |
| **Vague abbreviations** | `cur_act_plr` | `current_active_player` |

---

#### Naming Summary (Quick Reference)

| Item | Style | Example |
|------|-------|---------|
| Module/File | `lowercase_underscores` | `hand_evaluator.py` |
| Package | `lowercase` | `poker_engine/` |
| Class | `PascalCase` | `HandEvaluator` |
| Method/Function | `lowercase_underscores` | `evaluate_hand()` |
| Query Method | `get_*() / is_*() / has_*()` | `get_stack()`, `is_valid()` |
| Command Method | `verb_noun()` | `process_action()` |
| Variable | `lowercase_underscores` | `hand_rank` |
| Constant | `UPPERCASE_UNDERSCORES` | `MAX_PLAYERS` |
| Boolean Variable | `is_* / has_* / can_*` | `is_active`, `has_folded` |
| Private Method | `_lowercase_underscores` | `_validate_bet()` |
| Private Variable | `_lowercase_underscores` | `_internal_state` |

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

### Testing (NON-NEGOTIABLE)

#### Core Requirements

**MANDATORY: Every function/class must have unit tests before code is marked DONE.**

- All logic must have corresponding unit tests
- Use pytest as the testing framework
- Minimum 80% code coverage for core modules
- Test file naming: `test_<module_name>.py`
- Test function naming: `test_<function_name>_<scenario>`
- Tests must pass before submitting code for review

#### Test Coverage Standards

| Code Type | Minimum Coverage | Examples |
|-----------|------------------|----------|
| Core logic (hand evaluation, betting) | 90%+ | HandEvaluator, BettingValidator |
| Game state (dealer engine) | 85%+ | GameState, PlayerState |
| Utilities (helpers, converters) | 80%+ | CardConverter, PotCalculator |
| Integration tests | 70%+ | End-to-end game flow |

#### Test Structure

```python
def test_evaluate_hand_with_royal_flush():
    """Test that a royal flush is correctly identified as rank 10."""
    cards = [Card("hearts", "A"), Card("hearts", "K"), ...]
    result = evaluator.evaluate(cards)
    assert result["rank"] == 10
    assert result["name"] == "Royal Flush"

def test_evaluate_hand_with_low_pair():
    """Test that a pair is correctly ranked."""
    cards = [Card("hearts", "2"), Card("diamonds", "2"), ...]
    result = evaluator.evaluate(cards)
    assert result["rank"] == 9
```

#### Test Scenarios (Minimum)

For each function, test:
- **Happy path** — Normal input, expected output
- **Edge cases** — Boundary conditions (empty, max, min)
- **Error cases** — Invalid input, exceptions
- **Equivalence classes** — Groups of similar inputs

Example for `process_bet()`:
```python
# Happy path
test_process_bet_with_valid_raise()

# Edge cases
test_process_bet_with_minimum_bet()
test_process_bet_with_all_in()
test_process_bet_with_player_stack_boundary()

# Error cases
test_process_bet_with_amount_exceeding_stack()
test_process_bet_with_negative_amount()
test_process_bet_when_not_players_turn()
```

#### Context Window Management

**If writing tests would exceed context window limits:**

1. Write code first (Phase X.Y)
2. Create separate "test task" (Phase X.Y.1 or equivalent)
3. Run tests immediately after code, before marking DONE
4. Never skip tests to save tokens — move to separate task instead

Example:
```
Phase 2.2: Implement dealer engine (code + tests)
Phase 2.2.1: Write comprehensive test coverage (if needed separately)
```

**Important:** Code is NOT marked DONE until tests are written AND passing.

### Code Review Checklist

Before committing code:

- [ ] Code follows naming conventions
- [ ] No code duplication (DRY applied)
- [ ] Single responsibility per function/class
- [ ] All public functions documented
- [ ] **Unit tests written, comprehensive, and passing** ✓✓✓
- [ ] Test coverage >= minimum threshold (80%+)
- [ ] No hardcoded values (use constants)
- [ ] Error handling implemented and tested
- [ ] No TODO comments without context
- [ ] All tests run locally before commit

---

## TypeScript-Specific Standards (Backend + Frontend)

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Variables, functions | camelCase | `buyInChips`, `getActivePlayers()` |
| Classes, interfaces, types | PascalCase | `Tournament`, `PlayerState` |
| Enums | PascalCase (name), UPPER_SNAKE (members) | `enum Role { ADMIN, PLAYER }` |
| Constants | UPPER_SNAKE_CASE | `MAX_PLAYERS`, `DEFAULT_STACK` |
| File names | kebab-case | `auth.service.ts`, `tournament-card.tsx` |
| React components (files) | PascalCase | `TournamentCard.tsx`, `Layout.tsx` |
| Database columns | snake_case | `buy_in_chips`, `entry_fee_usd` |

### Type Safety

- **strict mode required** in all `tsconfig.json` files (`"strict": true`)
- Never use `any` without a justifying comment — prefer `unknown` and narrow
- Always type function parameters and return values explicitly for exported functions
- Use discriminated unions over optional fields where states are mutually exclusive:

```typescript
// BAD - ambiguous state
interface ApiResult {
  data?: Tournament[];
  error?: string;
  loading?: boolean;
}

// GOOD - discriminated union
type ApiResult =
  | { status: 'loading' }
  | { status: 'success'; data: Tournament[] }
  | { status: 'error'; error: string };
```

### Enums and Constants

- Use TypeScript `enum` for fixed sets of values shared across the codebase:

```typescript
// Prefer enums over string literals for status fields
enum TournamentStatus {
  SCHEDULED = 'scheduled',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

enum PlayerRole {
  ADMIN = 'admin',
  PLAYER = 'player',
}
```

- Use `as const` for simple value maps that don't need reverse lookup:

```typescript
const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  NOT_FOUND: 404,
} as const;
```

### API Layer Conventions

- Frontend service files must match the **actual backend response shape** (see AGENTS.md)
- Never assume wrapper objects — verify with `curl` first
- Type API responses at the service boundary, not in components:

```typescript
// Service layer types the response
async getAll(): Promise<Tournament[]> {
  const response = await apiClient.get<TournamentsListResponse>('/tournaments');
  return response.data.tournaments;
}

// Component receives clean typed data
const tournaments: Tournament[] = await tournamentsService.getAll();
```

### React / Frontend Patterns

- Use functional components exclusively (no class components)
- Prefer named exports over default exports for components
- Co-locate component tests in `__tests__/` with matching names
- Use React Context sparingly — only for truly global state (auth, theme)
- Keep components under 200 lines; extract sub-components when larger

### Import Order

Enforce consistent import ordering in all TypeScript files:

```typescript
// 1. React / framework imports
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// 2. Third-party libraries
import axios from 'axios';

// 3. Project services / utils
import { tournamentsService } from '../services/tournaments.service';

// 4. Project components
import { TournamentCard } from '../components/TournamentCard';

// 5. Types / interfaces (type-only imports)
import type { Tournament } from '../services/tournaments.service';
```

### Error Handling (TypeScript)

- Use typed error responses from the backend:

```typescript
interface ApiError {
  error: {
    code: string;
    message: string;
  };
}
```

- Catch Axios errors with type narrowing:

```typescript
try {
  await tournamentsService.create(data);
} catch (err) {
  if (axios.isAxiosError(err) && err.response) {
    const apiError = err.response.data as ApiError;
    setError(apiError.error.message);
  } else {
    setError('An unexpected error occurred');
  }
}
```

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

---

## Alignment with World-Leading Standards

This project follows principles adopted by:

- **Google** — SOLID, DRY, simplicity, testing culture
- **Amazon/AWS** — Separation of concerns, scalability-first design
- **Microsoft** — SOLID principles, design patterns
- **Python Community** — PEP 20 (Zen of Python), PEP 8 style guide
- **Netflix/Uber** — Microservices principles (SOC), failure resilience
- **Open Source (Linux, Django, FastAPI)** — Clean code, community standards

**Guiding Philosophy:**
Write code that a competent programmer who is not familiar with the project can understand in 5 minutes. This is the bar for "professional-grade" code.

---

**Document Created:** 2026-02-20 00:00 GMT+13
**Version:** 1.1 (Updated 2026-02-20 16:12 GMT+13)
**Status:** ACTIVE (Living Document)
