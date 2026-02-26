# OpenClaw Poker Platform - API Specification

**Document:** OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md
**Category:** specifications
**Purpose:** Complete API specification with locked JSON contracts
**Version:** 1.0
**Created:** 2026-02-26
**Owner:** Jon + Development Team
**Tags:** api, specification, contracts, endpoints, json-schema

---

## Document Status

**🔒 LOCKED SPECIFICATION**

This document defines the **immutable** API contract for the OpenClaw Poker Platform.
- **Backend MUST implement exactly as specified**
- **Frontend MUST consume exactly as specified**
- **No mapping layers allowed**
- **Changes require project owner approval**

**Related Documents:**
- **Field Naming Standard:** `docs/standards/API-FIELD-NAMING-GUIDE.md`
- **Setup Guide:** `docs/documentation/SETUP-GUIDE.md`

---

## Table of Contents

1. [Base Information](#base-information)
2. [Authentication](#authentication)
3. [Field Naming Conventions](#field-naming-conventions)
4. [API Endpoints](#api-endpoints)
   - [Health Check](#health-check)
   - [Authentication Endpoints](#authentication-endpoints)
   - [Tournament Endpoints](#tournament-endpoints)
   - [Match Endpoints](#match-endpoints)
   - [Leaderboard Endpoints](#leaderboard-endpoints)
5. [Error Handling](#error-handling)
6. [Data Types](#data-types)
7. [Status Codes](#status-codes)

---

## Base Information

### Base URLs

**Local Development:**
```
http://localhost:5000
```

**Production (Future):**
```
https://api.openclaw-poker.com
```

### API Version
All endpoints use `/api/` prefix.
Current version: **v1.0**

### Content Type
All requests and responses use:
```
Content-Type: application/json
```

### Date Format
All timestamps use ISO 8601 format:
```
2026-02-26T10:00:00.000Z
```

---

## Authentication

### Authentication Method: JWT (JSON Web Tokens)

The API uses **JWT** for authentication, **NOT OAuth**.

**What's the difference?**
- **OAuth 2.0** - Full authorization framework for third-party apps (e.g., "Login with Google")
- **JWT** - Simpler token-based authentication (username/password → signed token)

**This API uses JWT** - simpler and sufficient for this use case.

### How Authentication Works

1. **Register** or **Login** to receive a JWT token
2. **Include token in all protected endpoints:**
   ```
   Authorization: Bearer <your-jwt-token>
   ```
3. **Token expires after 1 hour** - login again for new token

### Token Expiry
- **Duration:** 3600 seconds (1 hour)
- **After expiry:** Must login again for new token
- **No refresh tokens:** Must re-authenticate

---

## Field Naming Conventions

### 🔒 MANDATORY Standard

All fields use **descriptive snake_case with units**.

**Rules:**
- **Case:** Always `snake_case` (lowercase with underscores)
- **IDs:** Full entity name + `_id` (e.g., `user_id`, `tournament_id`)
- **Currency:** Include unit suffix (`_usd`, `_chips`)
- **Counts:** Descriptive plural or `_count` suffix
- **Booleans:** `is_` or `has_` prefix
- **Timestamps:** `_at` suffix, ISO 8601 format

**Examples:**
```json
{
  "user_id": 1,                    // ✅ Not "id"
  "buy_in_chips": 1000,            // ✅ Not "buy_in"
  "entry_fee_usd": 10,             // ✅ Not "entry_fee"
  "player_count": 5,               // ✅ Not "players"
  "tournament_wins": 3,            // ✅ Not "tournaments_won"
  "is_registered": true,           // ✅ Not "registered"
  "scheduled_at": "2026-02-26T..."  // ✅ Not "scheduled"
}
```

**❌ Forbidden Patterns:**
- `camelCase`, `PascalCase`, `kebab-case`
- Generic `id` (must be `user_id`, `tournament_id`, etc.)
- Fields without units (`buy_in` → must be `buy_in_chips`)
- Abbreviations (`usr_id` → must be `user_id`)

**Full Details:** See `docs/standards/API-FIELD-NAMING-GUIDE.md`

---

## API Endpoints

---

## Health Check

### GET /health

Check if the API is running.

**Authentication:** ❌ Not required

**Request:**
```http
GET http://localhost:5000/health
```

**Success Response (200 OK):**
```json
{
  "status": "ok",
  "message": "OpenClaw Poker API running"
}
```

**🔒 Locked Schema:**
```typescript
interface HealthResponse {
  status: "ok" | "error";
  message: string;
}
```

---

## Authentication Endpoints

---

### POST /api/auth/register

Create a new user account.

**Authentication:** ❌ Not required

**Request Body:**
```json
{
  "username": "string (required, 3-32 chars, alphanumeric + underscore)",
  "email": "string (optional, valid email format)",
  "password": "string (required, minimum 6 characters)"
}
```

**🔒 Locked Request Schema:**
```typescript
interface RegisterRequest {
  username: string;  // 3-32 chars, alphanumeric + underscore only
  email?: string;    // Valid email format
  password: string;  // Minimum 6 characters
}
```

**Example Request:**
```http
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "username": "player123",
  "email": "player@example.com",
  "password": "securepass123"
}
```

**Success Response (201 Created):**
```json
{
  "user_id": 1,
  "username": "player123",
  "message": "User created successfully"
}
```

**🔒 Locked Response Schema:**
```typescript
interface RegisterResponse {
  user_id: number;
  username: string;
  message: string;
}
```

**Error Responses:**

**400 Bad Request - Invalid Username:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Username: 3-32 chars, alphanumeric + underscore"
  }
}
```

**400 Bad Request - Invalid Password:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Password must be at least 6 characters"
  }
}
```

**409 Conflict - Duplicate Username/Email:**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "Username or email already exists"
  }
}
```

---

### POST /api/auth/login

Authenticate user and receive JWT token.

**Authentication:** ❌ Not required

**Request Body:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**🔒 Locked Request Schema:**
```typescript
interface LoginRequest {
  username: string;
  password: string;
}
```

**Example Request:**
```http
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "username": "player123",
  "password": "securepass123"
}
```

**Success Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "player123",
  "role": "player",
  "expires_in": 3600
}
```

**🔒 Locked Response Schema:**
```typescript
interface LoginResponse {
  token: string;         // JWT token
  user_id: number;       // User ID
  username: string;      // Username
  role: string;          // User role: "player" | "admin" | "moderator"
  expires_in: number;    // Token expiry in seconds (3600)
}
```

**Error Responses:**

**400 Bad Request - Missing Fields:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Username and password are required"
  }
}
```

**401 Unauthorized - Invalid Credentials:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid credentials"
  }
}
```

---

## Tournament Endpoints

---

### GET /api/tournaments

Get a paginated list of tournaments with optional filtering.

**Authentication:** ❌ Not required

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (1-indexed) |
| `limit` | integer | No | 20 | Results per page (max: 100) |
| `status` | string | No | - | Filter by status: `scheduled`, `in_progress`, `completed`, `cancelled` |

**Example Request:**
```http
GET http://localhost:5000/api/tournaments?status=scheduled&page=1&limit=20
```

**Success Response (200 OK):**
```json
{
  "tournaments": [
    {
      "id": 1,
      "name": "Friday Night Poker",
      "description": "Weekly Friday night tournament",
      "status": "scheduled",
      "buy_in_chips": 1000,
      "entry_fee_usd": 10,
      "max_players": 8,
      "player_count": 5,
      "seats_available": 3,
      "scheduled_at": "2026-02-28T19:00:00.000Z",
      "created_at": "2026-02-23T10:41:32.000Z",
      "updated_at": "2026-02-23T10:41:32.000Z",
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

**🔒 Locked Response Schema:**
```typescript
interface TournamentsListResponse {
  tournaments: Tournament[];
  pagination: Pagination;
}

interface Tournament {
  id: number;                    // Tournament ID (unique)
  name: string;                  // Tournament name
  description: string | null;    // Tournament description
  status: TournamentStatus;      // Current status
  buy_in_chips: number;          // Entry chips required
  entry_fee_usd: number;         // Entry fee in USD
  max_players: number;           // Maximum players allowed
  player_count: number;          // Current registered players
  seats_available: number;       // Remaining seats (max_players - player_count)
  scheduled_at: string;          // Start time (ISO 8601)
  created_at: string;            // Creation time (ISO 8601)
  updated_at: string;            // Last update time (ISO 8601)
  is_registered?: boolean;       // Current user registration status (if authenticated)
}

type TournamentStatus = "scheduled" | "in_progress" | "completed" | "cancelled";

interface Pagination {
  total: number;    // Total items available
  page: number;     // Current page (1-indexed)
  limit: number;    // Items per page
  pages: number;    // Total pages
}
```

**Error Responses:**

**400 Bad Request - Invalid Query Parameters:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid pagination parameters"
  }
}
```

---

### GET /api/tournaments/:id

Get detailed information about a specific tournament.

**Authentication:** ❌ Not required (registration status requires auth)

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Tournament ID |

**Example Request:**
```http
GET http://localhost:5000/api/tournaments/1
```

**Success Response (200 OK):**
```json
{
  "tournament": {
    "id": 1,
    "name": "Friday Night Poker",
    "description": "Weekly Friday night tournament",
    "status": "scheduled",
    "buy_in_chips": 1000,
    "entry_fee_usd": 10,
    "max_players": 8,
    "player_count": 5,
    "seats_available": 3,
    "scheduled_at": "2026-02-28T19:00:00.000Z",
    "created_at": "2026-02-23T10:41:32.000Z",
    "updated_at": "2026-02-23T10:41:32.000Z",
    "is_registered": false
  }
}
```

**🔒 Locked Response Schema:**
```typescript
interface TournamentDetailsResponse {
  tournament: Tournament;  // Same as Tournament interface above
}
```

**Error Responses:**

**404 Not Found - Tournament Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tournament not found"
  }
}
```

---

### POST /api/tournaments/:id/register

Register the authenticated user for a tournament.

**Authentication:** ✅ Required

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Tournament ID |

**Example Request:**
```http
POST http://localhost:5000/api/tournaments/1/register
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (201 Created):**
```json
{
  "message": "Successfully registered for tournament",
  "tournament_id": 1,
  "user_id": 5
}
```

**🔒 Locked Response Schema:**
```typescript
interface TournamentRegisterResponse {
  message: string;
  tournament_id: number;
  user_id: number;
}
```

**Error Responses:**

**401 Unauthorized - No Token:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

**404 Not Found - Tournament Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tournament not found"
  }
}
```

**400 Bad Request - Already Registered:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Already registered for this tournament"
  }
}
```

**400 Bad Request - Tournament Full:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Tournament is full"
  }
}
```

**400 Bad Request - Tournament Not Scheduled:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Can only register for scheduled tournaments"
  }
}
```

