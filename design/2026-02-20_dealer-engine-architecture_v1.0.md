# Dealer Engine - Architecture Document

**Project:** OpenClaw Poker Platform
**Component:** Dealer Engine (Phase 2)
**Document Created:** 2026-02-20
**Version:** 1.0
**Status:** DRAFT (Awaiting Peer Review)

---

## Executive Summary

This document defines the architectural design of the Dealer Engine, focusing on game state management, concurrency handling, error resilience, and performance requirements. It bridges the gap between functional requirements (what the system does) and implementation (how it works).

---

## 1. System Overview

The Dealer Engine is responsible for:
- **Game orchestration** — Manage game lifecycle and turn order
- **State consistency** — Maintain valid game state across all operations
- **Betting management** — Validate and process player actions
- **Pot calculation** — Track main pot + side pots correctly
- **Winner determination** — Compare hands and distribute winnings
- **Error resilience** — Handle invalid inputs, bot failures, and edge cases

### Key Constraints
- Support 8 concurrent players per table
- No external dependencies (pure Python)
- Action response within 100ms
- Deterministic (same inputs = same outputs)
- Stateless between games (no persistent state required for Phase 2)

---

## 2. State Transition Architecture

### 2.1 Game State Diagram

```
DEALER ENGINE STATE FLOW
=========================

                    START_GAME
                        |
                        v
                  WAITING_PLAYERS
                  (seats filling)
                        |
                        v (all players seated)
                   BLINDS_POSTED
                        |
            +---TEXAS HOLD'EM---+---5-CARD DRAW---+
            |                   |                 |
            v                   v                 v
         PRE_FLOP           PRE_DRAW_BET      (players draw/discard)
            |                   |                 |
            v                   v                 v
          FLOP              POST_DRAW_BET       SHOWDOWN
            |                   |
            v                   |
          TURN                  |
            |                   |
            v                   |
          RIVER                 |
            |                   |
            +-------+           |
                    |           |
                    v           |
                 SHOWDOWN <-----+
                    |
                    v
               POT_DISTRIBUTE
                    |
                    v
               HAND_COMPLETE
                    |
                    v
               BLINDS_POSTED (next hand)
```

**Diagram Notes:**
- Texas Hold'em path: PRE_FLOP → FLOP → TURN → RIVER → SHOWDOWN
- 5-Card Draw path: PRE_DRAW_BET → (players draw) → POST_DRAW_BET → SHOWDOWN
- Both paths converge at SHOWDOWN
- All hands end with POT_DISTRIBUTE → HAND_COMPLETE

### 2.2 State Transition Rules

**TEXAS HOLD'EM PATH:**

| From State | To State | Trigger | Condition |
|------------|----------|---------|-----------|
| WAITING_PLAYERS | BLINDS_POSTED | Game start | All seats filled |
| BLINDS_POSTED | PRE_FLOP | Blinds valid | Small/big blind posted |
| PRE_FLOP | FLOP | All acted | Betting round complete |
| FLOP | TURN | All acted | Betting round complete |
| TURN | RIVER | All acted | Betting round complete |
| RIVER | SHOWDOWN | All acted | All bets final |

**5-CARD DRAW PATH:**

| From State | To State | Trigger | Condition |
|------------|----------|---------|-----------|
| BLINDS_POSTED | PRE_DRAW_BET | Blinds valid | Small/big blind posted |
| PRE_DRAW_BET | (Draw Phase) | All acted | First betting round complete |
| (Draw Phase) | POST_DRAW_BET | Players draw | Draw/discard complete |
| POST_DRAW_BET | SHOWDOWN | All acted | Second betting round complete |

**SHARED PATH (Both Game Types):**

| From State | To State | Trigger | Condition |
|------------|----------|---------|-----------|
| SHOWDOWN | POT_DISTRIBUTE | Winners determined | Hand comparison complete |
| POT_DISTRIBUTE | HAND_COMPLETE | Pots distributed | All chips awarded |
| HAND_COMPLETE | BLINDS_POSTED | Next hand | Dealer button rotates |

**Valid State Transitions:** Only transitions listed above are allowed. Any other state change is invalid.

**State Entry/Exit Rules:**
- Cannot skip states (e.g., FLOP → RIVER is invalid)
- All transitions are unidirectional (no reversals)
- All players must act before moving to next state
- One-way gate at SHOWDOWN (cannot return to betting)

---

## 3. Concurrency Model

### 3.1 Turn Order Architecture

The dealer engine enforces strict turn order to prevent race conditions:

