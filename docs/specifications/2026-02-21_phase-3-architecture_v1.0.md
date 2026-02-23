# Phase 3 Technology Stack & Architecture Specification

**Project:** OpenClaw Poker Platform  
**Component:** Platform Website & Backend Infrastructure  
**Document Created:** 2026-02-21 10:06 GMT+13  
**Version:** 1.0  
**Status:** DRAFT (awaiting Jon's approval)

---

## Purpose

This document specifies the technology stack, API design, and database schema for the OpenClaw Poker Platform website (Phase 3). It covers tournament management, leaderboard display, and match scheduling — excluding bot upload functionality (moved to backlog).

---

## Technology Stack Recommendations

### Backend Framework

**Recommended: Node.js + Express.js**

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Language | JavaScript/Node.js | Event-driven, non-blocking I/O; fast development |
| Framework | Express.js | Lightweight, battle-tested, minimal boilerplate |
| Database | SQLite (dev) / PostgreSQL (prod) | See section below |
| API Style | REST | Simple, cacheable, widely understood |
| Authentication | JWT tokens | Stateless, scalable, suitable for SPA+mobile |

**Alternative Considered: Python FastAPI**
- Pros: Single-language codebase (Python for both bots + backend)
- Cons: More overhead for simple CRUD operations
- **Rejected:** Node.js better for I/O-heavy web API

### Frontend Framework

**Recommended: React + TypeScript**

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Language | TypeScript | Type safety, better IDE support, fewer runtime bugs |
| Framework | React 18+ | Component-based, large ecosystem, performance |
| State Mgmt | Redux or Zustand | Centralized state for tournaments/leaderboard |
| Build Tool | Vite | Fast dev server, optimized builds |
| Styling | Tailwind CSS | Utility-first, rapid prototyping |

**Deployment:** Static files hosted on same server or CDN

### Database

**Development: SQLite3**
- File-based, zero setup required
- Suitable for single-table testing
- Connection string: `sqlite3:///poker.db`

**Production: PostgreSQL 13+**
- Horizontal scalability
- JSONB support for flexible match data
- Connection pooling via PgBouncer
- Backup and replication capabilities

**Migration:** Code uses ORM (TypeORM or Sequelize) → database-agnostic

---

## Database Schema

### Core Tables

#### `users` Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(32) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT username_length CHECK (LENGTH(username) >= 3)
);
```

#### `tournaments` Table
```sql
CREATE TABLE tournaments (
  id SERIAL PRIMARY KEY,
  name VARCHAR(128) NOT NULL,
  status ENUM('draft', 'scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'draft',
  buy_in_chips INT NOT NULL DEFAULT 10000,
  entry_fee_usd DECIMAL(8,2) NOT NULL DEFAULT 0.00,
  max_players INT NOT NULL DEFAULT 8,
  scheduled_at TIMESTAMP NOT NULL,
  created_by INT NOT NULL REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `tournament_players` Table
```sql
CREATE TABLE tournament_players (
  id SERIAL PRIMARY KEY,
  tournament_id INT NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status ENUM('registered', 'active', 'eliminated', 'withdrew') DEFAULT 'registered',
  starting_stack INT NOT NULL DEFAULT 10000,
  current_stack INT,
  finish_position INT,
  prize_usd DECIMAL(10,2),
  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(tournament_id, user_id)
);
```

#### `matches` Table
```sql
CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  tournament_id INT NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
  table_number INT NOT NULL,
  game_number INT NOT NULL,
  status ENUM('scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'scheduled',
  winner_id INT REFERENCES users(id),
  pot_total INT,
  scheduled_at TIMESTAMP,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  hand_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(tournament_id, table_number, game_number)
);
```

#### `match_players` Table
```sql
CREATE TABLE match_players (
  id SERIAL PRIMARY KEY,
  match_id INT NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  position INT NOT NULL,
  starting_stack INT NOT NULL,
  ending_stack INT,
  status ENUM('active', 'folded', 'eliminated', 'won') DEFAULT 'active',
  
  UNIQUE(match_id, user_id)
);
```

#### `leaderboard_view` (Materialized View)
```sql
CREATE MATERIALIZED VIEW leaderboard_view AS
SELECT 
  u.id,
  u.username,
  COUNT(DISTINCT t.id) AS tournaments_played,
  SUM(CASE WHEN tp.finish_position = 1 THEN 1 ELSE 0 END) AS tournament_wins,
  ROUND(AVG(CASE WHEN tp.finish_position IS NOT NULL THEN tp.finish_position ELSE NULL END)::numeric, 2) AS avg_finish,
  SUM(COALESCE(tp.prize_usd, 0)) AS total_winnings,
  ROW_NUMBER() OVER (ORDER BY SUM(COALESCE(tp.prize_usd, 0)) DESC) AS rank
FROM users u
LEFT JOIN tournament_players tp ON u.id = tp.user_id
LEFT JOIN tournaments t ON tp.tournament_id = t.id
WHERE t.status = 'completed'
GROUP BY u.id, u.username
ORDER BY rank;
```

---

## API Specification (REST)

### Authentication

**Endpoint:** `POST /api/auth/login`

Request:
```json
{
  "username": "player1",
  "password": "secret_password"
}
```

Response (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "player1",
  "expires_in": 3600
}
```

---

### Tournaments

**GET /api/tournaments** — List all tournaments

Query params:
- `status`: draft|scheduled|in_progress|completed (optional)
- `page`: pagination (default: 1)
- `limit`: per page (default: 20)

Response (200 OK):
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
  "total": 12,
  "page": 1,
  "limit": 20
}
```

---

**GET /api/tournaments/:id** — Get tournament details

Response (200 OK):
```json
{
  "id": 1,
  "name": "Saturday High Stakes",
  "status": "scheduled",
  "buy_in_chips": 10000,
  "entry_fee_usd": 5.00,
  "max_players": 8,
  "scheduled_at": "2026-02-21T14:00:00Z",
  "players": [
    {
      "user_id": 1,
      "username": "player1",
      "status": "registered",
      "starting_stack": 10000
    }
  ],
  "matches": [
    {
      "match_id": 101,
      "table_number": 1,
      "game_number": 1,
      "status": "completed",
      "winner": "player3"
    }
  ]
}
```

---

**POST /api/tournaments** — Create tournament (admin only)

Request:
```json
{
  "name": "Sunday Tournament",
  "buy_in_chips": 10000,
  "entry_fee_usd": 5.00,
  "max_players": 8,
  "scheduled_at": "2026-02-21T15:00:00Z"
}
```

Response (201 Created):
```json
{
  "id": 2,
  "name": "Sunday Tournament",
  "status": "draft",
  ...
}
```

---

**POST /api/tournaments/:id/register** — Join a tournament

Request:
```json
{
  "user_id": 1
}
```

Response (200 OK):
```json
{
  "success": true,
  "message": "Successfully registered",
  "tournament_id": 1,
  "player_count": 6
}
```

---

### Matches

**GET /api/tournaments/:id/matches** — List matches in a tournament

Response (200 OK):
```json
{
  "matches": [
    {
      "match_id": 101,
      "table_number": 1,
      "game_number": 1,
      "status": "completed",
      "winner": "player3",
      "pot_total": 40000,
      "hand_count": 15,
      "completed_at": "2026-02-21T14:45:30Z"
    }
  ]
}
```

---

**GET /api/matches/:id** — Get match details

Response (200 OK):
```json
{
  "match_id": 101,
  "tournament_id": 1,
  "table_number": 1,
  "status": "completed",
  "players": [
    {
      "user_id": 1,
      "username": "player1",
      "starting_stack": 10000,
      "ending_stack": 5000,
      "status": "eliminated"
    },
    {
      "user_id": 3,
      "username": "player3",
      "starting_stack": 10000,
      "ending_stack": 35000,
      "status": "won"
    }
  ],
  "pot_total": 40000,
  "hand_count": 15
}
```

---

### Leaderboard

**GET /api/leaderboard** — Get global leaderboard

Query params:
- `limit`: top N players (default: 50)
- `offset`: pagination (default: 0)

Response (200 OK):
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 5,
      "username": "champion",
      "tournaments_played": 8,
      "tournament_wins": 2,
      "avg_finish": 2.5,
      "total_winnings": 150.00
    },
    {
      "rank": 2,
      "user_id": 2,
      "username": "steady_player",
      "tournaments_played": 12,
      "tournament_wins": 1,
      "avg_finish": 3.1,
      "total_winnings": 95.50
    }
  ],
  "total_players": 24,
  "updated_at": "2026-02-21T10:15:00Z"
}
```

---

**GET /api/leaderboard/:user_id** — Get player stats

Response (200 OK):
```json
{
  "user_id": 5,
  "username": "champion",
  "rank": 1,
  "tournaments_played": 8,
  "tournament_wins": 2,
  "avg_finish": 2.5,
  "total_winnings": 150.00,
  "recent_matches": [
    {
      "tournament": "Saturday Tournament",
      "finish_position": 1,
      "prize": 50.00,
      "date": "2026-02-21"
    }
  ]
}
```

---

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React)                  │
│    - Tournament Lobby                               │
│    - Leaderboard                                    │
│    - Match Details                                  │
└──────────────┬──────────────────────────────────────┘
               │ HTTPS/REST
┌──────────────▼──────────────────────────────────────┐
│             API Server (Express.js)                 │
│ ┌─────────────────────────────────────────────────┐ │
│ │  Routes                                         │ │
│ │  - /api/auth/* (login)                          │ │
│ │  - /api/tournaments/* (CRUD, register)          │ │
│ │  - /api/matches/* (details)                     │ │
│ │  - /api/leaderboard/* (stats, rankings)         │ │
│ └─────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────┐ │
│ │  Services                                       │ │
│ │  - TournamentService                            │ │
│ │  - MatchService                                 │ │
│ │  - LeaderboardService                           │ │
│ │  - AuthService                                  │ │
│ └─────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────┐ │
│ │  Middleware                                     │ │
│ │  - JWT authentication                           │ │
│ │  - Error handling                               │ │
│ │  - Logging                                      │ │
│ └─────────────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────────────┘
               │ SQL
┌──────────────▼──────────────────────────────────────┐
│    Database (SQLite/PostgreSQL)                     │
│    - users                                          │
│    - tournaments                                    │
│    - tournament_players                             │
│    - matches                                        │
│    - match_players                                  │
│    - leaderboard_view (materialized)                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│    Dealer Engine (Phase 2)                          │
│    - Receives: match_id, players, dealer state      │
│    - Executes: game flow, hand evaluation           │
│    - Reports: results to API → database             │
└─────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

### Development Environment
- **Frontend:** React dev server (localhost:3000)
- **Backend:** Express dev server (localhost:5000)
- **Database:** SQLite (poker.db)
- **File system:** Local machine

### Production Environment
- **Frontend:** Static files on CDN or same server
- **Backend:** Node.js on Ubuntu/Debian VPS
- **Database:** PostgreSQL with automated backups
- **Reverse Proxy:** Nginx (SSL termination, load balancing)
- **Process Manager:** PM2 (auto-restart, clustering)

---

## Integration Points

### Backend ↔ Dealer Engine
- **Trigger:** User clicks "Play Match" in tournament
- **Flow:**
  1. API creates match record with players
  2. Spawns dealer engine subprocess with match_id
  3. Dealer executes game flow
  4. Reports results back to API
  5. API updates match_players, tournaments, leaderboard

### API ↔ Database
- ORM: TypeORM (Node.js + TypeScript)
- **Migrations:** Managed via TypeORM CLI
- **Connection Pool:** 10 connections (configurable)

---

## Security Considerations

| Aspect | Approach |
|--------|----------|
| Authentication | JWT tokens (RS256 asymmetric signing) |
| Authorization | Role-based (admin, player, spectator) |
| Database | SQL injection prevention via ORM parameterization |
| HTTPS | Mandatory in production (Nginx SSL) |
| Password Storage | bcrypt with 12 salt rounds |
| API Rate Limiting | 100 requests/minute per IP |

---

## Performance Targets

| Metric | Target |
|--------|--------|
| API response time | <200 ms (p95) |
| Database query | <50 ms (p95) |
| Leaderboard refresh | <5 seconds (materialized view) |
| Frontend load time | <3 seconds (first paint) |

---

## Estimated Effort

| Task | Estimate | Tokens |
|------|----------|--------|
| 3.1 Architecture spec (this doc) | 0.5 hours | 200 |
| 3.2 Frontend (lobby + leaderboard) | 4 hours | 1000-1200 |
| 3.3 Backend (API + database) | 4 hours | 1000-1200 |
| Integration & testing | 2 hours | 400-500 |
| **Total Phase 3** | ~10 hours | ~2600-3100 tokens |

---

## Out of Scope (Phase 3)

- Bot upload interface
- Bot execution engine
- Real-time WebSocket updates (deferred)
- Mobile app (deferred)
- Payment processing (deferred)

---

## Next Steps

1. **Jon's Approval:** Review and approve this specification
2. **Proceed to 3.2:** Frontend implementation (React lobby + leaderboard)
3. **Proceed to 3.3:** Backend implementation (Express API + database)

---

**Status:** DRAFT (awaiting approval)  
**Author:** Angus Young  
**Date:** 2026-02-21  
**Version:** 1.0
