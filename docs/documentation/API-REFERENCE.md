# API Reference

**Category:** documentation
**Purpose:** Complete API endpoint documentation and usage examples

**Status:** active
**Version:** 1.1
**Last Updated:** 2026-02-23 18:25 GMT+13
**Owner:** Angus + Sonnet 4.5
**Tags:** api, backend, endpoints, reference, authentication

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-23 18:25 | 1.1 | Sonnet 4.5 | Complete documentation with JWT auth flow, all endpoints, request/response examples, error codes |
| 2026-02-23 17:22 | 1.0 | Angus | Initial stub - TODO: auto-generate from OpenAPI spec |

---

## Base URL

**Local Development:**
```
http://localhost:5000
```

**Production:**
```
https://api.openclaw-poker.com (TBD)
```

---

## Authentication

### Important: JWT vs OAuth

The OpenClaw Poker API uses **JWT (JSON Web Tokens)** for authentication, **NOT OAuth**.

**What's the difference?**

- **OAuth 2.0** is a full authorization framework for third-party applications (e.g., "Login with Google")
- **JWT** is a simpler token-based authentication where you trade username/password for a signed token

**This API uses JWT**, which is simpler and sufficient for this use case.

### How to Get a JWT Token

**Step 1: Register a new account OR login with existing credentials**

**Option A - Register new account:**
```bash
POST http://localhost:5000/api/auth/register

Content-Type: application/json

{
  "username": "player123",
  "email": "player@example.com",
  "password": "mypassword123"
}
```

**Response (201 Created):**
```json
{
  "user_id": 1,
  "username": "player123",
  "message": "User created successfully"
}
```

**Option B - Login with existing account:**
```bash
POST http://localhost:5000/api/auth/login

Content-Type: application/json

{
  "username": "player123",
  "password": "mypassword123"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InBsYXllcjEyMyIsImlhdCI6MTYxNjE2MTYxNiwiZXhwIjoxNjE2MTY1MjE2fQ.5K9J3X...",
  "user_id": 1,
  "username": "player123",
  "expires_in": 3600
}
```

**Step 2: Use the token in subsequent requests**

For all protected endpoints, include the JWT token in the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InBsYXllcjEyMyIsImlhdCI6MTYxNjE2MTYxNiwiZXhwIjoxNjE2MTY1MjE2fQ.5K9J3X...
```

**Token Expiry:** Tokens expire after 1 hour (3600 seconds). After expiry, you must login again to get a new token.

---

## Endpoints

### Health Check

#### GET /health

Check if the API is running.

**Authentication:** Not required

**Request:**
```bash
GET http://localhost:5000/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "OpenClaw Poker API running"
}
```

---

## Authentication Endpoints

### Register User

#### POST /api/auth/register

Create a new user account.

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string (required, 3-32 chars, alphanumeric + underscore)",
  "email": "string (optional, valid email format)",
  "password": "string (required, minimum 6 characters)"
}
```

**Example Request:**
```bash
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

**Error Responses:**

**400 Bad Request - Invalid username:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Username: 3-32 chars, alphanumeric + underscore"
  }
}
```

**400 Bad Request - Invalid password:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Password must be at least 6 characters"
  }
}
```

**409 Conflict - Duplicate username/email:**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "Username or email already exists"
  }
}
```

---

### Login User

#### POST /api/auth/login

Authenticate user and receive JWT token.

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Example Request:**
```bash
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
  "expires_in": 3600
}
```

**Error Responses:**

**400 Bad Request - Missing fields:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Username and password are required"
  }
}
```

**401 Unauthorized - Invalid credentials:**
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

### List Tournaments

#### GET /api/tournaments

Get a paginated list of tournaments with optional filtering.

**Authentication:** Not required

**Query Parameters:**
- `page` (integer, optional, default: 1) - Page number
- `limit` (integer, optional, default: 20, max: 100) - Results per page
- `status` (string, optional) - Filter by status: `scheduled`, `in_progress`, `completed`, `cancelled`

**Example Request:**
```bash
GET http://localhost:5000/api/tournaments?status=scheduled&page=1&limit=20
```

**Success Response (200 OK):**
```json
{
  "tournaments": [
    {
      "id": 1,
      "name": "Friday Night Poker",
      "status": "scheduled",
      "buy_in_chips": 1000,
      "entry_fee_usd": 10.00,
      "max_players": 8,
      "scheduled_at": "2026-02-28T19:00:00.000Z",
      "created_at": "2026-02-23T05:00:00.000Z",
      "player_count": 5,
      "seats_available": 3
    }
  ],
  "pagination": {
    "total": 15,
    "page": 1,
    "limit": 20,
    "pages": 1
  }
}
```

---

### Get Tournament Details

#### GET /api/tournaments/:id

Get detailed information about a specific tournament including registered players.

**Authentication:** Not required

**Path Parameters:**
- `id` (integer, required) - Tournament ID

**Example Request:**
```bash
GET http://localhost:5000/api/tournaments/1
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Friday Night Poker",
  "status": "scheduled",
  "buy_in_chips": 1000,
  "entry_fee_usd": 10.00,
  "max_players": 8,
  "scheduled_at": "2026-02-28T19:00:00.000Z",
  "created_at": "2026-02-23T05:00:00.000Z",
  "created_by": {
    "id": 1,
    "username": "admin"
  },
  "players": [
    {
      "id": 1,
      "user_id": 2,
      "username": "player123",
      "starting_stack": 1000,
      "current_stack": 1000,
      "status": "active",
      "registered_at": "2026-02-23T10:00:00.000Z"
    }
  ]
}
```

**Error Response:**

**404 Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tournament not found"
  }
}
```

