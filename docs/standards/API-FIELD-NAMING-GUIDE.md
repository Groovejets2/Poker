# API Field Naming Guide

**Category:** standards
**Purpose:** Mandatory field naming conventions for all API endpoints
**Version:** 1.0
**Created:** 2026-02-26
**Owner:** Jon + Development Team
**Tags:** api, naming-conventions, standards, field-names

---

## 🔒 LOCKED STANDARD - Do Not Deviate

This document defines the **immutable** field naming conventions for the OpenClaw Poker API.
**ALL endpoints MUST follow these rules. Frontend MUST use these exact field names.**

---

## Core Naming Philosophy

### Chosen Style: **Descriptive Snake Case with Units**

**Format:** `{entity}_{attribute}_{unit}`

**Examples:**
- `buy_in_chips` (not `buy_in`, not `buyIn`, not `buyin`)
- `entry_fee_usd` (not `entry_fee`, not `entryFee`)
- `user_id` (not `id`, not `userId`)
- `tournament_wins` (not `wins`, not `tournaments_won`)

### Why This Style?

1. **Clarity:** `buy_in_chips` is unambiguous - it's chips, not dollars
2. **No Currency Confusion:** `entry_fee_usd` is explicit about USD
3. **Database Alignment:** Matches SQL column naming conventions
4. **Consistency:** All related fields follow same pattern
5. **Type Safety:** Unit suffixes prevent type confusion

---

## General Rules

### 1. Case Convention
- **✅ USE:** `snake_case` (lowercase with underscores)
- **❌ NEVER:** `camelCase`, `PascalCase`, `kebab-case`

**Examples:**
```json
{
  "user_id": 123,           // ✅ Correct
  "userId": 123,            // ❌ Wrong
  "UserID": 123,            // ❌ Wrong
  "user-id": 123            // ❌ Wrong
}
```

### 2. ID Fields
- **✅ USE:** Full entity name + `_id`
- **❌ NEVER:** Generic `id` alone

**Examples:**
```json
{
  "user_id": 1,             // ✅ Correct
  "tournament_id": 5,       // ✅ Correct
  "match_id": 10,           // ✅ Correct
  "id": 1                   // ❌ Wrong (ambiguous)
}
```

**Why:** When objects are embedded or joined, `user_id` is clear, `id` is not.

### 3. Currency/Money Fields
- **✅ USE:** Field name + `_usd` (or `_chips`)
- **❌ NEVER:** Generic `amount`, `value`, `cost`

**Examples:**
```json
{
  "entry_fee_usd": 10,      // ✅ Correct
  "buy_in_chips": 1000,     // ✅ Correct
  "total_winnings": 500,    // ✅ Correct (always USD)
  "fee": 10,                // ❌ Wrong (is it USD? Chips?)
  "buyin": 1000             // ❌ Wrong (no unit, no underscores)
}
```

### 4. Count/Quantity Fields
- **✅ USE:** Descriptive plural or `_count` suffix
- **❌ NEVER:** Abbreviations or ambiguous names

**Examples:**
```json
{
  "player_count": 5,        // ✅ Correct
  "max_players": 10,        // ✅ Correct
  "tournaments_played": 25, // ✅ Correct
  "tournament_wins": 3,     // ✅ Correct
  "players": 5,             // ❌ Ambiguous (count or list?)
  "plyr_cnt": 5             // ❌ Wrong (abbreviations)
}
```

### 5. Boolean Fields
- **✅ USE:** `is_` or `has_` prefix
- **❌ NEVER:** Bare adjectives

**Examples:**
```json
{
  "is_registered": true,    // ✅ Correct
  "is_active": false,       // ✅ Correct
  "has_started": true,      // ✅ Correct
  "registered": true,       // ❌ Wrong (not immediately clear it's boolean)
  "active": false           // ❌ Wrong
}
```

### 6. Date/Time Fields
- **✅ USE:** Past tense `_at` suffix for timestamps
- **✅ USE:** Present tense `_date` for dates
- **❌ NEVER:** Generic `date`, `time`

