# CLAUDE.md - Phase 3.3 TypeORM Refactor (Status Document)

**Category:** standards
**Purpose:** Current status of Phase 3.3 TypeScript/TypeORM conversion and next actions
**Status:** COMPLETE - API functional, 5 CRITICAL issues remain before production
**Version:** 1.2
**Last Updated:** 2026-02-23 23:50 GMT+13
**Owner:** Jon + Development Team
**Tags:** operational, phase-3.3, typeorm, completed, production-blockers

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-23 23:50 | 1.2 | Sonnet 4.5 | Added POST /tournaments implementation; discovered CRIT-6 (RBAC); updated issues tracker |
| 2026-02-23 23:25 | 1.1 | Sonnet 4.5 | Updated post-legacy-file-removal; added CRITICAL issues section; API verified working |
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

## Current Status (2026-02-23 23:25 GMT+13)

### ✅ Phase 3.3 COMPLETE - TypeScript Conversion Done

**All conversion work completed:**
- All routes converted to TypeScript (auth, tournaments, matches, leaderboard)
- All middleware converted to TypeScript (auth, errorHandler)
- All utils converted to TypeScript (validation)
- Legacy JavaScript files removed (server.js, database/db.js)
- API tested and verified working

**Latest Sessions (2026-02-23 evening):**

**Session 1: Legacy File Removal**
- Removed legacy `backend/src/server.js` (conflicted with server.ts)
- Removed legacy `backend/src/database/db.js` (old SQLite wrapper)
- Improved TypeScript type safety in route parameter parsing
- Tested full authentication flow (register → login → protected endpoints)
- Committed changes (commit e5aaa6b)

**Session 2: Postman Collection & Create Tournament**
- Fixed Postman collection v1.2 naming (added "Platform")
- Implemented POST /tournaments endpoint (create tournament)
- Full validation per OpenAPI spec (name, buy_in, entry_fee, max_players, scheduled_at)
- Tested successfully - tournament creation works
- Discovered CRIT-6: No RBAC (any user can create tournaments)
- Updated GitHub issues tracker to v1.1 with CRIT-6
- Commits: 6419abd (Postman v1.2), b2fe677 (POST /tournaments)

**Testing Results:** ✅ ALL PASS
- Server starts successfully on port 5000
- Health endpoint responds correctly
- User registration works
- User login works (JWT issued)
- Protected endpoints authenticate correctly

**See:** docs/progress/2026-02-23_legacy-js-removal-and-api-testing_v1.0.md

---

## ⚠️ CRITICAL Issues Before Production

**Status:** API is functional for development/testing but **NOT PRODUCTION-READY**

**BLOCKER Issues (Must fix before any deployment):**

1. **CRIT-1: Default JWT Secret** (15 min fix)
   - Current: Falls back to 'dev-secret-key' if JWT_SECRET not set
   - Impact: Anyone can forge authentication tokens
   - Fix: Require JWT_SECRET environment variable, fail if missing
   - Files: `backend/src/routes/auth.ts:9`, `backend/src/middleware/auth.ts:43`

2. **CRIT-3: Database Race Condition** (30 min fix)
   - Current: Server starts before database initialization completes
   - Impact: Random 500 errors on startup, inconsistent behaviour
   - Fix: Wait for DataSource.initialize() before starting Express server
   - File: `backend/src/server.ts`

3. **CRIT-5: No PostgreSQL SSL** (45 min fix)
   - Current: Production database connection has no SSL configuration
   - Impact: Credentials transmitted in plaintext, security violation
   - Fix: Add SSL configuration to production DataSource config
   - File: `backend/src/database/data-source.ts`

4. **CRIT-4: Auto-Schema Sync** (60 min fix)
   - Current: `synchronize: true` can destroy data automatically
   - Impact: Data loss during entity changes, no migration history
   - Fix: Disable synchronize, create TypeORM migrations
   - File: `backend/src/database/data-source.ts`

5. **CRIT-6: No Role-Based Access Control** (45 min fix)
   - Current: ANY authenticated user can create tournaments (admin function)
   - Impact: Security breach - regular players can create tournaments
   - Fix: Add role field to User entity, create requireRole middleware, protect admin endpoints
   - Files: `backend/src/database/entities/User.ts`, `backend/src/routes/tournaments.ts:60`

**Total Estimated Time:** 3 hours

**See Full Details:**
- docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (comprehensive review)
- docs/progress/2026-02-23_critical-issues-timeline_v1.0.md (resolution timeline)
- docs/progress/2026-02-23_github-issues-tracker_v1.0.md (GitHub issue templates - updated v1.1)

---

## What's Done

✅ **TypeORM setup:**
- typescript, ts-node, typeorm, reflect-metadata installed
- DataSource configured (SQLite for test, PostgreSQL for prod)
- All 5 entities created (User, Tournament, TournamentPlayer, Match, MatchPlayer)

✅ **Routes converted to TypeScript:**
- auth.ts: Login/register with TypeORM User repository ✅
- tournaments.ts: List, get, register, unregister with TypeORM ✅
- matches.ts: Match details, tournament matches, score submission ✅
- leaderboard.ts: Global rankings, player stats ✅

