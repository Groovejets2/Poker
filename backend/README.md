# OpenClaw Poker Backend API

Express.js REST API for tournament management, matches, and leaderboard.

## Quick Start

### Installation

```bash
cd backend
npm install
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your settings
```

### Development

```bash
npm run dev
```

Server runs on `http://localhost:5000`

### Production

```bash
npm start
```

## API Endpoints

**Authentication:**
- `POST /api/auth/login` — Login user
- `POST /api/auth/register` — Create account

**Tournaments:**
- `GET /api/tournaments` — List tournaments
- `GET /api/tournaments/:id` — Tournament details
- `POST /api/tournaments` — Create tournament (admin)
- `POST /api/tournaments/:id/register` — Join tournament

**Matches:**
- `GET /api/tournaments/:tournament_id/matches` — List matches
- `GET /api/matches/:id` — Match details

**Leaderboard:**
- `GET /api/leaderboard` — Global rankings
- `GET /api/leaderboard/:user_id` — Player stats

## Testing

```bash
npm test
```

## Database

SQLite database located at `./poker.db` (configured in `.env`).

Schema auto-initializes on server start.

## Structure

```
src/
├── server.js           # Express app entry
├── database/
│   └── db.js           # Database connection & queries
├── routes/
│   ├── auth.js         # Authentication endpoints
│   ├── tournaments.js   # Tournament CRUD
│   ├── matches.js       # Match details
│   └── leaderboard.js   # Leaderboard & stats
└── middleware/
    ├── auth.js         # JWT authentication
    └── errorHandler.js # Global error handler
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 5000 | Server port |
| NODE_ENV | development | Environment |
| DB_PATH | ./poker.db | SQLite database path |
| JWT_SECRET | dev-secret-key | JWT signing key (change in prod!) |

---

**Phase 3.3 Implementation**  
Status: In Progress
