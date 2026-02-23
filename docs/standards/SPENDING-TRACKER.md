# Project Spending Tracker & Rules

**Category:** standards
**Purpose:** Track project budget, spending, burn rate, and establish rules for cost management across all phases

**Status:** active
**Version:** 1.0
**Last Updated:** 2026-02-22 12:18 GMT+13
**Owner:** Jon
**Related Documents:** [PROJECT_CHARTER.md](../specifications/PROJECT_CHARTER.md), [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-22 12:18 | 1.0 | Angus | Initial creation with budget rules, burn rate tracking, topup protocol, cost projections |

---

## Current Budget Status

| Item | Value |
|------|-------|
| **Total Budget** | $15.23 USD |
| **Spent to Date** | $8.36 USD |
| **Current Balance** | $6.87 USD |
| **Burn Rate** | ~3250 tokens/session (~$3.02/session) |
| **Remaining Sessions** | ~2-3 hours of heavy work |
| **Last Updated** | 2026-02-22 12:18 GMT+13 |
| **Last Topup** | $5.80 USD (2026-02-22 12:18) |

---

## Budget Rules

### Alert Thresholds

Stop and alert Jon when balance falls below:
- **$1.00** — Critical (less than 1 hour of work)
- **$3.00** — Low (less than 3 hours of work)
- **$5.00** — Medium (less than 5 hours of work)

### Spending Protocol

1. **Major work session:** Estimate tokens before starting
2. **During work:** Track progress every 1-2 hours
3. **After work:** Update SPENDING-TRACKER.md change log + token-tracker.json
4. **Approaching alert:** Notify Jon in advance
5. **Below $1.00:** Stop work, wait for topup

### Topup Protocol (When Jon Funds)

When Jon sends topup amount:
1. **Acknowledge:** "Budget topped up $X confirmed"
2. **Update:** token-tracker.json + this document's change log
3. **Calculate:** New balance, new runway in hours
4. **Resume:** Work continues at same burn rate

---

## Phase-by-Phase Cost Tracking

| Phase | Status | Budget | Spent | Remaining | Burn Rate |
|-------|--------|--------|-------|-----------|-----------|
| **Phase 1: Bot Logic** | DONE | $2.50 | $1.86 | $0.64 | ~2000 tokens |
| **Phase 2: Dealer Engine** | DONE | $3.00 | $4.18 | (over) | ~4500 tokens |
| **Phase 3.2: Frontend** | READY | $1.20 | $0.00 | $1.20 | Est. 1000-1200 tokens |
| **Phase 3.3: Backend (Refactor)** | READY | $1.20 | $0.00 | $1.20 | Est. 1000-1200 tokens |
| **Phase 3.4: GitFlow** | READY | $1.20 | $0.00 | $1.20 | Est. 1000-1200 tokens |
| **Phase 4: Testing** | BACKLOG | $1.50 | $0.00 | $1.50 | TBD |
| **Contingency (docs, fixes)** | ACTIVE | $4.13 | $2.32 | $1.81 | Variable |
| **TOTAL** | - | $15.23 | $8.36 | $6.87 | - |

**Notes:**
- Phase 2 overran by $1.18 (dealer engine was complex)
- Phase 1 underran by $0.64 (efficient hand evaluation)
- Current runway: ~2.3 sessions of heavy work (3-4 hours each)

---

## Cost Projection (Forward)

| Phase | Est. Hours | Est. Tokens | Est. Cost | Timeline |
|-------|-----------|-------------|-----------|----------|
| **3.3 Refactor (ORM)** | 2-3h | 2000-3000 | $1.86-2.79 | This week |
| **3.2 Frontend** | 3-4h | 3000-4000 | $2.79-3.72 | Next week |
| **3.4 GitFlow** | 2-3h | 2000-3000 | $1.86-2.79 | Following week |
| **3.5 Setup Docs** | 1-2h | 1000-1500 | $0.93-1.40 | Post-launch |
| **Phase 4 Testing** | 2-3h | 2000-3000 | $1.86-2.79 | Post-Phase 3 |
| **TOTAL REMAINING** | 10-15h | 10000-15000 | $9.30-13.95 | 4-5 weeks |

**Runway Analysis:**
- Current balance: $6.87
- Remaining needed: $9.30-13.95
- **Gap:** Will need topup in 7-10 days (after 3.3 + 3.2)
- **Recommendation:** Plan next topup ~2026-03-01

---

## Burn Rate Calibration

**Historical:**
- Phase 1: 2000 tokens (~$1.86)
- Phase 2: 4500 tokens (~$4.18, complex dealer logic)
- Documentation system: 1500 tokens (~$1.39, now completed)

**Current estimate:** 3250 tokens/session (~$3.02/session)

**Variance factors:**
- Heavy implementation: +500-1000 tokens
- Debugging/refactoring: +300-800 tokens
- Documentation only: -1500-2000 tokens
- Specification drafting: -500-1000 tokens

---

## Cost Control Measures

1. **Spec First:** All work pre-approved in writing (reduces rework)
2. **Verification Protocol:** Run actual code before claiming done (prevents false positives)
3. **Daily Check-in:** Status updates every 1-2 hours during work (catch drift early)
4. **Batch Updates:** Group small doc changes into single session (saves tokens)
5. **Archive Old Sessions:** Don't load unnecessary history (smaller context = fewer tokens)

---

## Topup History

| Date | Amount | Balance Before | Balance After | Notes |
|------|--------|-----------------|----------------|-------|
| 2026-02-22 12:18 | +$5.80 | $0.10 | $6.87 | Critical refund; was at risk |
| 2026-02-19 (initial) | $9.43 | $0.00 | $9.43 | Project start |

---

## When to Request Topup

**Automatic notification to Jon when:**
- Balance hits $1.00 or below
- Weekly snapshot sent Fridays showing burn rate vs. remaining runway
- End of each phase with actual vs. budgeted cost analysis

**Jon can topup anytime:**
- Send WhatsApp with amount: "Top up $X"
- I update this tracker + token-tracker.json within 5 minutes
- Work resumes without delay

---

## Rules for Angus (Agent)

1. **Read this before any topup adjustment** — MANDATORY
2. **Update change log on every topup** — Date, amount, new balance, notes
3. **Monitor burn rate every session** — Track actual vs. estimated
4. **Alert Jon at thresholds** — Don't wait for permission to flag low balance
5. **Never spend below critical ($1.00) without approval** — Pause work and wait

---

**Last Updated:** 2026-02-22 12:18 GMT+13
