# GitHub Issues Tracker - Phase 3.3 Code Review

**Category:** progress
**Purpose:** GitHub issue templates for all CRITICAL and HIGH findings from Phase 3.3 code review
**Status:** active
**Version:** 1.0
**Last Updated:** 2026-02-23 19:00 GMT+13
**Owner:** Sonnet 4.5
**Tags:** github, issues, phase-3.3, code-review, tracking

---

## Instructions

Create these GitHub issues manually at: https://github.com/Groovejets2/Poker/issues

Copy each issue template below and paste into GitHub's "New Issue" form.

---

## CRITICAL Issues (5 total)

### Issue 1: [CRITICAL] Default JWT secret key allows authentication bypass

**Labels:** `security`, `critical`, `phase-3.3`

**Description:**
```markdown
## Severity: CRITICAL - Security Vulnerability

**Files:** `backend/src/routes/auth.ts:9`, `backend/src/middleware/auth.ts:43`

### Issue
Using hardcoded fallback JWT secret defeats authentication:
```typescript
const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-key';
```

### Impact
- Complete authentication bypass
- Anyone can forge tokens with publicly-known secret
- Unauthorized access to all protected endpoints
- Can impersonate any user

### Fix
```typescript
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
  throw new Error('FATAL: JWT_SECRET environment variable must be set');
}
```

### Priority
**BLOCKER** - Fix immediately before any deployment

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (CRIT-1)
- Branch: feature/phase-3.3-orm-refactor
```

---

### Issue 2: ~~[CRITICAL] Leaderboard broken - missing User relationship~~ ✅ FIXED

**Status:** ✅ FIXED in commit `102d025`

**Labels:** `bug`, `critical`, `phase-3.3`, `fixed`

**Description:**
```markdown
## Severity: CRITICAL - Runtime Failure

**Status:** ✅ FIXED in commit 102d025

**File:** `backend/src/database/entities/User.ts`

### Issue (RESOLVED)
Leaderboard queries referenced `u.tournamentPlayers` relationship that didn't exist in User entity.

### Fix Applied
Added `@OneToMany` relationship to User entity:
```typescript
@OneToMany(() => TournamentPlayer, tournamentPlayer => tournamentPlayer.user)
tournamentPlayers: TournamentPlayer[];
```

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (CRIT-2)
- Fix Commit: 102d025
```

---

### Issue 3: [CRITICAL] Database not ready when server starts (race condition)

**Labels:** `bug`, `critical`, `phase-3.3`, `reliability`

**Description:**
```markdown
## Severity: CRITICAL - Reliability

**File:** `backend/src/server.ts:21-28, 63-65`

### Issue
DataSource initialization is asynchronous but server starts immediately without waiting:

```typescript
// Async initialization (doesn't block)
AppDataSource.initialize()
  .then(() => console.log('TypeORM DataSource initialized successfully'))
  .catch((error) => process.exit(1));

// Server starts immediately
app.listen(PORT, () => {
  console.log(`OpenClaw Poker API running on port ${PORT}`);
});
```

### Impact
- Race condition: Requests hit endpoints before database is ready
- Random 500 errors on startup
- Inconsistent behaviour depending on DB connection speed

### Fix
```typescript
async function startServer() {
  try {
    await AppDataSource.initialize();
    console.log('TypeORM DataSource initialized successfully');

    app.listen(PORT, () => {
      console.log(`OpenClaw Poker API running on port ${PORT}`);
    });
  } catch (error) {
    console.error('Error during TypeORM DataSource initialization:', error);
    process.exit(1);
  }
}

startServer();
```

### Priority
**BLOCKER** - Fix before production deployment

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (CRIT-3)
- Branch: feature/phase-3.3-orm-refactor
```

---

### Issue 4: [CRITICAL] Auto-schema sync can destroy data

**Labels:** `bug`, `critical`, `phase-3.3`, `database`