---

### Register for Tournament

#### POST /api/tournaments/:id/register

Register the authenticated user for a tournament.

**Authentication:** Required (JWT token)

**Path Parameters:**
- `id` (integer, required) - Tournament ID

**Example Request:**
```bash
POST http://localhost:5000/api/tournaments/1/register
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Registered for tournament",
  "tournament_id": 1,
  "user_id": 2,
  "player_count": 6,
  "seats_available": 2
}
```

**Error Responses:**

**401 Unauthorized - Missing/invalid token:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing authentication token"
  }
}
```

**404 Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Tournament not found"
  }
}
```

**409 Conflict - Already registered:**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "Already registered"
  }
}
```

**400 Bad Request - Tournament full:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Tournament full"
  }
}
```

---

### Unregister from Tournament

#### DELETE /api/tournaments/:id/unregister

Remove the authenticated user from a tournament.

**Authentication:** Required (JWT token)

**Path Parameters:**
- `id` (integer, required) - Tournament ID

**Example Request:**
```bash
DELETE http://localhost:5000/api/tournaments/1/unregister
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Unregistered from tournament",
  "tournament_id": 1,
  "user_id": 2
}
```

**Error Response:**

**404 Not Found - Not registered:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Registration not found"
  }
}
```

---

## Match Endpoints

### List Tournament Matches

#### GET /api/matches/tournament/:tournament_id

Get all matches for a specific tournament.

**Authentication:** Not required

**Path Parameters:**
- `tournament_id` (integer, required) - Tournament ID

**Example Request:**
```bash
GET http://localhost:5000/api/matches/tournament/1
```

**Success Response (200 OK):**
```json
{
  "tournament_id": 1,
  "matches": [
    {
      "id": 1,
      "table_number": 1,
      "game_number": 1,
      "status": "completed",
      "winner": "player123",
      "pot_total": 2000,
      "scheduled_at": "2026-02-28T19:00:00.000Z",
      "started_at": "2026-02-28T19:05:00.000Z",
      "completed_at": "2026-02-28T19:45:00.000Z",
      "hand_count": 25,
      "created_at": "2026-02-28T18:00:00.000Z"
    }
  ]
}
```

---

### Get Match Details

#### GET /api/matches/:id

Get detailed information about a specific match including players.

**Authentication:** Not required

**Path Parameters:**
- `id` (integer, required) - Match ID

**Example Request:**
```bash
GET http://localhost:5000/api/matches/1
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "table_number": 1,
  "game_number": 1,
  "status": "completed",
  "winner": "player123",
  "pot_total": 2000,
  "scheduled_at": "2026-02-28T19:00:00.000Z",
  "started_at": "2026-02-28T19:05:00.000Z",
  "completed_at": "2026-02-28T19:45:00.000Z",
  "hand_count": 25,
  "created_at": "2026-02-28T18:00:00.000Z",
  "players": [
    {
      "id": 1,
      "user_id": 2,
      "username": "player123",
      "position": 1,
      "starting_stack": 1000,
      "ending_stack": 2000,
      "status": "won"
    },
    {
      "id": 2,
      "user_id": 3,
      "username": "player456",
      "position": 2,
      "starting_stack": 1000,
      "ending_stack": 0,
      "status": "eliminated"
    }
  ]
}
```

**Error Response:**

**404 Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Match not found"
  }
}
```

---

### Submit Match Score

#### POST /api/matches/:id/submit-score

Submit final results for a completed match.

**Authentication:** Required (JWT token)

**Path Parameters:**
- `id` (integer, required) - Match ID

**Request Body:**
```json
{
  "winner_id": "integer (required) - User ID of winner",
  "results": [
    {
      "user_id": "integer (required)",
      "ending_stack": "integer (required)",
      "status": "string (required): 'won', 'eliminated', 'active'"
    }
  ]
}
```

**Example Request:**
```bash
POST http://localhost:5000/api/matches/1/submit-score
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "winner_id": 2,
  "results": [
    {
      "user_id": 2,
      "ending_stack": 2000,
      "status": "won"
    },
    {
      "user_id": 3,
      "ending_stack": 0,
      "status": "eliminated"
    }
  ]
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Match score submitted",
  "match_id": 1
}
```

**Error Responses:**

**400 Bad Request - Missing data:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing winner_id or results"
  }
}
```

**404 Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Match not found"
  }
}
```

---

## Leaderboard Endpoints

### Get Global Leaderboard

