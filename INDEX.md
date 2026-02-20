# OpenClaw Poker Project - Document Index

**Project Location:** E:\poker-project\
**Storage Format:** Markdown (.md) + CSV where applicable
**Naming Convention:** YYYY-MM-DD_document-name_vX.X.md
**Language:** British English
**Version Control:** Git repository at E:\poker-project\

---

## Directory Structure

```
E:\poker-project\
├── INDEX.md (this file)
├── README.md (optional: quick start guide)
├── .gitignore
│
├── standards/
│   ├── DOCUMENTATION_STANDARDS.md (naming, versioning, format rules)
│   ├── CODING_STANDARDS.md (Python code standards)
│   └── GITFLOW.md (Git workflow)
│
├── specifications/
│   └── Functional requirements, use cases, architectural specs
│
├── design/
│   └── Design documents, API specs, task boards, data schemas
│
├── code/
│   ├── poker_engine/
│   ├── requirements.txt
│   └── PHASE_1_README.md
│
├── tests/
│   ├── unit/ (current unit tests)
│   ├── integration/ (Phase 4+)
│   ├── e2e/ (Phase 4+)
│   └── performance/ (Phase 5+)
│
├── progress/
│   └── PROGRESS_*.md (session logs and milestones)
│
└── archive/
    └── Deprecated or historical documents
```

---

## Current Documents

### Specifications
- **2026-02-19_project-charter_v1.0.md** — Overall project vision, phases, budget, risks
- **2026-02-19_dealer-functional-requirements_v1.0.md** (TBD) — Detailed dealer engine specifications

### Design
- **2026-02-19_task-board_v1.0.md** — Task tracking with status and token estimates

### Code
- (To be populated as development begins)

### Archive
- (To be populated as documents are superseded)

---

## Versioning Scheme

**Format:** vMAJOR.MINOR

- **v1.0** — Initial version
- **v1.1** — Minor fixes, clarifications
- **v2.0** — Major changes or complete rewrite
- **Archived versions** → Move to archive/ with suffix _ARCHIVED

---

## Navigation

**Standards & Rules** → `/standards/` (DOCUMENTATION_STANDARDS.md, CODING_STANDARDS.md, GITFLOW.md)
**Project Specs** → `/specifications/` (charter, requirements)
**Design & Planning** → `/design/` (task boards, API specs)
**Source Code** → `/code/poker_engine/`
**Tests** → `/tests/unit/`, `/tests/integration/`, etc.
**Progress & Logs** → `/progress/`

---

## Last Updated

- **2026-02-20 13:52 GMT+13** — Reorganized for scale; moved standards to `/standards/`, created modular test structure (`/tests/unit/`, `/integration/`, `/e2e/`, `/performance/`), created `/progress/` folder for session logs, removed duplicate CODE_STANDARDS.md