```
TURN ORDER - 8 PLAYER TABLE
===========================

Seat Layout (Top-down view):
  
    Seat 0 (D - Dealer)        Seat 1 (SB - Small Blind)
           |                           |
           |                   Seat 2 (BB - Big Blind)
           |                           |
    Seat 7 +----------+--------+ Seat 3 (UTG - First to act pre-flop)
           |          |        |
        Seat 6     (CENTER)  Seat 4
           |          |        |
           +----------+--------+
                   Seat 5

ACTION ORDER (Clockwise around table):

PRE-FLOP (Blinds already posted):
1. Seat 3 (UTG - Under The Gun)       [first action]
2. Seat 4
3. Seat 5
4. Seat 6
5. Seat 7
6. Seat 0 (Dealer)
7. Seat 1 (Small Blind)
8. Seat 2 (Big Blind)                  [last action pre-flop]

POST-FLOP (FLOP, TURN, RIVER):
1. Seat 1 (Small Blind)                [first action]
2. Seat 2 (Big Blind)
3. Seat 3
4. Seat 4
5. Seat 5
6. Seat 6
7. Seat 7
8. Seat 0 (Dealer)                     [last action post-flop]

Turn Order Rules:
- Clockwise rotation from action button
- Folded players skipped
- All-in players skip (cannot act further)
- Sequence repeats until all players acted
```

### 3.2 Player State During Action

```
PLAYER STATE MACHINE (Single Player, Per Round)

                    ACTIVE (can act)
                        |
                 [Player must act]
                        |
         +------+-------+-------+
         |      |       |       |
         v      v       v       v
       CHECK  CALL    RAISE   FOLD
       FOLD            |
         |             v
         |          ALL_IN
         |             |
         +------+------+
                |
                v
          WAITING_FOR_OTHERS
                |
      [Betting round done]
                |
                v
          ACTIVE (next round OR Showdown)

State Rules:
- ACTIVE → ACTED (any action) → WAITING
- FOLDED → no further action (skip rest of hand)
- ALL_IN → no action this round (skip but still in pot)
- Cannot reverse state (no un-folding)
```

### 3.3 Action Lock Pattern

To prevent concurrent actions:

```python
# Pseudo-code
class DealerEngine:
    def __init__(self):
        self.action_lock = Lock()  # Mutex for action processing
        self.current_actor = None  # Only this player can act
    
    def request_action(self, player_id):
        # Only called when it's player_id's turn
        if self.current_actor is None:
            self.current_actor = player_id
        else:
            raise InvalidAction("Not this player's turn")
    
    def process_action(self, player_id, action):
        with self.action_lock:
            if self.current_actor != player_id:
                raise InvalidAction("Not your turn")
            # Process action
            self.current_actor = None  # Release turn
```

---

## 4. Error Handling & Resilience

### 4.1 Invalid Action Responses

```
BOT ACTION FLOW
===============

Bot sends action
      |
      v
Validation checks:
  - Is it this bot's turn?       [YES/NO]
  - Is action valid?             [YES/NO]
  - Is bet amount valid?         [YES/NO]
  - Did response arrive < 5s?    [YES/NO]
      |
      +---- YES to all -----> Process Action --> Update game state
      |
      +---- NO (invalid) ----> Log error --> Reject action --> Re-prompt
      |
      +---- NO (timeout) ----> Log timeout --> Auto-FOLD

Results:
- Valid action: Immediately processed
- Invalid action: Rejected, player re-prompted
- Timeout (>5s): Auto-fold to prevent deadlock
```

### 4.2 Error Categories & Handling

| Error | Cause | Response | Result |
|-------|-------|----------|--------|
| **Invalid Bet** | Bet > stack, raise < min | Reject, log | Player re-prompted |
| **Out of Turn** | Player acts when not turn | Skip, log | Next player acts |
| **Bot Timeout** | No response in 5s | Default to FOLD | Game continues |
| **Invalid Game State** | Unknown state | Log error, abort hand | Hand void, pots returned |
| **Concurrent Action** | Multiple players act simultaneously | Lock enforces order | Only first processed |

### 4.3 Logging Strategy

```
[TIMESTAMP] [GAME_ID] [ACTION] [DETAILS]

Examples:
[2026-02-20 15:30:45.123] [GAME_001] HAND_START | Players: 8, Blinds: 10/20
[2026-02-20 15:30:46.456] [GAME_001] ACTION | Player: 3, Action: RAISE, Amount: 50
[2026-02-20 15:30:47.789] [GAME_001] ERROR | Player: 5, Error: INVALID_BET, Details: 200 > stack 150
[2026-02-20 15:30:50.012] [GAME_001] POT_UPDATE | Main: 300, Side Pots: [150, 100]
[2026-02-20 15:30:52.345] [GAME_001] HAND_COMPLETE | Winner: Player 3, Amount: 550
```

---

## 5. Performance Specifications

### 5.1 Response Time SLAs

