# CLAUDE.md - Phase 3.3 TypeORM Refactor (Completion Guide)

**Category:** standards
**Purpose:** Operational guidelines and remaining work for Phase 3.3 completion for Opus 4.6
**Status:** active
**Version:** 1.0
**Last Updated:** 2026-02-23 17:28 GMT+13
**Owner:** Angus
**Tags:** operational, handoff, phase-3.3, typeorm

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-23 17:28 | 1.0 | Angus | Final version ready for handoff to Opus 4.6 |

---

## Documentation Navigation

All project documentation is in `docs/` folder:

```
docs/
├── INDEX.md                    (Start here - main entry point)
├── specifications/INDEX.md     (Architecture & design decisions)
│   ├── DEPLOYMENT_ARCHITECTURE.md  (Test/prod setup)
│   ├── PHASE-3-ARCHITECTURE.md     (Tech stack & API design)
│   └── PROJECT_CHARTER.md          (Vision & budget)
├── design/INDEX.md            (Work breakdown & planning)
│   ├── TASK-BOARD.md              (Current tasks & status)
│   └── PHASE-3-ARCHITECTURE.md     (Implementation details)
├── standards/INDEX.md         (Rules & guidelines)
│   ├── DOCUMENTATION_STANDARDS.md  (How to write docs)
│   └── SPENDING-TRACKER.md         (Budget tracking)
├── documentation/INDEX.md     (Operational guides)
│   ├── SETUP-GUIDE.md
│   ├── API-REFERENCE.md
│   ├── DEPLOYMENT-GUIDE.md
│   └── TROUBLESHOOTING.md
└── progress/                  (Daily session logs)
```

**To find any document:**
1. Go to docs/INDEX.md
2. Find your situation in "By Situation" or "By Role"
3. Follow links to relevant sub-index
4. Each sub-index has links to actual documents

---

## Operational Guidelines

1. **Read before coding:**
   - `docs/standards/DOCUMENTATION_STANDARDS.md` (how to structure docs)
   - `docs/standards/SPENDING-TRACKER.md` (budget: currently ~$5.06)
   - `docs/specifications/DEPLOYMENT_ARCHITECTURE.md` (test/prod switching)

2. **Code locations:**
   - Source: `backend/src/`
   - Entities: `backend/src/database/entities/` (✅ DONE - all 5 entities)
   - DataSource: `backend/src/database/data-source.ts` (✅ DONE)
   - Routes: `backend/src/routes/` (⏳ IN PROGRESS - auth.ts ✅, tournaments.ts ✅, matches.ts ❌, leaderboard.ts ❌)
   - Middleware: `backend/src/middleware/` (⏳ NEEDS CONVERSION)
   - Utils: `backend/src/utils/` (⏳ NEEDS CONVERSION)
   - Server: `backend/src/server.ts` (✅ DONE)

3. **Git workflow:**
   - Current branch: `feature/phase-3.3-orm-refactor`
   - Commits must be small, focused, with clear messages
   - After each file conversion, commit immediately
   - Push after every 2-3 commits
   - Do NOT merge to main/develop

4. **Testing:**
   - After each route conversion, ensure imports are correct
   - Final: Run `npm start` in TEST mode and verify no errors
   - Must be able to start without database connection errors

---

## What's Done

✅ **TypeORM setup:**
- typescript, ts-node, typeorm, reflect-metadata installed
- DataSource configured (SQLite for test, PostgreSQL for prod)
- All 5 entities created (User, Tournament, TournamentPlayer, Match, MatchPlayer)

✅ **Routes converted to TypeScript:**
- auth.ts: Login/register with TypeORM User repository
- tournaments.ts: List, get, register, unregister with TypeORM

✅ **Documentation reorganized:**
- All docs moved to `docs/` subfolder
- Path references updated in AGENTS.md

✅ **server.ts created:**
- Express server with TypeORM initialization
- Routes mounted
- Error middleware

---

## What's Remaining (IN ORDER)

### 1. Convert matches.ts to TypeScript
**File:** `backend/src/routes/matches.js` → `backend/src/routes/matches.ts`

**Current logic:**
- GET /matches/:id - Get match details
- GET /tournaments/:id/matches - List matches for tournament
- POST /tournaments/:id/matches/:matchId/score - Submit match score

**Convert to TypeScript:**
- Replace raw database.get/all/run with TypeORM repositories
- Import Match, MatchPlayer, User, Tournament entities
- Use TypeORM QueryBuilder for complex queries
- Import Express types

**Commit message:** `feat: Convert matches routes to TypeScript with TypeORM`