**Description:**
```markdown
## Severity: CRITICAL - Data Loss Risk

**File:** `backend/src/database/data-source.ts:34`

### Issue
TypeORM's `synchronize: true` automatically alters database schema:

```typescript
synchronize: true,  // Line 34 (SQLite config)
```

This automatically:
- Drops columns that no longer exist in entities
- Drops tables during entity refactoring
- Loses data without migration safety

### Impact
- Accidental data loss during development
- No migration history
- Cannot rollback schema changes
- Risk of corrupting test database

### Fix
```typescript
synchronize: false,  // Use migrations instead
migrations: ['src/database/migrations/*.ts'],
migrationsRun: true,
```

Create proper migrations for schema changes using TypeORM CLI.

### Priority
**HIGH** - Fix before significant data is stored in test environment

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (CRIT-4)
- Branch: feature/phase-3.3-orm-refactor
```

---

### Issue 5: [CRITICAL] No PostgreSQL SSL configuration for production

**Labels:** `security`, `critical`, `phase-3.3`, `production`

**Description:**
```markdown
## Severity: CRITICAL - Security (Production)

**File:** `backend/src/database/data-source.ts:14-27`

### Issue
PostgreSQL production config has no SSL/TLS settings:

```typescript
if (env === 'production') {
  dataSourceConfig = {
    type: 'postgres',
    host: process.env.DB_HOST,
    // ... NO SSL CONFIGURATION ...
  };
}
```

### Impact
- Database credentials transmitted in plaintext
- Man-in-the-middle attack vulnerability
- Compliance violations (PCI-DSS, GDPR)

### Fix
```typescript
if (env === 'production') {
  dataSourceConfig = {
    type: 'postgres',
    // ... existing config ...
    ssl: {
      rejectUnauthorized: true,
      ca: process.env.DB_SSL_CA,  // CA certificate
    },
    extra: {
      max: 20,  // connection pool size
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    }
  };
}
```

### Priority
**BLOCKER** - Required for production deployment

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (CRIT-5)
- Branch: feature/phase-3.3-orm-refactor
```

---

## HIGH Priority Issues (6 total)

### Issue 6: [HIGH] N+1 query problem in tournament list (performance)

**Labels:** `performance`, `high`, `phase-3.3`

**Description:**
```markdown
## Severity: HIGH - Performance

**File:** `backend/src/routes/tournaments.ts:32-43`

### Issue
Player counts fetched in a loop, creating N+1 database queries:

```typescript
const tournamentsWithCounts = await Promise.all(
  tournaments.map(async (t) => {
    const playerCount = await tournamentPlayerRepository.count({
      where: { tournament: { id: t.id } }
    });
    // ... creates 1 query per tournament
  })
);
```

For 20 tournaments: **1 query + 20 queries = 21 total queries**

### Impact
- Slow response times (100ms → 2000ms+)
- Database connection exhaustion under load
- Poor user experience

### Fix
Use single query with LEFT JOIN and COUNT:
```typescript
const tournaments = await tournamentRepository
  .createQueryBuilder('t')
  .leftJoin('t.players', 'tp')
  .select('t.*')
  .addSelect('COUNT(tp.id)', 'player_count')
  .groupBy('t.id')
  .orderBy('t.scheduled_at', 'DESC')
  .skip(offset)
  .take(limit)
  .getRawAndEntities();
```

### Priority
Fix before load testing

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (HIGH-1)
- Branch: feature/phase-3.3-orm-refactor
```

---

### Issue 7: [HIGH] Race condition in tournament registration (overbooking possible)

**Labels:** `bug`, `high`, `phase-3.3`, `data-integrity`

