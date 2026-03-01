# Documentation Index

**Category:** documentation
**Purpose:** User guides, setup procedures, troubleshooting, and operational documentation

**Status:** active
**Version:** 2.1
**Last Updated:** 2026-03-01 GMT+13
**Owner:** Jon + Development Team
**Related Documents:** [DOCUMENTATION_STANDARDS.md](./standards/DOCUMENTATION_STANDARDS.md), [DOCUMENT_INDEX.md](./DOCUMENT_INDEX.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-03-01 | 2.1 | Sonnet 4.6 | Added tests/ folder reference; TEST-PLAN.md established as living document |
| 2026-02-26 21:15 | 2.0 | Sonnet 4.5 | Updated index: removed obsolete API-REFERENCE.md, added new API specification docs, updated metadata |
| 2026-02-22 11:50 | 1.0 | Angus | Added metadata and change log per DOCUMENTATION_STANDARDS.md |
| 2026-02-22 11:43 | 1.0 | Angus | Initial creation |

---

## Quick Reference

| Document | Tags | Purpose | Read When |
|----------|------|---------|-----------|
| [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md) | setup, development, environment | Get the development environment running | First time setup, onboarding new dev |
| [DEPLOYMENT-GUIDE.md](./documentation/DEPLOYMENT-GUIDE.md) | deployment, production, operations | Deploy to production | Taking to prod, updates |
| [OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md](./specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) | api, backend, endpoints, specification | Complete API specification with locked JSON contracts | Building frontend, testing API, contract reference |
| [API-FIELD-NAMING-GUIDE.md](./standards/API-FIELD-NAMING-GUIDE.md) | api, standards, naming | Field naming conventions (backend as source of truth) | Writing API integration code |
| [AGENTS.md](./standards/AGENTS.md) | standards, quality, api-integration | Mandatory quality standards for API integration | Before writing any API integration code |
| [TROUBLESHOOTING.md](./documentation/TROUBLESHOOTING.md) | debugging, troubleshooting, errors | Debug common issues, error messages | When something breaks |
| [tests/TEST-PLAN.md](./tests/TEST-PLAN.md) | testing, unit-tests, integration, stress | Project-wide test plan - all test suites, clinical testing, stress tests | Before running tests or starting Phase 4.1 |

---

## By Situation

### I'm setting up locally for the first time
→ Start with [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md)

### I want to test the API
→ [OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md](./specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) + [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md) for local setup

### I'm deploying to production
→ [DEPLOYMENT-GUIDE.md](./documentation/DEPLOYMENT-GUIDE.md) + [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md) (for reference)

### Something's broken / I'm getting an error
→ [TROUBLESHOOTING.md](./documentation/TROUBLESHOOTING.md) first, then [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md) for reference

---

## Document Status

All documents in this folder are **active** and production-ready.

| Document | Status | Last Verified |
|----------|--------|----------------|
| SETUP-GUIDE.md | active | (To be tested) |
| DEPLOYMENT-GUIDE.md | active | (To be tested) |
| API-REFERENCE.md | active | (To be tested) |
| TROUBLESHOOTING.md | active | (To be updated as issues arise) |

---

## How to Add Documentation

1. Identify the topic (setup, deployment, troubleshooting, API usage, etc.)
2. Create new file: `TOPIC-NAME.md` (uppercase-hyphens)
3. Follow metadata header (see DOCUMENTATION_STANDARDS.md)
4. Set status: `draft` or `active` (operational docs are usually active immediately)
5. Add to this INDEX.md
6. Link from relevant specification/ docs if applicable

---

## Related Documents

- **specifications/** — Architecture and schema (what's being built)
- **design/** — Task board and wireframes (how it's being built)
- **standards/** — DOCUMENTATION_STANDARDS.md governs all these docs
- **tests/** — Test plans, clinical test results, and bug reports