✅ **Middleware converted to TypeScript:**
- auth.ts: JWT verification middleware ✅
- errorHandler.ts: Express error handler ✅

✅ **Utils converted to TypeScript:**
- validation.ts: Username, password, email validators ✅

✅ **Legacy cleanup:**
- Removed old server.js (2026-02-23) ✅
- Removed old database/db.js (2026-02-23) ✅

✅ **Documentation reorganised:**
- All docs moved to `docs/` subfolder
- Path references updated in AGENTS.md

✅ **server.ts created:**
- Express server with TypeORM initialisation
- Routes mounted
- Error middleware

✅ **API tested and verified:**
- Health check working
- Registration working
- Login working (JWT issued)
- Protected endpoints working

---

## Next Actions

### Immediate Next Steps

**Phase 3.3 is COMPLETE.** All TypeScript conversion work is done.

**Choose one of the following paths:**

#### Path A: Fix CRITICAL Issues (Recommended Before Production)
**Time Required:** 2.5 hours
**Priority:** HIGH - Required before production deployment

See section "⚠️ CRITICAL Issues Before Production" above for details.

Follow timeline in: `docs/progress/2026-02-23_critical-issues-timeline_v1.0.md`

#### Path B: Continue with Phase 3.2 (Frontend Development)
**Status:** Ready to start (no blockers)
**Work:** Build React frontend for tournament lobby and leaderboard
**See:** docs/design/TASK-BOARD.md section "Phase 3.2 Website Frontend"

**Note:** Backend API is fully functional at `http://localhost:5000` for frontend development

#### Path C: Address HIGH Priority Issues
**Time Required:** 3-4 hours
**Work:** Fix N+1 queries, race conditions, authorization gaps

See: `docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md` (HIGH-1 through HIGH-6)

---

## How to Resume Work

**If starting a new session:**

1. **Check current branch:**
   ```bash
   git status
   # Should show: feature/phase-3.3-orm-refactor
   # If not, checkout: git checkout feature/phase-3.3-orm-refactor
   ```

2. **Check latest commits:**
   ```bash
   git log --oneline -5
   # Should see:
   # e5aaa6b - chore: Complete removal of legacy JavaScript files
   # 5862f80 - chore: Remove old JavaScript files
   # 102d025 - fix(CRIT-2): Add User->TournamentPlayer relationship
   ```

3. **Test API is working:**
   ```bash
   cd backend
   npm start
   # Should see:
   # - OpenClaw Poker API running on port 5000
   # - TypeORM DataSource initialized successfully
   ```

4. **Test endpoints:**
   ```bash
   # Health check
   curl http://localhost:5000/health

   # Register user
   curl -X POST http://localhost:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

   # Login
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","password":"password123"}'
   ```

5. **Review documentation:**
   - Phase 3.3 code review: `docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md`
   - Critical issues timeline: `docs/progress/2026-02-23_critical-issues-timeline_v1.0.md`
   - Task board: `docs/design/TASK-BOARD.md`

---

## Session Logs

**Latest sessions:**
- 2026-02-23 late evening: Postman collection fix & POST /tournaments implementation
  - Fixed Postman collection naming (v1.2)
  - Implemented missing create tournament endpoint
  - Discovered CRIT-6 (RBAC security issue)
  - Updated issues tracker to v1.1
  - Commits: 6419abd, b2fe677

- 2026-02-23 evening: Legacy file removal and API testing
  - Log: `docs/progress/2026-02-23_legacy-js-removal-and-api-testing_v1.0.md`
  - Commit: e5aaa6b

- 2026-02-23 afternoon: Phase 3.3 code review
  - Review: `docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md`
  - Issues: `docs/progress/2026-02-23_github-issues-tracker_v1.0.md` (now v1.1)
  - Timeline: `docs/progress/2026-02-23_critical-issues-timeline_v1.0.md`

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

## Git Workflow

**Current Branch:** `feature/phase-3.3-orm-refactor`

**Status:** 2 commits ahead of origin

**Do NOT merge to main/develop until CRITICAL issues are fixed**

**When ready to merge:**
1. Ensure all CRITICAL issues are addressed (see timeline doc)
2. Run full test suite
3. Create pull request to `develop` branch
4. Request code review
5. Merge after approval

---

## Quick Reference

**Start API:**
```bash
cd backend
npm start
# API will be at http://localhost:5000
```

**Test Health:**
```bash
curl http://localhost:5000/health
```

**View Logs:**
```bash
# In backend directory with npm start running
# Logs appear in terminal
```

**Common Issues:**
- If "TypeORM DataSource initialization failed" → Check database file permissions
- If "JWT_SECRET" error → Set JWT_SECRET in .env file (or use default for testing)
- If port 5000 in use → Change PORT in .env or kill existing process

---

**Document Version:** 1.1
**Last Updated:** 2026-02-23 23:25 GMT+13
**Next Update:** After CRITICAL issues addressed or Phase 3.2 started
