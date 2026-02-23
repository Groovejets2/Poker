# OpenClaw Poker API Specification

**OpenAPI Version:** 3.0.0  
**API Title:** OpenClaw Poker Platform API  
**Version:** 1.0.0  
**Description:** Tournament management, leaderboard, and match tracking API for OpenClaw Poker Platform  
**Base URL:** `https://api.openclaw-poker.local/api` (prod) | `http://localhost:5000/api` (dev)

---

## 1. Authentication

### Security Scheme: JWT Bearer Token

All protected endpoints require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Token obtained via POST `/auth/login` endpoint.

---

## 2. Paths

### 2.1 Authentication

#### POST /auth/login
**Summary:** User login  
**Tags:** Authentication  
**Security:** None (public endpoint)

**Request Body:**
```json
{
  "username": "string (3-32 chars, required)",
  "password": "string (required)"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Login successful, token returned |
| 400 | Invalid request (missing fields) |
| 401 | Invalid credentials |

**Response Body (200):**
```json
{
  "token": "string (JWT token)",
  "user_id": "integer",
  "username": "string",
  "expires_in": "integer (seconds)"
}
```

**Example:**
```
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "password": "secret"}'
```

---

### 2.2 Tournaments

#### GET /tournaments
**Summary:** List all tournaments  
**Tags:** Tournaments  
**Security:** Optional (public, but shows different data if authenticated)

**Query Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| status | string | No | Filter: draft, scheduled, in_progress, completed, cancelled |
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Results per page (default: 20, max: 100) |
| sort | string | No | Sort by: scheduled_at, created_at, player_count |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Success |
| 400 | Invalid query parameters |

**Response Body (200):**
```json
{
  "tournaments": [
    {
      "id": "integer",
      "name": "string",
      "status": "string (enum)",
      "buy_in_chips": "integer",
      "entry_fee_usd": "number (decimal)",
      "max_players": "integer",
      "scheduled_at": "string (ISO 8601 datetime)",
      "player_count": "integer",
      "seats_available": "integer",
      "created_by": "string (username)"
    }
  ],
  "pagination": {
    "total": "integer",
    "page": "integer",
    "limit": "integer",
    "pages": "integer"
  }
}
```

**Example:**
```
curl http://localhost:5000/api/tournaments?status=scheduled&limit=10
```

---

#### GET /tournaments/:id
**Summary:** Get tournament details  
**Tags:** Tournaments  
**Security:** Optional

**Path Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | integer | Yes | Tournament ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Success |
| 404 | Tournament not found |

**Response Body (200):**
```json
{
  "id": "integer",
  "name": "string",
  "description": "string (optional)",
  "status": "string (enum: draft, scheduled, in_progress, completed, cancelled)",
  "buy_in_chips": "integer",
  "entry_fee_usd": "number (decimal)",
  "max_players": "integer",
  "scheduled_at": "string (ISO 8601)",
  "created_by": "string (username)",
  "created_at": "string (ISO 8601)",
  "players": [
    {
      "user_id": "integer",
      "username": "string",
      "status": "string (registered, active, eliminated, withdrew)",
      "starting_stack": "integer",
      "current_stack": "integer (null if not started)",
      "joined_at": "string (ISO 8601)"
    }
  ],
  "matches": [
    {
      "match_id": "integer",
      "table_number": "integer",
      "game_number": "integer",
      "status": "string (scheduled, in_progress, completed, cancelled)",
      "winner": "string (username, null if not completed)",
      "pot_total": "integer",
      "hand_count": "integer"
    }
  ]
}
```

**Example:**
```
curl http://localhost:5000/api/tournaments/1
```

---

#### POST /tournaments
**Summary:** Create a new tournament (admin only)  
**Tags:** Tournaments  
**Security:** Required (JWT, admin role)

**Request Body:**
```json
{
  "name": "string (required, 3-128 chars)",
  "description": "string (optional)",
  "buy_in_chips": "integer (required, > 0)",
  "entry_fee_usd": "number (required, >= 0)",
  "max_players": "integer (required, 2-8)",
  "scheduled_at": "string (required, ISO 8601, future date)"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 201 | Tournament created successfully |
| 400 | Invalid request body |
| 401 | Unauthorized (not admin) |
| 403 | Forbidden |

**Response Body (201):**
```json
{
  "id": "integer",
  "name": "string",
  "status": "string (draft)",
  "buy_in_chips": "integer",
  "entry_fee_usd": "number",
  "max_players": "integer",
  "scheduled_at": "string",
  "created_by": "string",
  "created_at": "string"
}
```

**Example:**
```
curl -X POST http://localhost:5000/api/tournaments \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sunday Championship",
    "buy_in_chips": 10000,
    "entry_fee_usd": 5.00,
    "max_players": 8,
    "scheduled_at": "2026-02-23T14:00:00Z"
  }'
```

---

#### POST /tournaments/:id/register
**Summary:** Register a user for a tournament  
**Tags:** Tournaments  
**Security:** Required (JWT)

**Path Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | integer | Yes | Tournament ID |

**Request Body:**
```json
{
  "user_id": "integer (optional, defaults to authenticated user)"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Registered successfully |
| 400 | Invalid request (missing tournament, full, etc.) |
| 409 | User already registered |

**Response Body (200):**
```json
{
  "success": true,
  "message": "string",
  "tournament_id": "integer",
  "user_id": "integer",
  "player_count": "integer",
  "seats_available": "integer"
}
```

**Example:**
```
curl -X POST http://localhost:5000/api/tournaments/1/register \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

#### DELETE /tournaments/:id/unregister
**Summary:** Withdraw from a tournament  
**Tags:** Tournaments  
**Security:** Required (JWT)

**Path Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | integer | Yes | Tournament ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Unregistered successfully |
| 404 | Tournament or registration not found |

**Response Body (200):**
```json
{
  "success": true,
  "message": "string",
  "tournament_id": "integer",
  "user_id": "integer"
}
```

---

### 2.3 Matches

#### GET /tournaments/:tournament_id/matches
**Summary:** List all matches in a tournament  
**Tags:** Matches  
**Security:** Optional

**Path Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tournament_id | integer | Yes | Tournament ID |

**Query Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| status | string | No | Filter: scheduled, in_progress, completed, cancelled |
| table_number | integer | No | Filter by table |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Success |
| 404 | Tournament not found |

**Response Body (200):**
```json
{
  "tournament_id": "integer",
  "matches": [
    {
      "match_id": "integer",
      "table_number": "integer",
      "game_number": "integer",
      "status": "string",
      "winner": "string (username, null if not completed)",
      "pot_total": "integer",
      "hand_count": "integer",
      "started_at": "string (ISO 8601, null if not started)",
      "completed_at": "string (ISO 8601, null if not completed)"
    }
  ]
}
```

**Example:**
```
curl http://localhost:5000/api/tournaments/1/matches?status=completed
```

---

#### GET /matches/:id
**Summary:** Get detailed match information  
**Tags:** Matches  
**Security:** Optional

**Path Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | integer | Yes | Match ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Success |
| 404 | Match not found |

**Response Body (200):**
```json
{
  "match_id": "integer",
  "tournament_id": "integer",
  "table_number": "integer",
  "game_number": "integer",
  "status": "string",
  "players": [
    {
      "user_id": "integer",
      "username": "string",
      "position": "integer",
      "starting_stack": "integer",
      "ending_stack": "integer (null if ongoing)",
      "status": "string (active, folded, eliminated, won)"
    }
  ],
  "pot_total": "integer",
  "hand_count": "integer",
  "winner": "string (username)",
  "scheduled_at": "string (ISO 8601)",
  "started_at": "string (ISO 8601, null if not started)",
  "completed_at": "string (ISO 8601, null if not completed)"
}
```

**Example:**
```
curl http://localhost:5000/api/matches/101
```

---

### 2.4 Leaderboard

#### GET /leaderboard
**Summary:** Get global leaderboard rankings  
**Tags:** Leaderboard  
**Security:** Optional

**Query Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| limit | integer | No | Top N players (default: 50, max: 100) |
| offset | integer | No | Pagination offset (default: 0) |
| period | string | No | Time filter: all_time, this_month, this_week (default: all_time) |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Success |

**Response Body (200):**
```json
{
  "leaderboard": [
    {
      "rank": "integer",
      "user_id": "integer",
      "username": "string",
      "tournaments_played": "integer",
      "tournament_wins": "integer",
      "avg_finish": "number (decimal, 1-8)",
      "total_winnings": "number (USD)",
      "win_rate": "number (percentage)"
    }
  ],
  "total_players": "integer",
  "updated_at": "string (ISO 8601)",
  "period": "string"
}
```

**Example:**
```
curl 'http://localhost:5000/api/leaderboard?limit=25&period=this_month'
```

---

#### GET /leaderboard/:user_id
**Summary:** Get player statistics and ranking  
**Tags:** Leaderboard  
**Security:** Optional

**Path Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| user_id | integer | Yes | User ID |

**Responses:**

| Status | Description |
|--------|-------------|
| 200 | Success |
| 404 | User not found |

**Response Body (200):**
```json
{
  "user_id": "integer",
  "username": "string",
  "rank": "integer",
  "tournaments_played": "integer",
  "tournament_wins": "integer",
  "avg_finish": "number",
  "total_winnings": "number (USD)",
  "win_rate": "number (percentage)",
  "recent_matches": [
    {
      "tournament": "string (tournament name)",
      "tournament_id": "integer",
      "finish_position": "integer (1-8)",
      "prize": "number (USD)",
      "date": "string (ISO 8601)",
      "players_count": "integer"
    }
  ],
  "stats": {
    "avg_stack_at_elimination": "integer",
    "best_finish": "integer",
    "worst_finish": "integer"
  }
}
```

**Example:**
```
curl http://localhost:5000/api/leaderboard/5
```

---

## 3. Error Responses

All error responses follow this format:

```json
{
  "error": {
    "code": "string (ERROR_CODE)",
    "message": "string (human-readable)",
    "details": "object (optional, additional context)"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_REQUEST | 400 | Malformed request body or query parameters |
| UNAUTHORIZED | 401 | Missing or invalid JWT token |
| FORBIDDEN | 403 | Insufficient permissions (e.g., not admin) |
| NOT_FOUND | 404 | Resource does not exist |
| CONFLICT | 409 | Resource already exists (e.g., duplicate registration) |
| INTERNAL_ERROR | 500 | Server error |

**Example Error Response:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

---

## 4. Data Types

### Tournament Status
```
enum: ["draft", "scheduled", "in_progress", "completed", "cancelled"]
```

### Match Status
```
enum: ["scheduled", "in_progress", "completed", "cancelled"]
```

### Player Status (Tournament)
```
enum: ["registered", "active", "eliminated", "withdrew"]
```

### Player Status (Match)
```
enum: ["active", "folded", "eliminated", "won"]
```

---

## 5. Rate Limiting

All endpoints are rate limited to **100 requests per minute per IP address**.

Response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1645364400
```

---

## 6. Pagination

Endpoints that return lists support pagination via `page` and `limit` query parameters.

**Default values:**
- `page`: 1
- `limit`: 20
- `max_limit`: 100

**Response metadata:**
```json
{
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "pages": 8
  }
}
```

---

## 7. CORS

CORS is enabled for development.

**Allowed origins:**
- `http://localhost:3000` (React dev server)
- `https://openclaw-poker.local` (production domain)

---

## 8. Request/Response Examples

### Example 1: User Login

**Request:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "player1",
    "password": "mypassword"
  }'
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "player1",
  "expires_in": 3600
}
```

---

### Example 2: List Upcoming Tournaments

**Request:**
```bash
curl http://localhost:5000/api/tournaments?status=scheduled&limit=5
```

**Response (200 OK):**
```json
{
  "tournaments": [
    {
      "id": 1,
      "name": "Saturday High Stakes",
      "status": "scheduled",
      "buy_in_chips": 10000,
      "entry_fee_usd": 5.00,
      "max_players": 8,
      "scheduled_at": "2026-02-21T14:00:00Z",
      "player_count": 5,
      "seats_available": 3,
      "created_by": "admin"
    }
  ],
  "pagination": {
    "total": 2,
    "page": 1,
    "limit": 5,
    "pages": 1
  }
}
```

---

### Example 3: Register for Tournament

**Request:**
```bash
curl -X POST http://localhost:5000/api/tournaments/1/register \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully registered for tournament",
  "tournament_id": 1,
  "user_id": 1,
  "player_count": 6,
  "seats_available": 2
}
```

---

## 9. Implementation Notes

- All timestamps are in **ISO 8601 format** (UTC)
- All monetary amounts are in **USD** (decimal, 2 places)
- All numeric IDs are **positive integers**
- Stack sizes are in **chips** (integer)
- Usernames are **case-sensitive**, alphanumeric + underscore, 3-32 chars
- JWT tokens expire after **3600 seconds (1 hour)**

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-21  
**Status:** DRAFT (awaiting approval)
