# Dealer Engine - Functional Requirements

**Project:** OpenClaw Poker Platform
**Component:** Dealer Engine (Phase 2)
**Document Created:** 2026-02-20 00:00 GMT+13
**Version:** 1.0
**Status:** APPROVED

---

## Purpose

This document specifies the functional requirements for the Dealer Engine, which manages all game flow, betting, pot management, and rules enforcement for poker games (5-card draw and Texas Hold'em).

---

## Scope

The Dealer Engine is responsible for:
- Managing game state and turn order
- Processing player actions (check, fold, raise, all-in, call)
- Managing the pot and side pots
- Tracking community cards (for Texas Hold'em)
- Determining winners and distributing pots
- Enforcing poker rules and bet constraints

The Dealer Engine does NOT handle:
- AI strategy decisions (that is the Bot Logic component)
- User interface or visualisation
- Network communication
- Database persistence

---

## Game State Model

### Game States
The dealer engine operates with the following game states:

1. **WAITING_FOR_PLAYERS** — Awaiting players to join
2. **GAME_STARTED** — All players seated, game beginning
3. **BLINDS_POSTED** — Small and big blinds have been posted
4. **PRE_FLOP** — First betting round (5-card draw or Texas Hold'em)
5. **FLOP** — Texas Hold'em only: 3 community cards revealed
6. **TURN** — Texas Hold'em only: 4th community card revealed
7. **RIVER** — Texas Hold'em only: 5th community card revealed
8. **SHOWDOWN** — All active players reveal hands
9. **POT_DISTRIBUTION** — Winner(s) determined, pot distributed
10. **HAND_COMPLETE** — Hand finished, next hand preparing

### Player States
Each player has a state within the current betting round:

1. **ACTIVE** — Player is still in the hand and may act
2. **FOLDED** — Player has folded; no longer eligible to win
3. **ALL_IN** — Player has gone all-in; cannot act further this hand
4. **WAITING_FOR_ACTION** — It is this player's turn to act
5. **ACTED** — Player has acted; waiting for others
6. **OUT_OF_HAND** — Player folded or went all-in; cannot win main pot

---

## Betting Rules

### Bet Types

1. **Check** — Pass action without betting (allowed if no bet to call)
2. **Fold** — Forfeit the hand and current bets
3. **Call** — Match the current bet amount
4. **Raise** — Increase the current bet (must be at least 2x the previous bet)
5. **All-In** — Bet all remaining chips

### Bet Constraints

- **Minimum Bet:** Must equal the big blind in the current betting round
- **Raise Minimum:** A raise must be at least equal to the previous bet increase
- **All-In Protection:** A player may go all-in for any amount, triggering potential side pots
- **No Negative Stacks:** A player cannot bet more chips than they have

### Betting Rounds

#### 5-Card Draw
1. **Pre-Draw Betting** — Antes or blinds, initial betting round
2. **Draw Phase** — Players discard and receive new cards (no betting)
3. **Post-Draw Betting** — Second betting round with new hands
4. **Showdown** — Remaining players reveal hands

#### Texas Hold'em
1. **Pre-Flop** — Blinds posted, initial betting round
2. **Flop** — 3 community cards revealed, betting round
3. **Turn** — 4th community card revealed, betting round
4. **River** — 5th community card revealed, final betting round
5. **Showdown** — Remaining players reveal hands

---

## Pot Management

### Pot Structure

- **Main Pot** — Created by the first player to bet (minimum bet from all players)
- **Side Pots** — Created when a player goes all-in with fewer chips than others

### Side Pot Example

```
Player A: Stack = 100 chips, bets 100 (all-in)
Player B: Stack = 500 chips, bets 200
Player C: Stack = 500 chips, bets 200

Main Pot: 100 × 3 = 300 chips (available to A, B, C)
Side Pot 1: 100 × 2 = 200 chips (available to B, C only; A cannot win)
```

### Pot Rules

- Each pot can only be won by players who contributed to it
- A player who goes all-in cannot win more than their contribution × number of contributors
- All remaining chips after the main pot contribution go to side pots
- Pots are evaluated separately for winner determination

---

## Action Order (Turn Management)

### Texas Hold'em Pre-Flop
1. Small blind posts (0.5 × big blind)
2. Big blind posts (standard bet)
3. Action begins to the left of big blind (UTG: Under The Gun)
4. Continues clockwise until all players have acted or folded

### Subsequent Rounds (Flop, Turn, River)
1. Small blind acts first (or next active player if folded)
2. Action proceeds clockwise
3. Continues until all active players have called or folded

### 5-Card Draw
1. After blinds, action begins left of big blind
2. Proceeds clockwise
3. Draw phase (no action)
4. Subsequent betting round follows dealer button clockwise

### Action Rules
- A player must act when it is their turn
- A player cannot act out of turn
- Action circle continues until only one player remains or all have called current bet
- If a player raises, action returns to the raiser's opponent
- The hand is invalid if no betting occurs in a round (should not happen in poker)

---

## Player Interface (Bot Communication)

### Input: Requesting a Player's Action

The dealer calls a bot with the following information:

```
{
    "player_id": "<unique_player_identifier>",
    "game_state": "PRE_FLOP|FLOP|TURN|RIVER",
    "hole_cards": [
        {"suit": "hearts", "rank": "A"},
        {"suit": "spades", "rank": "K"}
    ],
    "community_cards": [
        {"suit": "diamonds", "rank": "Q"},
        {"suit": "clubs", "rank": "J"},
        {"suit": "hearts", "rank": "10"}
    ],
    "current_bet": 50,
    "player_stack": 5000,
    "pot_total": 300,
    "table_state": [
        {
            "player_id": "player_1",
            "position": "dealer",
            "stack": 4500,
            "status": "ACTIVE",
            "current_bet": 50
        },
        ...
    ]
}
```

### Output: Player's Action Decision

The bot responds with:

```
{
    "action": "CALL|FOLD|RAISE|ALL_IN",
    "amount": 50
}
```

### Action Validation
- **CALL:** Amount must equal current_bet
- **FOLD:** Amount is ignored (set to 0)
- **RAISE:** Amount must be at least current_bet + minimum raise
- **ALL_IN:** Amount must be ≤ player_stack

---

## Winner Determination

### Hand Comparison
1. All remaining players (not folded) compare hands
2. Hand ranks are determined by the Hand Evaluator component
3. The highest-ranked hand wins

### Tie Resolution
- If two or more players have identical hand ranks, the pot is split evenly
- Remainder chips (if any) go to the earliest player in position order

### Side Pot Distribution
- Each side pot is evaluated separately
- A player who went all-in can only win up to their contribution per opponent

### All-Fold Scenario
- If all players fold except one, that player wins without showdown
- No cards are revealed

---

## Game Errors and Edge Cases

### Invalid Actions
- Player attempts to bet more than their stack → Error (reject action)
- Player attempts to act out of turn → Error (skip; allow next player)
- Player attempts to raise less than minimum → Error (reject action)
- Player attempts to call when no bet exists → Allow as check

### Edge Cases
- Only one player remains (all others folded) → That player wins immediately
- All players go all-in → All remaining cards revealed automatically
- Exact split pot (two players, equal hands) → Chips split 50/50
- Three-way tie → Pot divided three ways, remainder goes to earliest position

### State Consistency
- Game state must always be valid and consistent
- No player can have negative chips
- Total chips in play must equal sum of all player stacks plus pots
- No two players can have the same player_id

---

## Dealer Engine API Specifications

### Methods (High-Level Interface)

```
DealerEngine
├── __init__(game_type, players, blind_levels)
├── start_game()
├── start_hand()
├── request_player_action(player_id)
├── process_action(player_id, action, amount)
├── reveal_community_card(card)
├── advance_round()
├── determine_winners()
├── distribute_pot()
├── end_hand()
├── get_game_state()
├── get_player_state(player_id)
└── validate_action(player_id, action, amount)
```

### Data Structures

```
Card = {suit: str, rank: str}
PlayerAction = {action: str, amount: int}
PlayerStatus = {id: str, position: str, stack: int, status: str, bet: int}
GameState = {phase: str, players: [PlayerStatus], main_pot: int, side_pots: [int]}
```

---

## Testing Requirements

### Unit Tests
- Each method must have at least 3 test cases
- Test normal cases, edge cases, and error cases
- All tests must pass before code is merged

### Test Scenarios
- Betting validation (minimum bets, raises, all-in)
- Pot calculation with side pots
- Turn order with various player counts
- Showdown with ties
- Folding scenarios
- All-in protection

### Coverage Target
- Minimum 85% code coverage for dealer engine

---

## Non-Functional Requirements

### Performance
- Action request/response cycle < 100ms
- Pot calculation < 50ms
- Winner determination < 100ms
- Support 8+ concurrent players per table

### Reliability
- No data loss of game state
- Consistent game logic across all scenarios
- Clear error messages for debugging

### Maintainability
- Code follows CODING_STANDARDS.md
- All public methods documented
- Clear separation of concerns (SRP)
- DRY principle applied

---

## Out of Scope (Phase 2)

- Network communication
- Database persistence
- User interface or visualisation
- Tournament management
- Multiple tables
- Chat or social features
- Replay functionality

These will be addressed in Phase 3 (Platform Website) and beyond.

---

**Approval:** Jon (Project Lead)
**Next Step:** Implement Dealer Engine based on these specifications (Task 2.2)