**Examples:**
```json
{
  "created_at": "2026-02-26T10:00:00Z",  // ✅ Correct
  "updated_at": "2026-02-26T10:05:00Z",  // ✅ Correct
  "scheduled_at": "2026-03-01T18:00:00Z", // ✅ Correct
  "start_date": "2026-03-01",            // ✅ Correct
  "date": "2026-03-01",                  // ❌ Wrong (which date?)
  "timestamp": 1645889400                // ❌ Wrong (use ISO 8601)
}
```

### 7. Average/Aggregate Fields
- **✅ USE:** `avg_` prefix, descriptive name
- **❌ NEVER:** Just `average`

**Examples:**
```json
{
  "avg_finish": 3.5,        // ✅ Correct
  "avg_score": 450,         // ✅ Correct
  "average": 3.5            // ❌ Wrong (average of what?)
}
```

---

## Field Name Dictionary

### Authentication Fields
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `user_id` | integer | Unique user identifier | `1` |
| `username` | string | User's chosen username | `"player123"` |
| `email` | string | User's email address | `"user@example.com"` |
| `password` | string | User's password (request only, never in response) | `"secret123"` |
| `token` | string | JWT authentication token | `"eyJhbGci..."` |
| `role` | string | User's role | `"player"`, `"admin"` |
| `expires_in` | integer | Token expiry in seconds | `3600` |

### Tournament Fields
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `tournament_id` | integer | Unique tournament identifier | `5` |
| `name` | string | Tournament name | `"Friday Night Poker"` |
| `description` | string | Tournament description | `"Weekly tournament"` |
| `status` | string | Tournament status | `"scheduled"`, `"in_progress"`, `"completed"` |
| `buy_in_chips` | integer | Entry chips required | `1000` |
| `entry_fee_usd` | number | Entry fee in USD | `10.00` |
| `max_players` | integer | Maximum players allowed | `8` |
| `player_count` | integer | Current registered players | `5` |
| `seats_available` | integer | Remaining seats | `3` |
| `scheduled_at` | string (ISO 8601) | Tournament start time | `"2026-02-28T19:00:00.000Z"` |
| `created_at` | string (ISO 8601) | Record creation time | `"2026-02-23T10:41:32.000Z"` |
| `updated_at` | string (ISO 8601) | Last update time | `"2026-02-23T10:41:32.000Z"` |
| `is_registered` | boolean | Current user registration status | `true`, `false` |

### Leaderboard Fields
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `rank` | integer | Player's rank position | `1` |
| `user_id` | integer | Player's user ID | `5` |
| `username` | string | Player's username | `"player123"` |
| `tournaments_played` | integer | Total tournaments entered | `25` |
| `tournament_wins` | integer | Total tournament wins | `3` |
| `avg_finish` | number (nullable) | Average finish position | `3.5` or `null` |
| `total_winnings` | number | Total winnings in USD | `500.00` |

### Match Fields
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `match_id` | integer | Unique match identifier | `10` |
| `tournament_id` | integer | Associated tournament | `5` |
| `match_number` | integer | Match sequence number | `1` |
| `table_number` | integer | Table assignment | `2` |
| `status` | string | Match status | `"pending"`, `"active"`, `"completed"` |
| `started_at` | string (ISO 8601) | Match start time | `"2026-02-28T19:15:00.000Z"` |
| `ended_at` | string (ISO 8601) | Match end time | `"2026-02-28T20:30:00.000Z"` |

### Pagination Fields
| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| `total` | integer | Total items available | `100` |
| `page` | integer | Current page number (1-indexed) | `1` |
| `limit` | integer | Items per page | `20` |
| `pages` | integer | Total pages available | `5` |

---

## Forbidden Patterns

### ❌ DO NOT USE These Patterns

1. **Abbreviations:**
   - ❌ `usr_id` → ✅ Use `user_id`
   - ❌ `trn_id` → ✅ Use `tournament_id`
   - ❌ `cnt` → ✅ Use `count` or `_count`