**Description:**
```markdown
## Severity: HIGH - Data Integrity

**File:** `backend/src/routes/tournaments.ts:94-154`

### Issue
No database transaction when registering for tournament. Two users can register for the last spot simultaneously:

```typescript
// User A checks: playerCount = 7 (1 spot left)
// User B checks: playerCount = 7 (1 spot left)
// User A registers: playerCount = 8 (full)
// User B registers: playerCount = 9 (OVERBOOKING!)
```

### Impact
- Tournament overbooking
- More players than max_players allows
- Data integrity violation

### Fix
Use database transaction with row-level locking:
```typescript
await AppDataSource.transaction(async (manager) => {
  const tournament = await manager.findOne(Tournament, {
    where: { id: tournamentId },
    lock: { mode: 'pessimistic_write' }
  });

  const playerCount = await manager.count(TournamentPlayer, {
    where: { tournament: { id: tournamentId } }
  });

  if (playerCount >= tournament.max_players) {
    throw new Error('Tournament full');
  }

  await manager.save(newPlayer);
});
```

### Priority
Fix before beta testing with real users

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (HIGH-2)
- Branch: feature/phase-3.3-orm-refactor
```

---

### Issue 8: [HIGH] No authorization on match score submission

**Labels:** `security`, `high`, `phase-3.3`, `authorization`

**Description:**
```markdown
## Severity: HIGH - Security/Authorization

**File:** `backend/src/routes/matches.ts:83-136`

### Issue
Anyone with a valid JWT can submit scores for any match, even if they're not involved:

```typescript
router.post('/:id/submit-score', authMiddleware, async (req, res, next) => {
  // NO CHECK: Is req.user actually in this match?
  // NO CHECK: Is req.user a tournament admin?
  // Anyone can submit any score!
});
```

### Impact
- Match result manipulation
- Cheating in tournaments
- Leaderboard corruption

### Fix
Add authorization check:
```typescript
// Verify user is match participant or tournament admin
const match = await matchRepository.findOne({
  where: { id: matchId },
  relations: ['tournament', 'tournament.created_by', 'players', 'players.user']
});

const userId = req.user.user_id;
const isParticipant = match.players.some(p => p.user.id === userId);
const isTournamentAdmin = match.tournament.created_by.id === userId;

if (!isParticipant && !isTournamentAdmin) {
  return res.status(403).json({
    error: { code: 'FORBIDDEN', message: 'Not authorized to submit scores' }
  });
}
```

### Priority
Fix before any competitive play

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (HIGH-3)
- Branch: feature/phase-3.3-orm-refactor
```

---

### Issue 9: [HIGH] No transaction for match score updates (partial updates possible)

**Labels:** `bug`, `high`, `phase-3.3`, `data-integrity`

**Description:**
```markdown
## Severity: HIGH - Data Integrity

**File:** `backend/src/routes/matches.ts:103-129`

### Issue
Match score submission updates match + multiple players without transaction:

```typescript
// Update match
await matchRepository.save(match);  // Could succeed

// Update players (loop)
for (const result of results) {
  // ... Could fail halfway through!
  await matchPlayerRepository.save(matchPlayer);
}
```

If the loop fails midway:
- Match marked as "completed"
- Winner set
- Only some players have ending_stack updated
- **Inconsistent state**

### Impact
- Partial score submissions
- Data corruption
- Cannot replay/fix failed submissions

### Fix
Wrap in transaction:
```typescript
await AppDataSource.transaction(async (manager) => {
  match.status = 'completed';
  match.winner = { id: winner_id } as User;
  match.completed_at = new Date();
  await manager.save(Match, match);

  for (const result of results) {
    const matchPlayer = await manager.findOne(MatchPlayer, {
      where: { match: { id: matchId }, user: { id: result.user_id } }
    });
    if (matchPlayer) {
      matchPlayer.ending_stack = result.ending_stack;
      matchPlayer.status = result.status;
      await manager.save(MatchPlayer, matchPlayer);
    }
  }
});
```

### Priority
Fix before production

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (HIGH-4)
- Branch: feature/phase-3.3-orm-refactor
```

---

### Issue 10: [HIGH] No validation of query parameters (can cause NaN in SQL)

**Labels:** `bug`, `high`, `phase-3.3`, `validation`

