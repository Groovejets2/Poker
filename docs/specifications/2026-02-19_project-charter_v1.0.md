# OpenClaw Poker Platform - Project Charter

**Category:** specifications
**Purpose:** Define project vision, budget, phases, success metrics, and governance model

**Status:** active
**Version:** 1.0
**Last Updated:** 2026-02-22 11:48 GMT+13
**Owner:** Jon
**Related Documents:** [TASK-BOARD.md](../design/TASK-BOARD.md), [DEPLOYMENT_ARCHITECTURE.md](../DEPLOYMENT_ARCHITECTURE.md), [DOCUMENTATION_STANDARDS.md](../DOCUMENTATION_STANDARDS.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-22 11:48 | 1.0 | Angus | Added change log table and updated metadata format per DOCUMENTATION_STANDARDS.md |
| 2026-02-19 23:12 | 1.0 | Jon | Initial creation |

---

## Vision Statement

OpenClaw Poker: An open platform where developers build, test, and compete with AI poker bots. Craft your strategy. Upload your bot. Prove your algorithm is smarter than everyone else's. Compete in tournaments, win prize pools, and claim glory. The real reward isn't just the money — it's knowing your bot outplayed the competition.

---

## Core Principles

1. **Bot-Only Gameplay** — No real players. Eliminates gambling licensing and compliance issues.
2. **Skill Competition** — Better bot = higher win rate. Value prop is in algorithmic intelligence.
3. **Monetisation via Tournaments** — Users pay to enter tournaments. Platform takes percentage.
4. **Open Ecosystem** — Other OpenClaw users can build and upload their own bots.
5. **Tight Budget Discipline** — Every token counts. Spec first, code second.

---

## Phases

### Phase 1: Bot Logic (MVP)
- Hand evaluation engine (5-card draw and Texas Hold'em)
- Basic strategy decision-making
- Test on Zynga Poker
- **Deliverable:** Playable bot
- **Budget:** £2.50-3.50 USD equivalent

### Phase 2: Dealer Engine
- Game flow management
- Pot management
- Betting round logic
- Rules enforcement
- Unit tests for all logic
- **Deliverable:** Fully functional dealer
- **Budget:** £1.50-2.50 USD equivalent

### Phase 3: Platform Website
- Bot registration and upload
- Tournament creation and management
- Leaderboards
- Basic user interface
- **Deliverable:** Live website
- **Budget:** £1.50-2.50 USD equivalent

### Phase 4: Testing and Quality Assurance
- Eight-bot clinical testing
- Performance validation
- Bug fixes and optimisation
- **Deliverable:** Stable, tested system
- **Budget:** £0.75-1.50 USD equivalent

### Phase 5: Marketing and Design (To Be Determined)
- Professional branding
- Marketing strategy
- Public launch preparation
- **Budget:** To be determined

---

## Budget Model

- **Current Balance:** USD 9.43
- **Weekly Funding:** USD 9-20 per week (recurring)
- **Monthly Runway:** approximately USD 36-80 per month
- **Approach:** Incremental building, not sprint-based. Time allocated to ensure quality.
- **Allocation per phase:**
  - Phase 1: USD 3-4
  - Phase 2: USD 2-3
  - Phase 3: USD 2-3
  - Phase 4: USD 1-2
  - Phase 5: Reserve and future allocation
- **Tracking:** Real-time via token-tracker.json plus weekly budget reviews
- **Note:** No panic mode. This is sustainable long-term work.

---

## Technical Decisions (To Finalise)

- **Bot Logic:** Python (fast, good poker libraries available)
- **Dealer Engine:** Python (same codebase)
- **Website:** Node.js and React (later, Phase 3)
- **Testing:** pytest for unit tests
- **Database:** To be determined (Phase 3)

---

## Success Metrics

- Phase 1: Bot beats Zynga benchmark
- Phase 2: Dealer handles eight concurrent bots without errors
- Phase 3: Website launches and handles tournament flow
- Phase 4: Clinical testing passes with less than 5% error rate
- Final: Eight or more external bots can upload and compete

---

## Key Risks

1. **Token budget depletion** — Mitigation: Specify everything first, code only approved tasks
2. **Scope creep** — Mitigation: Strict task board, approve all changes
3. **Complex mathematical requirements** — Mitigation: Research and plan before coding
4. **Testing delays** — Mitigation: Unit tests from day one

---

## Project Governance

- Jon is the decision-maker. I provide ideas and warnings.
- No code without specifications. No specifications without approval.
- Two-way relationship: I will advise if we are drifting off course.
- Progress updates delivered in text format (not voice) when work is being executed.

---

**Document Created:** 2026-02-19 23:12 GMT+13
**Version:** 1.0
**Status:** Approved