---

### DELETE /api/tournaments/:id/unregister

Unregister the authenticated user from a tournament.

**Authentication:** ✅ Required

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Tournament ID |

**Example Request:**
```http
DELETE http://localhost:5000/api/tournaments/1/unregister
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200 OK):**
```json
{
  "message": "Successfully unregistered from tournament",
  "tournament_id": 1,
  "user_id": 5
}
```

**🔒 Locked Response Schema:**
```typescript
interface TournamentUnregisterResponse {
  message: string;
  tournament_id: number;
  user_id: number;
}
```

**Error Responses:**

**401 Unauthorized - No Token:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

**404 Not Found - Tournament Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tournament not found"
  }
}
```

**400 Bad Request - Not Registered:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Not registered for this tournament"
  }
}
```

**400 Bad Request - Tournament Started:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Cannot unregister from tournament that has started"
  }
}
```

---

## Leaderboard Endpoints

---

### GET /api/leaderboard

Get the global leaderboard rankings.

**Authentication:** ❌ Not required

**Example Request:**
```http
GET http://localhost:5000/api/leaderboard
```

**Success Response (200 OK):**
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 5,
      "username": "player123",
      "tournaments_played": 25,
      "tournament_wins": 3,
      "avg_finish": 3.5,
      "total_winnings": 500
    },
    {
      "rank": 2,
      "user_id": 10,
      "username": "pokerpro",
      "tournaments_played": 20,
      "tournament_wins": 2,
      "avg_finish": 4.2,
      "total_winnings": 350
    }
  ],
  "updated_at": "2026-02-26T10:00:00.000Z"
}
```

**🔒 Locked Response Schema:**
```typescript
interface LeaderboardResponse {
  leaderboard: LeaderboardPlayer[];
  updated_at: string;  // ISO 8601 timestamp
}