---

### 2. Convert leaderboard.ts to TypeScript
**File:** `backend/src/routes/leaderboard.js` → `backend/src/routes/leaderboard.ts`

**Current logic:**
- GET /leaderboard - Global rankings (top players by winnings)
- GET /leaderboard/:userId - Player stats (tournaments, wins, avg finish, total winnings)

**Convert to TypeScript:**
- Use TypeORM QueryBuilder for complex aggregations
- Calculate: tournaments_played, tournament_wins, avg_finish, total_winnings
- Group and order by winnings descending

**Commit message:** `feat: Convert leaderboard routes to TypeScript with TypeORM`

---

### 3. Convert middleware/auth.ts
**File:** `backend/src/middleware/auth.js` → `backend/src/middleware/auth.ts`

**Current logic:**
- JWT verification with `jwt.verify()`
- Extract user_id and username from token
- Attach to req.user

**Convert to TypeScript:**
- Add Express Request/Response/NextFunction types
- Define interface for req.user (user_id: number, username: string)
- Export default middleware

**Commit message:** `feat: Convert auth middleware to TypeScript`

---

### 4. Convert middleware/errorHandler.ts
**File:** `backend/src/middleware/errorHandler.js` → `backend/src/middleware/errorHandler.ts`

**Current logic:**
- Catch errors and return JSON with status codes
- Log errors
- Return 500 for unexpected errors

**Convert to TypeScript:**
- Add Express error handler types
- Type error parameter
- Export default middleware

**Commit message:** `feat: Convert error handler middleware to TypeScript`

---

### 5. Convert utils/validation.ts
**File:** `backend/src/utils/validation.js` → `backend/src/utils/validation.ts`

**Current logic:**
- Validators: username (3-32 chars), password (6+ chars), email (regex)

**Convert to TypeScript:**
- Export functions with return type: boolean
- Add JSDoc comments for clarity

**Commit message:** `feat: Convert validation utilities to TypeScript`

---

### 6. Update package.json
**Already done:** start and dev scripts use ts-node

**Verify:** `npm start` works (TypeORM initializes, server listens on port 5000)

---

### 7. Test the API
**Steps:**
1. Ensure `.env` file exists or use default JWT_SECRET
2. Run `npm install` (if not already done)
3. Run `npm start` - should see:
   ```
   TypeORM DataSource initialized successfully
   OpenClaw Poker API running on port 5000
   ```
4. Test with curl or Postman:
   ```
   POST http://localhost:5000/api/auth/login
   { "username": "test", "password": "password" }
   ```

**Expected response:**
```
{
  "token": "<JWT_TOKEN>",
  "user_id": 1,
  "username": "test",
  "expires_in": 3600
}
```

---

## Dependencies Installed

```
npm list --depth=0 | grep typeorm
npm list --depth=0 | grep ts-node
npm list --depth=0 | grep typescript
```

Should show:
- typeorm@^0.3.28
- ts-node@^10.9.2
- typescript@^5.9.3
- reflect-metadata@^0.2.2

---

## Key Files to Review

- `docs/specifications/DEPLOYMENT_ARCHITECTURE.md` - Test/prod setup
- `docs/standards/DOCUMENTATION_STANDARDS.md` - Doc structure
- `backend/src/database/data-source.ts` - TypeORM initialization
- `backend/src/server.ts` - Express + TypeORM setup
- `backend/src/routes/auth.ts` - Example route conversion

---

## Budget

Starting budget for this session: ~$5.06 USD
Estimated cost for remaining work: 1.5-2 hours (~$1.86-2.48)
**Margin available: Good**

---

## Success Criteria

✅ All routes converted to TypeScript
✅ All middleware converted to TypeScript
✅ All utils converted to TypeScript
✅ `npm start` runs without errors
✅ API listens on port 5000
✅ Health check endpoint responds: `GET /health` → `{ "status": "ok" }`
✅ Auth routes work with TypeORM User repository
✅ Tournament routes work with TypeORM repositories
✅ Matches routes work with TypeORM repositories
✅ Leaderboard calculations work with TypeORM QueryBuilder
✅ Can test with Postman against `http://localhost:5000`

---

## When You're Done

1. Final commit: `feat: Phase 3.3 complete - full TypeScript/TypeORM conversion with test-ready API`
2. Push to feature/phase-3.3-orm-refactor
3. Report to Jon: "Phase 3.3 complete. API testable in Postman at localhost:5000"
4. Do NOT merge to main/develop

---

**Good luck. This is straightforward routing work. Follow the patterns in auth.ts and tournaments.ts.**
