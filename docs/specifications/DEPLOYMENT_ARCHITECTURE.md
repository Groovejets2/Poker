# Deployment Architecture - Test vs Production

**Category:** specifications
**Purpose:** Define database, port, environment, and configuration differences between test and production environments

**Status:** active
**Version:** 1.0
**Last Updated:** 2026-02-22 11:48 GMT+13
**Owner:** Jon + Angus
**Related Documents:** [PHASE-3-ARCHITECTURE.md](PHASE-3-ARCHITECTURE.md), [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md), [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-22 11:48 | 1.0 | Angus | Added change log table and updated metadata format per DOCUMENTATION_STANDARDS.md |
| 2026-02-22 11:27 | 1.0 | Angus | Initial creation with SQLite (test) vs PostgreSQL (prod) specification |

---

## Quick Reference

| Aspect | TEST | PROD |
|--------|------|------|
| **Database** | SQLite 3 | PostgreSQL 13+ |
| **Location** | `data/test/poker.db` (file-based) | `prod.env` connection string (remote) |
| **Node.js Port** | 3000 (dev) or 5000 (test) | 3000 (behind Nginx) |
| **Frontend URL** | `http://localhost:3000` | `https://openclaw-poker.local` |
| **ORM** | TypeORM or Sequelize | TypeORM or Sequelize (same) |
| **Config File** | `config/test.env` | `config/prod.env` |
| **Migrations** | `npm run migrate:test` | `npm run migrate:prod` |
| **Use Case** | Local development, Postman testing, unit tests | Live tournaments, real users |

---

## Environment Variables

### TEST (`config/test.env`)
```
NODE_ENV=test
DB_TYPE=sqlite
DB_PATH=../../data/test/poker.db
API_PORT=5000
JWT_SECRET=test-secret-key-do-not-use-in-prod
LOG_LEVEL=debug
```

### PROD (`config/prod.env`)
```
NODE_ENV=production
DB_TYPE=postgres
DB_HOST=<your-postgres-host>
DB_PORT=5432
DB_NAME=openclaw_poker
DB_USER=<postgres-user>
DB_PASSWORD=<secure-password>
API_PORT=3000
JWT_SECRET=<cryptographically-secure-key>
LOG_LEVEL=info
```

---

## Database Schema

**Identical schema for both environments** (defined in `backend/src/database/schema.js`):
- users
- tournaments
- tournament_players
- matches
- match_players

Migrations are version-controlled in `backend/src/database/migrations/`.

---

## Startup Commands

```bash
# Test environment (SQLite, development)
npm run start:test

# Production environment (PostgreSQL, hardened)
npm run start:prod

# Run migrations on test DB
npm run migrate:test

# Run migrations on prod DB
npm run migrate:prod
```

---

## File Structure

```
E:\poker-project\backend\
├── src/
│   ├── database/
│   │   ├── schema.js          (ORM models, database-agnostic)
│   │   └── migrations/        (version-controlled schema changes)
│   ├── routes/                (API endpoints)
│   ├── middleware/            (auth, error handling)
│   └── utils/
├── config/
│   ├── test.env               (SQLite connection)
│   └── prod.env               (PostgreSQL connection)
├── data/
│   ├── test/
│   │   └── poker.db           (SQLite file, test only)
│   └── prod/                  (not applicable—PostgreSQL is remote)
└── scripts/
    ├── start-test.js
    ├── start-prod.js
    ├── migrate-test.js
    └── migrate-prod.js
```

---

## Critical Rules

1. **Never hardcode database paths or credentials** — always use `.env`
2. **All code is database-agnostic** — use ORM, not raw SQL
3. **Migrations are mandatory** — any schema change goes through version control
4. **Test data is ephemeral** — poker.db can be deleted and regenerated
5. **Prod data is permanent** — backups required, never delete without verification
6. **Same code runs in both** — no branching for test vs prod logic

---

## When to Read This

- **Every coding session** (before touching backend code)
- **Before deploying to production**
- **When adding database changes**
- **When debugging environment-specific issues**

**Do NOT update this document** unless the core architecture changes (e.g., switching to MongoDB, moving from Nginx to Kubernetes, etc.).