interface LeaderboardPlayer {
  rank: number;                  // Rank position (1-indexed)
  user_id: number;               // Player's user ID
  username: string;              // Player's username
  tournaments_played: number;    // Total tournaments entered
  tournament_wins: number;       // Total tournament wins
  avg_finish: number | null;     // Average finish position (null if no tournaments)
  total_winnings: number;        // Total winnings in USD
}
```

---

### GET /api/leaderboard/:user_id

Get detailed statistics for a specific player.

**Authentication:** ❌ Not required

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | Yes | User ID |

**Example Request:**
```http
GET http://localhost:5000/api/leaderboard/5
```

**Success Response (200 OK):**
```json
{
  "player": {
    "user_id": 5,
    "username": "player123",
    "tournaments_played": 25,
    "tournament_wins": 3,
    "avg_finish": 3.5,
    "total_winnings": 500
  }
}
```

**🔒 Locked Response Schema:**
```typescript
interface PlayerStatsResponse {
  player: LeaderboardPlayer;  // Same as LeaderboardPlayer above
}
```

**Error Responses:**

**404 Not Found - User Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}
```

---

## Error Handling

### Error Response Format

All errors follow this consistent structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

**🔒 Locked Error Schema:**
```typescript
interface ErrorResponse {
  error: {
    code: string;     // Machine-readable error code
    message: string;  // Human-readable error message
  };
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Bad request - invalid input |
| `UNAUTHORIZED` | 401 | Authentication required or invalid token |
| `FORBIDDEN` | 403 | Authenticated but not authorized |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict (e.g., duplicate) |
| `INTERNAL_ERROR` | 500 | Internal server error |

---

## Data Types

### Status Enums

**TournamentStatus:**
```typescript
type TournamentStatus = "scheduled" | "in_progress" | "completed" | "cancelled";
```

**UserRole:**
```typescript
type UserRole = "player" | "admin" | "moderator";
```

### Field Types

| Field Pattern | Type | Format | Example |
|--------------|------|--------|---------|
| `*_id` | integer | Positive integer | `1`, `25`, `100` |
| `*_chips` | integer | Positive integer | `1000`, `5000` |
| `*_usd` | number | Decimal (2 places) | `10.00`, `25.50` |
| `*_count` | integer | Non-negative integer | `0`, `5`, `25` |
| `is_*` | boolean | true/false | `true`, `false` |
| `*_at` | string | ISO 8601 | `"2026-02-26T10:00:00.000Z"` |
| `*_wins` | integer | Non-negative integer | `0`, `3`, `10` |
| `avg_*` | number | Decimal or null | `3.5` or `null` |

---

## Status Codes

### HTTP Status Codes

| Code | Status | Usage |
|------|--------|-------|
| 200 | OK | Successful GET, DELETE |
| 201 | Created | Successful POST (resource created) |
| 400 | Bad Request | Invalid input, validation errors |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 500 | Internal Server Error | Server-side error |

---

## Change Log

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-02-26 | 1.0 | Sonnet 4.5 | Initial creation - locked JSON contracts with backend field names as standard |

---

## Version History

**v1.0 (2026-02-26)**
- Initial locked specification
- All endpoints documented with exact JSON schemas
- Field naming standard enforced
- Backend field names (`buy_in_chips`, `user_id`, etc.) established as standard

---

## Maintenance Notes

### Changing This Specification

**🔒 This is a LOCKED specification.**

**To make changes:**
1. Requires project owner (Jon) approval
2. Must update version number
3. Must update change log
4. Must update both backend AND frontend code
5. Must run full test suite
6. Must update all documentation

**No unilateral changes allowed.**

---

**Document:** OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md
**Version:** 1.0
**Status:** 🔒 LOCKED
**Last Updated:** 2026-02-26
**Owner:** Jon + Development Team

**This is the single source of truth for the OpenClaw Poker API.**
