# Documentation Index

**Category:** documentation
**Purpose:** User guides, setup procedures, troubleshooting, and operational documentation

**Status:** active
**Version:** 1.0
**Last Updated:** 2026-02-22 11:50 GMT+13
**Owner:** Jon + Angus
**Related Documents:** [DOCUMENTATION_STANDARDS.md](./standards/DOCUMENTATION_STANDARDS.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-22 11:50 | 1.0 | Angus | Added metadata and change log per DOCUMENTATION_STANDARDS.md |
| 2026-02-22 11:43 | 1.0 | Angus | Initial creation |

---

## Quick Reference

| Document | Tags | Purpose | Read When |
|----------|------|---------|-----------|
| [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md) | setup, development, environment | Get the development environment running | First time setup, onboarding new dev |
| [DEPLOYMENT-GUIDE.md](./documentation/DEPLOYMENT-GUIDE.md) | deployment, production, operations | Deploy to production | Taking to prod, updates |
| [API-REFERENCE.md](./documentation/API-REFERENCE.md) | api, backend, endpoints | API endpoint documentation, usage examples | Building frontend, testing API |
| [TROUBLESHOOTING.md](./documentation/TROUBLESHOOTING.md) | debugging, troubleshooting, errors | Debug common issues, error messages | When something breaks |

---

## By Situation

### I'm setting up locally for the first time
→ Start with [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md)

### I want to test the API
→ [API-REFERENCE.md](./documentation/API-REFERENCE.md) + [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md) for local setup

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