#### GET /api/leaderboard

Get global player rankings ordered by total winnings.

**Authentication:** Not required

**Query Parameters:**
- `limit` (integer, optional, default: 50, max: 100) - Number of results
- `offset` (integer, optional, default: 0) - Offset for pagination

**Example Request:**
```bash
GET http://localhost:5000/api/leaderboard?limit=50&offset=0
```

**Success Response (200 OK):**
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 5,
      "username": "pokerpro",
      "tournaments_played": 25,
      "tournament_wins": 8,
      "avg_finish": 2.5,
      "total_winnings": 5000.00
    },
    {
      "rank": 2,
      "user_id": 12,
      "username": "player123",
      "tournaments_played": 15,
      "tournament_wins": 3,
      "avg_finish": 3.2,
      "total_winnings": 2500.00
    }
  ],
  "updated_at": "2026-02-23T18:25:00.000Z"
}
```

---

### Get Player Stats

#### GET /api/leaderboard/:user_id

Get detailed statistics for a specific player.

**Authentication:** Not required

**Path Parameters:**
- `user_id` (integer, required) - User ID

**Example Request:**
```bash
GET http://localhost:5000/api/leaderboard/5
```

**Success Response (200 OK):**
```json
{
  "user_id": 5,
  "username": "pokerpro",
  "tournaments_played": 25,
  "tournament_wins": 8,
  "avg_finish": 2.5,
  "total_winnings": 5000.00
}
```

**Error Response:**

**404 Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found"
  }
}
```

---

## Error Codes

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

**Common Error Codes:**

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | INVALID_REQUEST | Invalid request parameters or body |
| 401 | UNAUTHORIZED | Missing or invalid authentication token |
| 404 | NOT_FOUND | Requested resource not found |
| 409 | CONFLICT | Resource conflict (e.g., duplicate username) |
| 429 | RATE_LIMIT_EXCEEDED | Too many requests (100 per minute limit) |
| 500 | INTERNAL_ERROR | Server error |

**Development Mode:** In development (NODE_ENV=development), error responses include a `details` field with the stack trace.

---

## Rate Limiting

The API enforces rate limiting to prevent abuse:

- **Limit:** 100 requests per minute per IP address
- **Response when exceeded:** HTTP 429 with message "Too many requests, please try again later"

---

## CORS Policy

The API accepts requests from the following origins:

**Development:**
- `http://localhost:3000`
- `https://openclaw-poker.local`

**Production:** (TBD)

---

## Testing with Postman

A Postman collection is available at:
```
backend/OpenClaw-Poker-API.postman_collection.json
```

**Import Instructions:**
1. Open Postman
2. Click "Import" button
3. Select the JSON file
4. All endpoints will be pre-configured

### How to Configure Postman for JWT Authentication

**Step-by-step guide:**

**1. Send a Login or Register Request**

First, create or login to an account:

- Select the `POST /api/auth/login` request (or `/api/auth/register` for new account)
- In the Body tab, enter your credentials:
  ```json
  {
    "username": "youruser",
    "password": "yourpass"
  }
  ```
- Click "Send"

**2. Copy the JWT Token from Response**

After successful login, you'll receive a response like:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InBsYXllcjEyMyIsImlhdCI6MTYxNjE2MTYxNiwiZXhwIjoxNjE2MTY1MjE2fQ.abc123...",
  "user_id": 1,
  "username": "youruser",
  "expires_in": 3600
}
```

Copy the entire `token` value (the long string starting with `eyJ...`)

**3. Configure Authorization for Protected Endpoints**

For any endpoint that requires authentication (marked with "Authentication: Required"):

**Option A - Set Authorization per request:**
1. Open the request (e.g., `POST /api/tournaments/:id/register`)
2. Go to the "Authorization" tab
3. Type: Select "Bearer Token"
4. Token: Paste your JWT token
5. Click "Send"

**Option B - Set Authorization for entire collection (recommended):**
1. Right-click the "OpenClaw Poker API" collection
2. Click "Edit"
3. Go to "Authorization" tab
4. Type: Select "Bearer Token"
5. Token: Paste your JWT token
6. Click "Update"
7. For individual requests, set Authorization to "Inherit auth from parent"

**4. Token Expiry**

JWT tokens expire after 1 hour (3600 seconds). When you get a 401 Unauthorized error, simply:
1. Re-send the login request
2. Copy the new token
3. Update your Postman authorization

**Note:** You do NOT configure OAuth 2.0 in Postman for this API. Use "Bearer Token" type only.

---

## Testing with curl

**Example: Register, Login, and Join Tournament**

```bash
# 1. Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# 2. Login and get token
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  | jq -r '.token')

# 3. Register for tournament
curl -X POST http://localhost:5000/api/tournaments/1/register \
  -H "Authorization: Bearer $TOKEN"
```

---

**Document Created:** 2026-02-23 17:22 GMT+13
**Last Updated:** 2026-02-23 18:25 GMT+13
**Version:** 1.1
**Status:** active
**Maintainer:** Angus Young + Sonnet 4.5