2. **Ambiguous Names:**
   - ❌ `id` → ✅ Use `user_id`, `tournament_id`, etc.
   - ❌ `amount` → ✅ Use `entry_fee_usd`, `buy_in_chips`
   - ❌ `count` → ✅ Use `player_count`, `tournament_count`

3. **CamelCase:**
   - ❌ `buyInChips` → ✅ Use `buy_in_chips`
   - ❌ `entryFeeUsd` → ✅ Use `entry_fee_usd`
   - ❌ `userId` → ✅ Use `user_id`

4. **Missing Units:**
   - ❌ `buy_in` → ✅ Use `buy_in_chips`
   - ❌ `entry_fee` → ✅ Use `entry_fee_usd`
   - ❌ `fee` → ✅ Use specific field name with unit

---

## Migration from Inconsistent Naming

### Previous Frontend Names (DEPRECATED)
| ❌ Old Name | ✅ New Name | Reason |
|------------|------------|---------|
| `buy_in` | `buy_in_chips` | Missing unit clarification |
| `entry_fee` | `entry_fee_usd` | Missing currency |
| `tournaments_won` | `tournament_wins` | Grammatical consistency |
| `id` | `user_id`, `tournament_id`, etc. | Ambiguity |
| `avg_finish_position` | `avg_finish` | Redundant (position implied) |

### Required Frontend Changes
All frontend code using deprecated names must be updated to use new standard names.
**No mapping layers allowed** - frontend must use backend field names exactly.

---

## Examples

### ✅ Good API Response
```json
{
  "tournaments": [
    {
      "tournament_id": 5,
      "name": "Friday Night Poker",
      "status": "scheduled",
      "buy_in_chips": 1000,
      "entry_fee_usd": 10,
      "max_players": 8,
      "player_count": 5,
      "seats_available": 3,
      "scheduled_at": "2026-02-28T19:00:00.000Z",
      "is_registered": false
    }
  ],
  "pagination": {
    "total": 10,
    "page": 1,
    "limit": 20,
    "pages": 1
  }
}
```

### ❌ Bad API Response
```json
{
  "tournaments": [
    {
      "id": 5,                    // ❌ Ambiguous
      "name": "Friday Night Poker",
      "buyIn": 1000,              // ❌ camelCase, missing unit
      "fee": 10,                  // ❌ Missing currency
      "maxPlayers": 8,            // ❌ camelCase
      "players": 5,               // ❌ Ambiguous (count or list?)
      "scheduled": "2026-02-28"   // ❌ Not ISO 8601, ambiguous field name
    }
  ]
}
```

---

## Enforcement

### Code Review Checklist
- [ ] All field names use `snake_case`
- [ ] ID fields include entity name (`user_id`, not `id`)
- [ ] Currency fields include unit (`_usd`, `_chips`)
- [ ] Count fields are descriptive (`player_count`, not `count`)
- [ ] Boolean fields use `is_` or `has_` prefix
- [ ] Timestamps use `_at` suffix and ISO 8601 format
- [ ] No abbreviations used
- [ ] No ambiguous generic names

### TypeScript Interface Enforcement
```typescript
// ✅ Correct interface
interface Tournament {
  tournament_id: number;
  name: string;
  buy_in_chips: number;
  entry_fee_usd: number;
  max_players: number;
  player_count: number;
  scheduled_at: string;
}

// ❌ Wrong interface
interface Tournament {
  id: number;              // Wrong - ambiguous
  buyIn: number;           // Wrong - camelCase, missing unit
  entryFee: number;        // Wrong - camelCase, missing unit
  maxPlayers: number;      // Wrong - camelCase
  players: number;         // Wrong - ambiguous
  scheduled: string;       // Wrong - ambiguous
}
```

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-26 | 1.0 | Initial creation - established backend naming as standard |

---

**Last Updated:** 2026-02-26
**Status:** 🔒 LOCKED - Changes require project owner approval

**This document is MANDATORY for all API development. Frontend MUST use these exact field names.**
