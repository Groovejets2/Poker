# Specifications Index

**Category:** specifications
**Purpose:** Navigate all specifications, architecture decisions, and schema definitions for OpenClaw Poker

**Status:** active
**Version:** 1.2
**Last Updated:** 2026-03-01 GMT+13
**Owner:** Jon + Angus
**Related Documents:** [DOCUMENTATION_STANDARDS.md](../standards/DOCUMENTATION_STANDARDS.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-03-01 | 1.2 | Sonnet 4.6 | Removed Phase 4.1 Clinical Testing Plan (moved to docs/tests/TEST-PLAN.md as living document) |
| 2026-02-26 21:30 | 1.1 | Sonnet 4.5 | Updated to reference actual API spec (OPEN-CLAW-API-SPECIFICATION); removed non-existent API-SCHEMA.md and DATABASE-SCHEMA.md references; moved obsolete files to archive |
| 2026-02-22 11:50 | 1.0 | Angus | Added metadata and change log per DOCUMENTATION_STANDARDS.md |
| 2026-02-22 11:42 | 1.0 | Angus | Initial creation with 5-document reference table |

---

## Quick Reference

| Document | Tags | Purpose | Read When |
|----------|------|---------|-----------|
| [PROJECT_CHARTER.md](PROJECT_CHARTER.md) | project, budget, scope | Vision, budget, phases, timeline | Starting new phase, reviewing scope |
| [DEPLOYMENT_ARCHITECTURE.md](DEPLOYMENT_ARCHITECTURE.md) | deployment, test-vs-prod, infrastructure | Test/prod tech stack and separation | **Before any backend coding** |
| [PHASE-3-ARCHITECTURE.md](PHASE-3-ARCHITECTURE.md) | tech-stack, api, backend, frontend | Website tech stack, API design, database schema | Before Phase 3.2 or 3.3 work |
| [OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md](OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) | api, backend, endpoints, specification | Complete API spec with locked JSON contracts | Building or testing API |
| [SECURITY-ARCHITECTURE.md](SECURITY-ARCHITECTURE.md) | security, threats, backend | Security design and threat model | Before deployment |
| [../tests/TEST-PLAN.md](../tests/TEST-PLAN.md) | testing, integration, bots, unit-tests | Project-wide test plan - unit test inventory and clinical testing strategy | Before running tests or starting Phase 4.1 |

---

## By Role

### Backend Engineers
1. **First:** [DEPLOYMENT_ARCHITECTURE.md](DEPLOYMENT_ARCHITECTURE.md) — Know test vs prod setup
2. **Then:** [PHASE-3-ARCHITECTURE.md](PHASE-3-ARCHITECTURE.md) — Understand tech stack and database schema
3. **Then:** [OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md](OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) — Build according to locked spec
4. **Reference:** [../standards/API-FIELD-NAMING-GUIDE.md](../standards/API-FIELD-NAMING-GUIDE.md) for field naming rules

### Frontend Engineers
1. **First:** [PHASE-3-ARCHITECTURE.md](PHASE-3-ARCHITECTURE.md) — Understand tech stack
2. **Then:** [OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md](OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) — Know exact API contracts
3. **Reference:** [../standards/AGENTS.md](../standards/AGENTS.md) — Quality standards before API integration

### DevOps / Deployment
1. **First:** [DEPLOYMENT_ARCHITECTURE.md](DEPLOYMENT_ARCHITECTURE.md) — Know infrastructure
2. **Then:** [PHASE-3-ARCHITECTURE.md](PHASE-3-ARCHITECTURE.md) — Understand tech stack
3. **Reference:** Documentation folder for setup/deployment guides

### Project Lead (Jon)
1. [PROJECT_CHARTER.md](PROJECT_CHARTER.md) — Budget, timeline, scope
2. [DEPLOYMENT_ARCHITECTURE.md](DEPLOYMENT_ARCHITECTURE.md) — Technical decisions
3. All others — As needed for review/approval

---

## Document Status Summary

| Document | Status | Approved | Notes |
|----------|--------|----------|-------|
| PROJECT_CHARTER.md | active | ✓ | Foundational; don't change |
| DEPLOYMENT_ARCHITECTURE.md | active | ✓ | Canonical; read before backend work |
| PHASE-3-ARCHITECTURE.md | active | ✓ | Website tech decisions and database schema |
| OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md | active | ✓ | 🔒 Locked API contract; changes require owner approval |
| SECURITY-ARCHITECTURE.md | active | ✓ | Security design and threat model |
| ../tests/TEST-PLAN.md | active | Jon | Moved to docs/tests/ as living document |

---

## How to Add a New Specification

1. Create new file: `NEW-SPEC-NAME.md` (use uppercase-hyphens)
2. Add metadata header (see DOCUMENTATION_STANDARDS.md)
3. Set status: `draft`
4. Tell Jon: "New spec ready for review: NEW-SPEC-NAME.md"
5. Jon approves → change status to `active`
6. **Add to this INDEX.md**

---

## How to Update a Specification

**Minor changes** (v1.0 → v1.1):
- Clarifications, examples, typos
- Update version in metadata
- Update "Last Updated" date
- No approval needed

**Major changes** (v1.0 → v2.0):
- Architecture change, technology swap, scope change
- Archive old version: move to `archive/` with timestamp
- Create new document with updated content
- Mark status: `review` (needs Jon approval)
- Update this INDEX.md with new location

---

## Related Documents

- **DOCUMENTATION_STANDARDS.md** — How all documents are structured and maintained
- **design/** folder — Task board and design decisions (more tactical, less formal)
- **documentation/** folder — User guides and operational procedures
