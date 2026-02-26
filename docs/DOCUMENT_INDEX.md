# Document Index - Master Reference

**Category:** standards
**Purpose:** Master index of all project documentation with hierarchical organization
**Status:** active
**Version:** 1.2
**Last Updated:** 2026-02-26 21:35 GMT+13
**Owner:** Jon + Development Team
**Related Documents:** [DOCUMENTATION_STANDARDS.md](./standards/DOCUMENTATION_STANDARDS.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-26 21:35 | 1.2 | Sonnet 4.5 | Archived 3 obsolete dated documents (task-board, phase-3-architecture, openapi-spec); updated specifications INDEX.md |
| 2026-02-26 21:30 | 1.1 | Sonnet 4.5 | Removed duplicate RESUME_STATE.md, consolidated into SESSION_STATE.md |
| 2026-02-26 21:15 | 1.0 | Sonnet 4.5 | Initial creation as master index; consolidated from root INDEX file per documentation standards |

---

## Quick Navigation

**Start Here:**
- **New to project?** → [CLAUDE.md](../CLAUDE.md) for current status
- **Need to resume work?** → [CLAUDE.md](../CLAUDE.md) + [CURRENT_SESSION_STATE.md](../CURRENT_SESSION_STATE.md)
- **Setting up locally?** → [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md)
- **API integration?** → [AGENTS.md](./standards/AGENTS.md) + [OPEN-CLAW-API-SPECIFICATION](./specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md)

---

## Document Organization

```
docs/
├── INDEX.md                          Main documentation index
├── DOCUMENT_INDEX.md                 This file - master index
│
├── specifications/                   Architecture & design decisions
│   ├── INDEX.md
│   ├── DEPLOYMENT_ARCHITECTURE.md
│   ├── PHASE-3-ARCHITECTURE.md
│   ├── PROJECT_CHARTER.md
│   ├── OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md  [NEW]
│   └── SECURITY-ARCHITECTURE.md
│
├── design/                           Work breakdown & planning
│   ├── INDEX.md
│   ├── TASK-BOARD.md
│   └── PHASE-*.md files
│
├── standards/                        Rules & guidelines
│   ├── INDEX.md
│   ├── DOCUMENTATION_STANDARDS.md
│   ├── SPENDING-TRACKER.md
│   ├── API-FIELD-NAMING-GUIDE.md    [NEW]
│   └── AGENTS.md                    [NEW]
│
├── documentation/                    Operational guides
│   ├── INDEX.md
│   ├── SETUP-GUIDE.md
│   ├── DEPLOYMENT-GUIDE.md
│   └── TROUBLESHOOTING.md
│
├── progress/                         Daily session logs
│   └── YYYY-MM-DD_session-name_vX.X.md
│
└── claude/                           [NEW] Claude-specific files
    ├── CLAUDE_ARCHIVE.md
    └── RESUME_STATE.md
```

---

## By Category

### 📋 Project Management
| Document | Purpose | Status |
|----------|---------|--------|
| [CLAUDE.md](../CLAUDE.md) | Current project status, quick resume guide | Active - v2.0 |
| [SESSION_STATE.md](./claude/SESSION_STATE.md) | Session recovery and clean restart instructions | Active |
| [TASK-BOARD.md](./design/TASK-BOARD.md) | Current tasks and progress | Active |
| [SPENDING-TRACKER.md](./standards/SPENDING-TRACKER.md) | Budget tracking | Active |
| [CLAUDE_ARCHIVE.md](./claude/CLAUDE_ARCHIVE.md) | Archived session logs | Archive |

### 🏗️ Architecture & Specifications
| Document | Purpose | Status |
|----------|---------|--------|
| [PROJECT_CHARTER.md](./specifications/PROJECT_CHARTER.md) | Project vision, scope, success criteria | Active |
| [PHASE-3-ARCHITECTURE.md](./specifications/PHASE-3-ARCHITECTURE.md) | Tech stack and design decisions | Active |
| [DEPLOYMENT_ARCHITECTURE.md](./specifications/DEPLOYMENT_ARCHITECTURE.md) | Test/prod environment setup | Active |
| [OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md](./specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) | **Complete API spec with locked JSON contracts** | Active |
| [SECURITY-ARCHITECTURE.md](./specifications/SECURITY-ARCHITECTURE.md) | Security design and threat model | Active |

### 📐 Standards & Guidelines
| Document | Purpose | Status |
|----------|---------|--------|
| [DOCUMENTATION_STANDARDS.md](./standards/DOCUMENTATION_STANDARDS.md) | How to write and organize docs | Active |
| [API-FIELD-NAMING-GUIDE.md](./standards/API-FIELD-NAMING-GUIDE.md) | **API field naming conventions** | Active |
| [AGENTS.md](./standards/AGENTS.md) | **Mandatory quality standards for API integration** | Active |

### 📚 User Documentation
| Document | Purpose | Status |
|----------|---------|--------|
| [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md) | Local development setup | Active |
| [DEPLOYMENT-GUIDE.md](./documentation/DEPLOYMENT-GUIDE.md) | Production deployment | Active |
| [TROUBLESHOOTING.md](./documentation/TROUBLESHOOTING.md) | Common issues and solutions | Active |

### 📊 Progress Logs
| Location | Purpose | Status |
|----------|---------|--------|
| [progress/](./progress/) | Daily session logs | Archive - reference only |

---

## By Role

### I'm a Developer
**Setting up:**
1. [SETUP-GUIDE.md](./documentation/SETUP-GUIDE.md) - Get environment running
2. [PHASE-3-ARCHITECTURE.md](./specifications/PHASE-3-ARCHITECTURE.md) - Understand tech stack
3. [OPEN-CLAW-API-SPECIFICATION](./specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) - API reference

**Writing code:**
1. [AGENTS.md](./standards/AGENTS.md) - **Read FIRST before API integration**
2. [API-FIELD-NAMING-GUIDE.md](./standards/API-FIELD-NAMING-GUIDE.md) - Field naming standards
3. [OPEN-CLAW-API-SPECIFICATION](./specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) - API contracts
4. [TASK-BOARD.md](./design/TASK-BOARD.md) - Current tasks

### I'm Continuing AI Agent Work
**Resuming:**
1. [CLAUDE.md](../CLAUDE.md) - **Start here** for current status
2. [SESSION_STATE.md](./claude/SESSION_STATE.md) - Session recovery (if needed)
3. [TASK-BOARD.md](./design/TASK-BOARD.md) - What's next

**Before writing API code:**
1. [AGENTS.md](./standards/AGENTS.md) - **MANDATORY quality standards**
2. [API-FIELD-NAMING-GUIDE.md](./standards/API-FIELD-NAMING-GUIDE.md) - Naming rules
3. [OPEN-CLAW-API-SPECIFICATION](./specifications/OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md) - Contract reference

### I'm a Project Manager
**Overview:**
1. [PROJECT_CHARTER.md](./specifications/PROJECT_CHARTER.md) - Vision and scope
2. [TASK-BOARD.md](./design/TASK-BOARD.md) - Current status
3. [SPENDING-TRACKER.md](./standards/SPENDING-TRACKER.md) - Budget tracking
4. [CLAUDE.md](../CLAUDE.md) - Latest progress

---

## By Situation

### 🚨 Something's broken
1. [TROUBLESHOOTING.md](./documentation/TROUBLESHOOTING.md)
2. [CLAUDE.md](../CLAUDE.md) - Check known issues
3. [progress/](./progress/) - Review recent changes

### 🎯 Starting a new task
1. [TASK-BOARD.md](./design/TASK-BOARD.md) - See what's available
2. [CLAUDE.md](../CLAUDE.md) - Check current state
3. [AGENTS.md](./standards/AGENTS.md) - If API work, read quality standards

### 🔧 Deploying to production
1. [DEPLOYMENT-GUIDE.md](./documentation/DEPLOYMENT-GUIDE.md)
2. [DEPLOYMENT_ARCHITECTURE.md](./specifications/DEPLOYMENT_ARCHITECTURE.md)
3. [SECURITY-ARCHITECTURE.md](./specifications/SECURITY-ARCHITECTURE.md)

### 📝 Writing documentation
1. [DOCUMENTATION_STANDARDS.md](./standards/DOCUMENTATION_STANDARDS.md) - **Follow these rules**
2. Update relevant INDEX.md files
3. Update version and last updated date

---

## Recently Added/Modified (2026-02-26)

### New Documents
- `OPEN-CLAW-API-SPECIFICATION_v1.0_2026-02-26.md` - Complete API specification
- `API-FIELD-NAMING-GUIDE.md` - Field naming standards
- `AGENTS.md` - Quality standards for API integration
- `SESSION_STATE.md` - Session recovery document
- `DOCUMENT_INDEX.md` - This file

### Updated Documents
- `CLAUDE.md` - v2.0 - API integration status
- `INDEX.md` - v2.0 - Removed obsolete API-REFERENCE.md
- `DOCUMENTATION_STANDARDS.md` - v1.1 - Added mandatory check for existing documents
- `DOCUMENT_INDEX.md` - v1.1 - Removed duplicate session state document

### Removed/Archived Documents
- `API-REFERENCE.md` - Consolidated into OPEN-CLAW-API-SPECIFICATION
- `RESUME_STATE.md` - Outdated, superseded by SESSION_STATE.md
- `2026-02-19_task-board_v1.0.md` - Archived (superseded by TASK-BOARD.md)
- `2026-02-21_phase-3-architecture_v1.0.md` - Archived (superseded by PHASE-3-ARCHITECTURE.md)
- `2026-02-21_openapi-specification_v1.0.md` - Archived (superseded by OPEN-CLAW-API-SPECIFICATION)

### Reorganized
- `CLAUDE_ARCHIVE.md` - Moved to `docs/claude/`
- `SESSION_STATE.md` - Renamed from CURRENT_SESSION_STATE.md (simpler name)

---

## Document Status Legend

- **Active** - Current, up-to-date, refer to this
- **Draft** - Work in progress, not final
- **Archive** - Historical reference, not current
- **Deprecated** - Do not use, kept for reference only

---

**Version:** 1.0
**Last Updated:** 2026-02-26 21:15 GMT+13
**Maintained By:** Development Team