**Description:**
```markdown
## Severity: HIGH - Input Validation

**Files:**
- `backend/src/routes/tournaments.ts:13-14`
- `backend/src/routes/matches.ts:16`
- `backend/src/routes/leaderboard.ts:14-15,58`

### Issue
`parseInt()` on query parameters/path params without validation:

```typescript
const page = parseInt(req.query.page as string) || 1;
const tournamentId = parseInt(req.params.tournament_id);
const matchId = parseInt(req.params.id);
```

Problems:
- `parseInt("abc")` returns `NaN`
- `NaN` in SQL queries causes errors
- No bounds checking (page = -1000?)
- No type checking before parse

### Impact
- 500 errors on invalid input
- Potential SQL errors
- Poor error messages

### Fix
Create validation helper:
```typescript
function parsePositiveInt(value: string | undefined, defaultValue?: number): number {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    if (defaultValue !== undefined) return defaultValue;
    throw new Error('Invalid integer parameter');
  }
  return parsed;
}

// Usage:
const page = parsePositiveInt(req.query.page as string, 1);
const limit = Math.min(parsePositiveInt(req.query.limit as string, 20), 100);
```

### Priority
Fix before production

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (HIGH-5)
- Branch: feature/phase-3.3-orm-refactor
```

---

### Issue 11: [HIGH] SQL dialect incompatibility (SQLite vs PostgreSQL)

**Labels:** `bug`, `high`, `phase-3.3`, `database`, `compatibility`

**Description:**
```markdown
## Severity: HIGH - Cross-Database Issue

**File:** `backend/src/routes/leaderboard.ts:26`

### Issue
```typescript
.addSelect('ROUND(AVG(CAST(tp.finish_position AS DECIMAL)), 2)', 'avg_finish')
```

- **PostgreSQL:** Uses `DECIMAL` type
- **SQLite:** Uses `REAL` type
- `CAST(... AS DECIMAL)` won't work in SQLite

### Impact
- Leaderboard fails in test/dev environment (SQLite)
- Different behaviour between test and production
- Testing doesn't reflect production reality

### Fix
Use database-agnostic approach:
```typescript
.addSelect('ROUND(AVG(tp.finish_position), 2)', 'avg_finish')
```

Or use TypeORM's query builder functions to handle dialect differences.

### Priority
Fix to ensure test/prod parity

### Related
- Code Review: docs/progress/2026-02-23_phase-3.3-code-review_v1.0.md (HIGH-6)
- Branch: feature/phase-3.3-orm-refactor
```

---

## Issue Summary

| Issue | Title | Labels | Priority |
|-------|-------|--------|----------|
| 1 | Default JWT secret key allows authentication bypass | security, critical | BLOCKER |
| 2 | ~~Leaderboard broken - missing User relationship~~ | bug, critical, fixed | ✅ FIXED |
| 3 | Database not ready when server starts | bug, critical, reliability | BLOCKER |
| 4 | Auto-schema sync can destroy data | bug, critical, database | HIGH |
| 5 | No PostgreSQL SSL configuration | security, critical, production | BLOCKER |
| 6 | N+1 query problem in tournament list | performance, high | HIGH |
| 7 | Race condition in tournament registration | bug, high, data-integrity | HIGH |
| 8 | No authorization on match score submission | security, high, authorization | HIGH |
| 9 | No transaction for match score updates | bug, high, data-integrity | HIGH |
| 10 | No validation of query parameters | bug, high, validation | HIGH |
| 11 | SQL dialect incompatibility | bug, high, database, compatibility | HIGH |

---

## Creation Checklist

- [ ] Issue 1 - Default JWT secret
- [x] Issue 2 - User relationship (FIXED)
- [ ] Issue 3 - Database initialization race
- [ ] Issue 4 - Auto-schema sync
- [ ] Issue 5 - PostgreSQL SSL
- [ ] Issue 6 - N+1 query
- [ ] Issue 7 - Tournament registration race
- [ ] Issue 8 - Match score authorization
- [ ] Issue 9 - Match score transaction
- [ ] Issue 10 - Query parameter validation
- [ ] Issue 11 - SQL dialect compatibility

---

**Document Created:** 2026-02-23 19:00 GMT+13
**Version:** 1.0
**Status:** active
**Next Action:** Create issues manually at https://github.com/Groovejets2/Poker/issues
