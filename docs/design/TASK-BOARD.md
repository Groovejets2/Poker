# Task Board - OpenClaw Poker Platform

**Category:** design
**Purpose:** Work queue, task breakdown, status tracking, and timeline for all project phases

**Status:** active
**Version:** 1.1
**Last Updated:** 2026-02-22 11:50 GMT+13
**Owner:** Jon + Angus
**Related Documents:** [PROJECT_CHARTER.md](../specifications/PROJECT_CHARTER.md), [DEPLOYMENT_ARCHITECTURE.md](../specifications/DEPLOYMENT_ARCHITECTURE.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-22 11:50 | 1.1 | Angus | Added metadata and change log; renamed from 2026-02-19_task-board_v1.0.md to TASK-BOARD.md |
| 2026-02-21 10:03 | 1.1 | Angus | Updated Phase 2 completion status, Phase 3 scope change (bot upload backlog) |
| 2026-02-19 23:12 | 1.0 | Jon | Initial creation |

---

## Quick Navigation

Use these sections with offset/limit to avoid loading full file:
- **Summary Only:** Load "Phase Status Summary" section (~40 lines)
- **Immediate Actions:** Load "Immediate Next Actions" section (~20 lines)
- **Full Task Breakdown:** Load "Phase 1-4" sections as needed

---

## Phase 1: Bot Logic

### 1.1 Hand Evaluation Engine
- [x] Design hand ranking system (5-card and Texas Hold'em)
- [x] Implement hand value calculation
- [x] Test hand rankings against known poker hands
- [x] Unit tests for edge cases (ties, kickers, etc.)
- **Status:** DONE
- **Completed:** 2026-02-20 14:51 GMT+13
- **Actual Time:** ~3 hours
- **Token Budget Used:** approximately 800-1000 tokens

### 1.2 Basic Strategy Engine
- [x] Define starting hand rankings (GTO basics)
- [x] Implement pre-flop decision logic
- [x] Implement flop/turn/river logic
- [x] Unit tests for decision consistency
- **Status:** DONE
- **Completed:** 2026-02-20 14:51 GMT+13
- **Actual Time:** ~3 hours
- **Token Budget Used:** approximately 1200-1500 tokens

### 1.3 Zynga Integration
- [ ] Research Zynga API and automation options
- [ ] Build bot input and output handlers
- [ ] Test on Zynga test tables
- **Status:** READY (after 1.1 and 1.2) ✓ Unblocked
- **Estimate:** 2-3 hours
- **Token Budget:** approximately 1000-1500 tokens

### 1.4 Phase 1 Testing
- [ ] Run bot against Zynga opponents for 50 or more hands
- [ ] Log win rate and decision patterns
- [ ] Document results
- **Status:** READY (after 1.3) ✓ Unblocked
- **Estimate:** 1 hour
- **Token Budget:** approximately 300-500 tokens

---

## Phase 2: Dealer Engine

### 2.1 Functional Requirements Document
- [x] Define dealer responsibilities
- [x] Define betting rules (check, fold, raise, all-in)
- [x] Define pot management
- [x] Define action order and turn logic
- **Status:** DONE
- **Estimate:** 1-2 hours
- **Token Budget:** approximately 400-600 tokens

### 2.2 Core Dealer Logic
- [x] Implement dealer state machine
- [x] Implement betting round management
- [x] Implement pot distribution (winner, splits)
- [x] Unit tests (38/38 tests passing)
- **Status:** DONE
- **Completed:** 2026-02-21 10:00 GMT+13
- **Estimate:** 4-5 hours
- **Token Budget:** approximately 1500-2000 tokens

### 2.3 Game Flow Integration
- [ ] Connect dealer to bot interface
- [ ] Test two-bot game with 10 hands
- [ ] Debug any state issues
- **Status:** READY (after 2.2)
- **Estimate:** 2-3 hours
- **Token Budget:** approximately 800-1200 tokens

### 2.4 Multi-Bot Testing
- [ ] Test dealer with four bots
- [ ] Test dealer with eight bots
- [ ] Stress test for 100 hands
- **Status:** READY (after 2.3)
- **Estimate:** 2 hours
- **Token Budget:** approximately 600-900 tokens

---

## Phase 3: Platform Website

### 3.1 Technology Stack and Architecture
- [ ] Finalise technology choices (database, hosting, etc.)
- [ ] Design API specification
- [ ] Design database schema
- **Status:** READY (after Phase 2)
- **Estimate:** 2 hours
- **Token Budget:** approximately 600-800 tokens

### 3.2 Website Frontend
- [ ] Build tournament lobby
- [ ] Build leaderboard
- [x] ~~Build bot upload interface~~ **→ MOVED TO BACKLOG (ON-HOLD)**
- **Status:** READY (after 3.1)
- **Estimate:** 3-4 hours (reduced from 4-5)
- **Token Budget:** approximately 1000-1200 tokens (reduced)

### 3.3 Website Backend
- [x] Build tournament management API (DONE 2026-02-22)
- [x] Build scoring and leaderboard API (DONE 2026-02-22)
- [x] ~~Build bot execution engine~~ **→ MOVED TO BACKLOG (ON-HOLD)**
- **Status:** DONE (needs ORM refactor for test/prod separation)
- **Estimate:** 3-4 hours (completed)
- **Token Budget:** approximately 1000-1200 tokens (used)

---

## Phase 3.4: GitFlow Strategy & PR Automation

### 3.4 GitFlow Implementation (PRIORITY: AFTER 3.3 REFACTOR)
- [ ] Create GitFlow skill with branching strategy (feature/, release/, hotfix/)
- [ ] Implement PR automation via GitHub API
- [ ] Build sub-agent for PR creation + notifications
- [ ] Define code review standards (see below)
- **Status:** READY (after Phase 3.3 refactor)
- **Estimate:** 2-3 hours
- **Token Budget:** approximately 1000-1200 tokens

**Code Review Standards (CRITICAL):**
- Agent must analyze code critically
- Challenge logic when confident in alternative approach
- Willingly recode solutions for better quality
- Use PR process as collaborative improvement tool
- Call Jon before making major architectural decisions
- PRs should improve code, not just pass tests

---

## Phase 3.5: Setup Documentation (POST-LAUNCH)

### 3.5 Setup & Deployment Guides
- [ ] Development environment setup guide
- [ ] Production deployment guide
- [ ] Database migration guide
- [ ] Docker setup (optional)
- **Status:** BACKLOG (after test + prod setups verified)
- **Estimate:** 2 hours
- **Token Budget:** approximately 500-700 tokens
- **Trigger:** Once Phase 3.2 & 3.3 have working test/prod environments

---

## Phase 4: Testing and Quality Assurance

### 4.1 Clinical Testing Plan
- [ ] Define test scenarios
- [ ] Recruit eight test bots (simple strategies)
- [ ] Run 500 or more hands across all bots
- **Status:** READY (after Phase 3)
- **Estimate:** 2-3 hours (setup), then ongoing
- **Token Budget:** approximately 400-600 tokens

### 4.2 Bug Fixes and Optimisation
- [ ] Document any bugs found
- [ ] Prioritise and fix bugs
- [ ] Re-test after each fix
- **Status:** READY (after 4.1)
- **Estimate:** Variable

---

## Summary

- **Phase 1 Total:** Approximately 5-7 tasks, USD 1.50-2.50 — COMPLETE ✓
- **Phase 2 Total:** Approximately 10 tasks, USD 2.00-3.00 — COMPLETE ✓
- **Phase 3 Total:** Approximately 4-5 tasks (bot upload on hold), USD 1.50-2.00 — 3.3 DONE, 3.2 READY
- **Phase 4 Total:** Approximately 2 main tasks, USD 0.50-1.00

**Grand Total:** Approximately USD 5.50-8.50 (within budget with increased margin)

---

## Phase Status Summary

**Phase 1 (Bot Logic):** COMPLETE ✓
- 1.1 & 1.2 fully implemented with 64/64 tests passing
- 1.3 & 1.4 on backlog (Zynga integration skipped per decision 2026-02-21)

**Phase 2 (Dealer Engine):** COMPLETE ✓
- 2.1 Functional Requirements: DONE (2026-02-20)
- 2.2 Core Dealer Logic: DONE (2026-02-21) — 38/38 tests passing
- 2.3 & 2.4 Testing: READY to start or skip based on timeline

**Phase 3 (Platform Website):** IN PROGRESS
- 3.3 Backend API: DONE (2026-02-22) — but needs ORM refactor for test/prod
- 3.2 Frontend: READY to start (awaiting 3.3 refactor)
- 3.1 Architecture: SUPERSEDED by DEPLOYMENT_ARCHITECTURE.md
- Bot upload: MOVED TO BACKLOG (on-hold indefinitely)

---

## Immediate Next Actions

**PRIORITY 1:** Refactor Phase 3.3 Backend (ORM Integration)
- Current: Raw SQLite via sqlite3 module
- Target: TypeORM or Sequelize (database-agnostic)
- Why: Enable test/prod separation (SQLite for test, PostgreSQL for prod)
- Estimate: 2-3 hours
- Then: test/prod folder restructuring per DEPLOYMENT_ARCHITECTURE.md

**PRIORITY 2:** Phase 3.2 Frontend (React)
- Blocked on 3.3 refactor completion
- Build tournament lobby + leaderboard
- Estimate: 3-4 hours after 3.3 ready

---

**Last Updated:** 2026-02-22 11:50 GMT+13
**Version:** 1.1
**Maintainer:** Angus Young + Jon
