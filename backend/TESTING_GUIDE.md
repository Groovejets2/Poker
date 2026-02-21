# Phase 3.3 API Testing Guide

## Quick Start

### 1. Install Dependencies
```bash
cd backend
npm install
```

### 2. Seed Test Data
```bash
node scripts/seed-data.js
```

This creates:
- 5 test users (player1-player5, password: password123)
- 2 test tournaments (scheduled)
- Player registrations

### 3. Start Server
```bash
npm run dev
```

Server runs on `http://localhost:5000`

### 4. Import Postman Collection
- Open Postman
- Click "Import"
- Select `OpenClaw-Poker-API.postman_collection.json`
- Set `baseUrl` variable: `http://localhost:5000/api`

---

## Testing Workflow

### Step 1: Login
1. Go to **Authentication > Login**
2. Use credentials: `player1` / `password123`
3. Click Send
4. Token auto-saves to `{{token}}` variable (tests script)

### Step 2: List Tournaments
1. Go to **Tournaments > List Tournaments**
2. Click Send
3. See scheduled tournaments with player counts

### Step 3: Join Tournament
1. Go to **Tournaments > Register for Tournament**
2. Click Send (uses token from login)
3. Response shows seats available

### Step 4: View Tournament Details
1. Go to **Tournaments > Get Tournament**
2. Click Send
3. See all registered players

### Step 5: List Matches
1. Go to **Matches > List Tournament Matches**
2. Click Send
3. See matches (initially empty)

### Step 6: Submit Match Score
1. Go to **Matches > Submit Match Score**
2. Update match_id and player results in body
3. Click Send
4. Match marked as completed

### Step 7: View Leaderboard
1. Go to **Leaderboard > Global Leaderboard**
2. Click Send
3. See all players ranked by winnings

---

## API Endpoints Reference

### Auth
- `POST /auth/register` — Create account
- `POST /auth/login` — Login (returns JWT token)

### Tournaments
- `GET /tournaments` — List tournaments (paginated)
- `GET /tournaments/:id` — Tournament details + players
- `POST /tournaments/:id/register` — Join tournament (requires auth)
- `DELETE /tournaments/:id/unregister` — Leave tournament (requires auth)

### Matches
- `GET /matches/tournament/:tournament_id` — List matches in tournament
- `GET /matches/:id` — Match details + player results
- `POST /matches/:id/submit-score` — Submit match results (requires auth)

### Leaderboard
- `GET /leaderboard` — Global rankings (paginated)
- `GET /leaderboard/:user_id` — Player stats

### Health
- `GET /health` — Server status

---

## Test Users

All test users use password: `password123`

| Username | Email | ID |
|----------|-------|-----|
| player1 | player1@test.local | 1 |
| player2 | player2@test.local | 2 |
| player3 | player3@test.local | 3 |
| player4 | player4@test.local | 4 |
| player5 | player5@test.local | 5 |

---

## Common Errors & Fixes

### 401 Unauthorized
- **Cause:** Missing or invalid JWT token
- **Fix:** Login first, ensure Bearer token in header

### 404 Not Found
- **Cause:** Tournament/match ID doesn't exist
- **Fix:** Check ID in database (seed data creates IDs 1-2 for tournaments)

### 409 Conflict
- **Cause:** Already registered for tournament
- **Fix:** Unregister first, then register again

### 400 Invalid Request
- **Cause:** Missing required fields or invalid format
- **Fix:** Check request body against API spec

---

## Database Reset

To start fresh:
```bash
rm poker.db
npm run dev
node scripts/seed-data.js
```

---

**Status:** Ready for testing in Postman  
**Last Updated:** 2026-02-22