| Operation | Target | Measurement | Threshold |
|-----------|--------|-------------|-----------|
| **Action Request** | <100ms | Time from bot call to response receipt | 100ms max |
| **Action Validation** | <10ms | Time to validate action format + rules | 10ms max |
| **Pot Calculation** | <50ms | Time to compute main + all side pots | 50ms max |
| **Winner Determination** | <100ms | Time to compare hands + distribute | 100ms max |
| **State Transition** | <50ms | Time to update game state | 50ms max |

### 5.2 Performance Testing

```
Test Matrix:
- Player count: 2, 4, 6, 8 (measure scaling)
- Action complexity: Check, Call, Raise, All-in (measure variance)
- Iterations: 1000+ hands per scenario (measure consistency)

Success Criteria:
- 99th percentile response < SLA threshold
- No memory leaks (constant heap size)
- CPU usage < 50% on single core
```

---

## 6. Data Structures

### 6.1 Game State

```python
class GameState:
    game_id: str                    # Unique game identifier
    players: List[PlayerState]      # Array of 2-8 players
    current_phase: GamePhase        # BLINDS_POSTED, PRE_FLOP, etc.
    current_action_player: int      # Seat number of player to act
    main_pot: int                   # Chips in main pot
    side_pots: List[SidePot]       # Active side pots
    community_cards: List[Card]     # Texas Hold'em only
    dealer_button: int              # Seat number of dealer
    small_blind_amount: int         # SB value (e.g., 10)
    big_blind_amount: int           # BB value (e.g., 20)
    last_action_player: int         # For detecting all-acted state
```

### 6.2 Player State

```python
class PlayerState:
    player_id: str                  # Unique bot identifier
    seat_number: int                # 0-7
    stack: int                      # Chips remaining
    current_bet: int                # Chips bet this round
    hole_cards: List[Card]          # Private cards
    status: PlayerStatus            # ACTIVE, FOLDED, ALL_IN, WAITING
    round_status: RoundStatus       # ACTED, WAITING_FOR_ACTION
```

---

## 7. Security Considerations

### 7.1 Input Validation

All bot inputs are validated:
```
- Bet amount: Must be integer, ≥ 0, ≤ player stack
- Action type: Must be in {CHECK, FOLD, CALL, RAISE, ALL_IN}
- Player ID: Must match seated player
- Timing: Must be within action window (5s timeout)
```

### 7.2 Game Integrity

```
- Cards cannot be modified mid-hand
- Pots cannot be removed or reduced
- Fold is irreversible
- All-in is irreversible
- No player can see other players' hole cards
```

---

## 8. Implementation Roadmap

| Phase | Task | Complexity | Est. Hours |
|-------|------|-----------|-----------|
| 2.2 | Core state machine + action validation | High | 4-5 |
| 2.3 | Bot interface + integration | Medium | 2-3 |
| 2.4 | Multi-bot testing + stress | Medium | 2 |

---

## 9. Design Decisions & Rationale

### Decision 1: Strict Turn Order Enforcement
**Why:** Prevents race conditions. Only one player acts at a time.
**Alternative:** Concurrent actions with conflict resolution. *Rejected:* More complex, harder to debug.

### Decision 2: Main Pot + Side Pots Separately
**Why:** Handles all-in scenarios correctly. Player A (100 chips) can only win 100×N from others.
**Alternative:** Single pot with complex winner logic. *Rejected:* Error-prone, harder to verify.

### Decision 3: Stateless Between Games
**Why:** Simpler. Each game is independent. No persistent DB needed for Phase 2.
**Alternative:** Persistent state. *Rejected:* Adds complexity before Phase 3 (platform).

### Decision 4: Timeout → Auto-Fold
**Why:** Game cannot wait forever. 5s timeout is reasonable for testing.
**Alternative:** Infinite wait. *Rejected:* Would deadlock.

---

## 10. Open Questions & Assumptions

**Q1:** Should the dealer engine support pausing/resuming mid-hand?
**A1:** Assumption: No. Games run to completion. Simplifies state management.

**Q2:** What happens if a bot requests an invalid action multiple times?
**A2:** Assumption: Log error, treat as FOLD after 3 attempts. Prevents spam.

**Q3:** Can blind levels change mid-game?
**A3:** Assumption: No. Fixed for each game. Tournament structures (Phase 4+).

---

## Approval & Next Steps

**Status:** DRAFT - Self-reviewed by Angus Young

**Self-Review Checklist:**
- ✓ All functional requirements addressed
- ✓ Error scenarios covered
- ✓ Diagrams clear and accurate
- ✓ Performance SLAs measurable
- ✓ State transitions complete and valid
- ✓ Concurrency model prevents race conditions
- ✓ No contradictions with functional spec

**Ready for:** Jon's approval before Phase 2.2 implementation begins

---

**Document Version:** 1.0
**Last Updated:** 2026-02-20 15:12 GMT+13 (DRAFT)
**Author:** Angus Young
**Next Iteration:** Pending feedback
