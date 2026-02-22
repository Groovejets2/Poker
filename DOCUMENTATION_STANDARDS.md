# Documentation Standards & System

**Category:** standards
**Purpose:** Establish a holistic, standards-controlled documentation system for architecture, use cases, tech configuration, API specs, and operations.

**Status:** active
**Version:** 1.3
**Last Updated:** 2026-02-22 16:02 GMT+13
**Owner:** Jon + Angus
**Related Documents:** [DEPLOYMENT_ARCHITECTURE.md](../DEPLOYMENT_ARCHITECTURE.md), [PROJECT_CHARTER.md](../specifications/PROJECT_CHARTER.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-22 16:02 | 1.3 | Angus | Added section 14 (section markers for offset/limit reading); permanent token discipline fix |
| 2026-02-22 12:00 | 1.2 | Angus | Added version column to change log table; clarified progress/log file naming (date-ordered); added archive management and grep rules |
| 2026-02-22 11:48 | 1.0 | Angus | Added mandatory change log tables to section 3; updated operating mandate |
| 2026-02-22 11:40 | 1.0 | Angus | Initial creation with 12 sections covering folder taxonomy, naming, versioning, review workflow |

---

## 1. Folder Taxonomy

```
E:\poker-project\
│
├── specifications/          ← WHAT we're building (immutable, versioned)
│   ├── INDEX.md             (navigation + table of contents)
│   ├── PROJECT_CHARTER.md
│   ├── DEPLOYMENT_ARCHITECTURE.md
│   ├── PHASE-3-ARCHITECTURE.md
│   ├── API-SCHEMA.md
│   ├── DATABASE-SCHEMA.md
│   └── [archive/]
│
├── design/                  ← HOW we're building it (evolving, task-focused)
│   ├── TASK-BOARD.md        (work queue, priorities)
│   ├── UI-WIREFRAMES.md
│   └── [archive/]
│
├── documentation/           ← HOW TO USE IT (guides, procedures)
│   ├── INDEX.md             (navigation)
│   ├── SETUP-GUIDE.md       (dev environment)
│   ├── DEPLOYMENT-GUIDE.md  (take to production)
│   ├── TROUBLESHOOTING.md   (debug + fix issues)
│   ├── API-REFERENCE.md     (endpoint details)
│   └── [archive/]
│
├── standards/               ← RULES + GUIDELINES (prescriptive)
│   ├── DOCUMENTATION_STANDARDS.md  (this file)
│   ├── CODE_STANDARDS.md           (style, structure)
│   ├── GIT_WORKFLOW.md             (branching, commits)
│   └── TESTING_STANDARDS.md        (unit tests, coverage)
│
├── progress/                ← TRACKING (daily logs, snapshots)
│   ├── 2026-02-22.md        (daily session notes)
│   ├── 2026-02-21.md
│   └── MILESTONES.md        (version releases, key dates)
│
└── archive/                 ← RETIRED DOCUMENTS (no longer active)
    ├── 2026-02-20_old-spec.md
    └── README.md            (why archived, where moved to)
```

**Principles:**
- **specifications/** = immutable reference documents (truth source)
- **design/** = evolving work documents (tactical, task-driven)
- **documentation/** = user-facing guides (setup, operation, troubleshooting)
- **standards/** = rules that govern all other documents
- **progress/** = session logs and milestones (read-only after date passes)
- **archive/** = retired documents with move-to references

---

## 2. Naming Conventions

### Format by Category

```
Specifications/Design/Documentation/Standards: UPPERCASE-HYPHENATED.md
Progress/Logs (date-ordered, non-versioned):  2026-MM-DD.md or 2026-MM-DD_short-title.md
Archive (retired):                            UPPERCASE-HYPHENATED_vX.Y_archived-2026-MM-DD.md
```

### Rules

1. **Specifications, Design, Documentation, Standards: UPPERCASE with hyphens**
   - `DEPLOYMENT-ARCHITECTURE.md` ✅
   - `TASK-BOARD.md` ✅
   - `deployment_architecture.md` ❌ (underscores)
   - `deployment-architecture.md` ❌ (lowercase)

2. **No dates in active versioned filenames**
   - `PHASE-3-ARCHITECTURE.md` ✅
   - `PHASE-3-ARCHITECTURE-2026-02-21.md` ❌ (dates in active docs hurt searchability)

3. **Progress & Log Files: ISO date prefix (for chronological ordering)**
   - `progress/2026-02-22.md` ✅
   - `progress/2026-02-22_session-summary.md` ✅ (optional short title after date)
   - These are time-ordered, not versioned — no version suffix

4. **Versioning lives in document metadata, not filename**
   - Document header has `Version: 1.0`
   - Filename never contains version unless archived

5. **Archived documents: Full timestamp + version**
   - `archive/DEPLOYMENT-ARCHITECTURE_v1.0_archived-2026-02-20.md` ✅
   - Includes version + archived date for reference and audit trail

### Examples

✅ **Correct:**
- `DEPLOYMENT-ARCHITECTURE.md` (active, stable, spec)
- `TASK-BOARD.md` (active, evolving, design)
- `progress/2026-02-22.md` (daily log, time-ordered)
- `progress/2026-02-22_session-summary.md` (daily log with optional title)
- `archive/DEPLOYMENT-ARCHITECTURE_v1.0_archived-2026-02-20.md` (retired, dated)

❌ **Wrong:**
- `deployment-architecture.md` (lowercase)
- `DEPLOYMENT_ARCHITECTURE.md` (underscores)
- `DEPLOYMENT-ARCHITECTURE-2026-02-22.md` (date in active doc, hurts navigation)
- `task_board_v2.md` (version in filename)
- `progress/session-summary.md` (no date prefix on progress file, breaks ordering)

---

## 3. File Structure (Metadata + Content + Change Log)

Every document has THREE sections before content:

### 3a. Metadata Header

```markdown
# Document Title

**Category:** specifications | design | documentation | standards | progress
**Purpose:** One-line description of what this document does
**Status:** active | draft | review | archived | superseded
**Version:** X.Y (X = major, Y = minor)
**Last Updated:** YYYY-MM-DD HH:MM GMT+13
**Owner:** Jon | Angus | Both
**Tags:** tag1, tag2, tag3 (optional, for search/filtering)
**Related Documents:** [Link to related docs]
```

**Tags are optional** but help with search/filtering. Use lower-case, hyphen-separated.
Common tags: `api`, `backend`, `frontend`, `deployment`, `test-vs-prod`, `database`, `infrastructure`, `tech-stack`, `security`, `performance`, etc.

### 3b. Change Log Table

Immediately after metadata, before content:

```markdown
---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-22 11:50 | 1.1 | Angus | Added ORM requirement to database schema section |
| 2026-02-22 11:45 | 1.0 | Angus | Initial creation; added deployment architecture |
| 2026-02-23 09:00 | 1.0 | Jon | Approved for production use |
```

**Rules:**
- Every edit gets a row in the table
- Date format: YYYY-MM-DD HH:MM (24-hour time)
- Version: Current version after this change (X.Y format)
  - Increment Y for minor updates (1.0 → 1.1 → 1.2)
  - Increment X for major updates (1.Y → 2.0)
  - See section 10 (Maintenance) for versioning rules
- Author: Jon or Angus (who made the change)
- Change: One-liner describing what changed (be specific, not vague)
- Most recent change at the TOP (reverse chronological order)
- Update **Last Updated** field in metadata AND **Version** field when you add a row

### 3c. Table of Contents (if >2000 words)

```markdown
---

## Table of Contents

[Auto-generated or manual list of sections]
```

### 3d. Main Content

```markdown
---

## Content Section 1

(Main content here)
```

**Complete Example:**

```markdown
# Deployment Architecture - Test vs Production

**Category:** specifications
**Purpose:** Define database, port, and configuration differences between test and production
**Status:** active
**Version:** 1.1
**Last Updated:** 2026-02-22 11:50 GMT+13
**Owner:** Jon + Angus
**Tags:** deployment, test-vs-prod, infrastructure, database
**Related Documents:** [PHASE-3-ARCHITECTURE.md](../PHASE-3-ARCHITECTURE.md)

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-22 11:50 | 1.1 | Angus | Added PostgreSQL details and ORM requirement |
| 2026-02-22 11:27 | 1.0 | Angus | Initial creation |

---

## Quick Reference

(content starts here)
```

### Header Rules

| Field | Purpose | Example |
|-------|---------|---------|
| **Category** | Folder location signal | `specifications`, `design`, `documentation` |
| **Purpose** | One-liner (why this exists) | "Deployment strategy for test/prod separation" |
| **Status** | Is it ready? | `active` = use it; `draft` = don't use yet; `archived` = old |
| **Version** | Track changes | `1.0` = first release, `1.1` = minor update, `2.0` = major change |
| **Last Updated** | Recency signal | When this was last edited |
| **Owner** | Who maintains it | Jon makes final calls; Angus implements |
| **Tags** | Search/filtering (optional) | `api`, `backend`, `deployment`, `test-vs-prod` |
| **Related Documents** | Cross-references | Links to related docs (no inline prose references) |

---

## 4. Indexing System

Every **folder** with 3+ documents gets an `INDEX.md`:

```markdown
# [Folder] Documentation Index

**Location:** E:\poker-project\specifications\
**Purpose:** Navigate specifications for OpenClaw Poker Platform
**Last Updated:** 2026-02-22

---

## Quick Reference

| Document | Purpose | Read When |
|----------|---------|-----------|
| [PROJECT_CHARTER.md](PROJECT_CHARTER.md) | Vision, budget, phases | Starting new phase |
| [DEPLOYMENT_ARCHITECTURE.md](DEPLOYMENT_ARCHITECTURE.md) | Test/prod tech | Before backend coding |
| [API_SCHEMA.md](API_SCHEMA.md) | API endpoints, request/response | Building API |
| [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) | Data model, tables | Designing or migrating DB |

---

## By Role

### For Backend Engineers
1. Read: DEPLOYMENT_ARCHITECTURE.md
2. Read: DATABASE_SCHEMA.md
3. Build: According to API_SCHEMA.md

### For Frontend Engineers
1. Read: PHASE-3-ARCHITECTURE.md (overview)
2. Read: API_SCHEMA.md (what data you get)
3. Build: UI per wireframes

### For DevOps/Deployment
1. Read: DEPLOYMENT_ARCHITECTURE.md
2. Read: PROJECT_CHARTER.md (budget/timeline)
3. Execute: Steps in DEPLOYMENT-GUIDE.md
```

**Rules:**
- INDEX.md is a **table of contents + quick reference**
- It has a **"By Role"** section routing people to the right docs
- It **never duplicates content** — links to content, doesn't repeat it
- It's **updated whenever a document is added/removed/archived**

---

## 5. Cross-Referencing

Documents link to each other, but follow these rules:

### Internal Links (Within Project)
```markdown
See [DEPLOYMENT_ARCHITECTURE.md](../DEPLOYMENT_ARCHITECTURE.md) for test/prod setup.
```

### Sections Within Same Folder
```markdown
For database details, see [DATABASE-SCHEMA.md#users-table](DATABASE-SCHEMA.md#users-table).
```

### Never:
- Copy/paste content from one doc to another (link instead)
- Duplicate rules or specs (single source of truth)
- Reference by line number (it moves; use section headers)

---

## 6. Versioning Strategy

### Minor Updates (1.0 → 1.1)
- Clarifications, typos, examples
- No structural changes
- Keep filename the same
- Update "Last Updated" date
- **Example:** DEPLOYMENT_ARCHITECTURE.md v1.0 → v1.1 (added Postgres backup example)

### Major Changes (1.0 → 2.0)
- Architecture change, new technology, removal of features
- Requires approval before publishing
- **Option A:** Keep old version in archive/ with dated suffix
- **Option B:** Update in-place if it's still active (rare)
- Update filename only if archived
- **Example:** DEPLOYMENT_ARCHITECTURE.md v1.0 → archive/DEPLOYMENT_ARCHITECTURE_v1.0_archived-2026-03-15.md + create DEPLOYMENT_ARCHITECTURE.md v2.0

### When to Version

✅ **Update version in header:**
- Structural changes
- New sections added
- Rules changed
- Technology swapped

❌ **Don't version, just update:**
- Grammar/spelling fixes
- Adding examples (same section)
- Clarifying wording

---

## 7. Status Lifecycle

```
draft → review → active → (minor updates) → archived
```

### draft
- Not ready for use
- Under construction
- Don't read yet

### review
- Ready for Jon's approval
- Angus: "This doc is ready to review"
- Jon: Approves or requests changes
- Once approved → active

### active
- In use, governs work
- Can have minor updates (1.0 → 1.1 → 1.2)
- Always readable and current

### archived
- No longer used
- Moved to archive/ with timestamp
- New document replaces it
- Keep for reference only

---

## 8. Review Workflow (Before Publishing)

**For specifications/ documents (governance-level):**

1. Angus: Draft document, mark status: `draft`
2. Angus: "This doc is ready to review: [filename]"
3. Jon: Reads, approves or requests changes
4. Angus: Updates, changes status: `active`
5. Both: Document is now law

**For design/ documents (tactical, less formal):**

1. Angus: Create/update document
2. Angus: "Updated TASK-BOARD.md"
3. Jon: May approve or request changes
4. Status: `active` if Jon agrees, `draft` if still discussing

**For standards/ documents (system-level):**

1. Same as specifications/ (formal approval)
2. These govern how all other docs are structured

---

## 9. What Goes Where (Decision Tree)

```
Does it describe WHAT we're building?
  ├─ YES → specifications/
  │   (Immutable reference, governs design)
  │   Examples: Charter, architecture specs, schemas
  │
  └─ NO → Does it describe HOW we're building it?
      ├─ YES → design/
      │   (Evolving, task-focused, tactical)
      │   Examples: Task board, wireframes, patterns
      │
      └─ NO → Does it describe HOW TO USE it (after built)?
          ├─ YES → documentation/
          │   (User-facing guides, operation procedures)
          │   Examples: Setup guide, deployment, troubleshooting
          │
          └─ NO → Does it set RULES for future work?
              ├─ YES → standards/
              │   (Prescriptive, governs all other docs)
              │   Examples: Doc standards, code style, git workflow
              │
              └─ NO → Is it a time-dated session log?
                  ├─ YES → progress/
                  │   (Daily notes, snapshots, milestones)
                  │
                  └─ NO → Does it still apply?
                      ├─ NO → archive/
                      │   (Retired, dated, reference only)
                      │
                      └─ YES → You have a new category—talk to Jon
```

---

## 10. Maintenance Rules

### Owner Responsibilities

**Angus (Agent):**
- Create drafts of all documents
- Keep progress/ logs updated daily
- Update minor versions (typos, examples)
- Maintain INDEX.md files
- Archive outdated docs

**Jon (Human):**
- Approve all specifications/ and standards/ documents
- Approve major changes (v2.0+)
- Decide when to archive
- Set strategic direction

### Quarterly Audit (Every 3 months)

1. Review all active documents
2. Archive anything superseded
3. Consolidate fragmented docs
4. Update all INDEX.md files
5. Verify no broken cross-references

### Broken Document = Broken System

- Stale docs lead to wrong decisions
- Cross-reference links must work
- If a doc is outdated, archive it (don't leave it semi-updated)
- If a doc is wrong, fix it immediately (don't let it linger)

---

## 11. Examples (Real Cases)

### Example 1: Add a new API endpoint

1. Update `specifications/API-SCHEMA.md` (add endpoint + schema)
2. Version: 1.2 → 1.3 (minor update, same scope)
3. Update `documentation/API-REFERENCE.md` with usage example
4. Angus: "Updated API schema to include new endpoint"
5. No Jon approval needed (minor specification change)

### Example 2: Switch from SQLite to PostgreSQL in prod

1. Update `specifications/DEPLOYMENT_ARCHITECTURE.md` (change DB technology)
2. Version: 1.0 → 2.0 (major change, architecture shifted)
3. Create `archive/DEPLOYMENT_ARCHITECTURE_v1.0_archived-2026-02-22.md`
4. Angus: "Major change: DEPLOYMENT_ARCHITECTURE.md switched to PostgreSQL"
5. Requires Jon approval
6. Update `specifications/DATABASE-SCHEMA.md` (new migration path)

### Example 3: Clarify how to handle test data

1. Update `standards/TESTING_STANDARDS.md` (add section on test fixtures)
2. Version: 1.0 → 1.1 (minor update, clarification)
3. Update `design/TASK-BOARD.md` (if affects upcoming work)
4. Angus: "Clarified test fixture standards in TESTING_STANDARDS.md"
5. No approval needed (clarification, not structural change)

---

## 12. Angus's Operating Mandate

**Every session, before coding:**

1. Identify task type: "Building Phase 3.2 frontend"
2. Check task-specific docs:
   - Backend task → Read DEPLOYMENT_ARCHITECTURE.md first
   - Frontend task → Read relevant phase spec
   - Adding standard → Read DOCUMENTATION_STANDARDS.md
   - Updating docs → Read DOCUMENTATION_STANDARDS.md

3. If creating/updating a document:
   - Follow structure in section 3 (metadata + change log + content)
   - Use naming from section 2
   - Place in correct folder (section 9 decision tree)
   - Add to INDEX.md
   - Mark status: `draft` (awaiting approval) or `active` (approved)
   - **CRITICAL: Add entry to Change Log table with date, author, and change description**

4. If document is wrong/outdated:
   - Fix immediately or archive it
   - Never leave stale documents in active folders
   - Update all cross-references
   - **Add row to Change Log** (even for small fixes)

### Change Log Protocol (MANDATORY)

**Every time you edit a document:**
1. Add new row to Change Log table (at TOP, reverse chronological)
2. Use format: `| 2026-02-22 11:45 | Angus | Brief description of change |`
3. Update **Last Updated** field in metadata to match change log date
4. Keep description to ONE LINE, specific not vague

**Examples of good change log entries:**
- ✅ "Added PostgreSQL details to production section"
- ✅ "Fixed broken cross-reference to API-SCHEMA.md"
- ✅ "Clarified ORM migration requirements with example"
- ✅ "Updated Phase 3.2 timeline from 4h to 3.5h"

**Examples of bad change log entries:**
- ❌ "Updated document" (too vague)
- ❌ "Fixed stuff" (not specific)
- ❌ "Minor changes" (meaningless)
- ❌ Multi-line entries (keep to one line)

**Key rule:** Documents are sacred. They govern work. If they're broken, work goes wrong. Audit trail proves who changed what, when, and why.

---

## 13. Tools & Automation

### Linting
- All .md files follow structure (metadata block)
- File names follow convention (UPPERCASE-HYPHENATED.md)
- No broken cross-references

### Validation
- Every INDEX.md link is tested (CI/CD)
- No circular references (A → B → A)
- No duplicate content (checked manually in review)

### Future
- Git pre-commit hook: validate .md structure
- GitHub Actions: test all links, flag stale docs
- Auto-generate site from /specifications (once mature)

---

## Summary Table

| Aspect | Rule |
|--------|------|
| **Folder taxonomy** | 6 folders: specifications, design, documentation, standards, progress, archive |
| **File naming** | `CATEGORY-NAME.md` (uppercase, hyphens, no dates for active docs) |
| **Metadata** | Every doc has: Category, Purpose, Status, Version, Updated, Owner, Tags, Related |
| **Change Log** | Every doc has table: Date, Version, Author, Change (mandatory, reverse chronological) |
| **Section markers** | Large docs (>100 lines) include [SECTION: Name — lines X-Y] for easy offset/limit reading |
| **Indexing** | Every folder (3+ docs) has INDEX.md with table + role-based routing |
| **Cross-referencing** | Link don't duplicate; use markdown links, not line numbers |
| **Versioning** | Minor (1.0→1.1) for updates; Major (1.0→2.0) for architecture changes |
| **Status** | draft → review → active → archived (follow lifecycle) |
| **Review** | All specs/ and standards/ need Jon approval before active |
| **Maintenance** | Owner maintains; Quarterly audit; No stale documents allowed |
| **Token discipline** | Never load full files; always use offset/limit based on section markers |
| **Angus's job** | Follow structure, add change log entries, keep references alive, validate before publishing, respect token budget |

---

## 14. Section Markers for Easy Navigation

Large documents (>100 lines) include **section markers** to enable quick offset/limit reading:

```markdown
# Document Title

---
[SECTION: Quick Start — lines 1-50]

Quick reference content here

---
[SECTION: Detailed Reference — lines 51-200]

Detailed content here

---
[SECTION: Examples — lines 201-300]

Examples here
```

**Why:** Allows readers to load specific sections without reading entire file:
```
read file.md offset=51 limit=150  # Load "Detailed Reference" section
```

**Rule:** All documents >100 lines must include section markers at major breaks.

---

## 15. Archive Management & Search Rules

### How to Archive a Document

**When a document is superseded or retired:**

1. **Copy to archive/**
   - Old filename: `DEPLOYMENT-ARCHITECTURE.md`
   - Archived filename: `archive/DEPLOYMENT-ARCHITECTURE_v1.0_archived-2026-02-20.md`
   - Include: full version number + archived date

2. **Delete from active folder**
   - Remove old file from specifications/, design/, etc.
   - It now lives only in archive/

3. **Update INDEX.md**
   - Remove old document link
   - Add new replacement document link (if exists)
   - Add note: "Old: DEPLOYMENT-ARCHITECTURE v1.0, archived 2026-02-20 → see v2.0 above"

4. **Add archive metadata**
   - Create section in archived file: "## Archive Notes"
   - Explain: Why archived, what replaces it, when to reference this version
   - Example:
     ```markdown
     ## Archive Notes
     
     **Archived:** 2026-02-20
     **Reason:** Switched from SQLite to PostgreSQL for production
     **Replaced By:** [DEPLOYMENT-ARCHITECTURE.md v2.0](../DEPLOYMENT-ARCHITECTURE.md) (same folder)
     **Keep For:** Historical reference, rollback decisions
     **Delete After:** 12 months (2027-02-20) if no longer needed
     ```

### Grep & Search Rules

**When searching documentation, ALWAYS exclude archive/:**

```bash
# ❌ DON'T do this (searches archive too)
grep -r "database" E:\poker-project\

# ✅ DO this (excludes archive/)
grep -r "database" E:\poker-project\ --exclude-dir=archive
```

**Git ignore for archive/ (if using version control):**

In `.gitignore`:
```
# Archive files (historical reference only, not in active development)
archive/
```

**Why exclude archive/?**
- Archive is historical reference, not active code
- Searching archive pollutes results with outdated information
- Developers should work with active documents only
- Archive entries can contradict current specs (that's the point — they're old)

**Rules for archive/ folder:**

1. **Never edit archived documents** — They're immutable historical records
2. **Never reference archived docs in active docs** — Links point to active versions only
3. **Never include archive/ in grep/search workflows** — Use `--exclude-dir=archive`
4. **Use archive only for reference** — "Why did we switch? See v1.0 in archive"
5. **Archive can be pruned after 12 months** — Old, superseded docs can be deleted

**Archive Structure:**

```
archive/
├── README.md                                      (explains archive contents)
├── DEPLOYMENT-ARCHITECTURE_v1.0_archived-2026-02-20.md
├── PHASE-3-ARCHITECTURE_v0.9_archived-2026-02-21.md
└── [other retired docs]
```

**archive/README.md example:**

```markdown
# Archive

This folder contains retired documentation. Files here are historical reference only.

**Do not:**
- Link to archive docs in active docs
- Edit or update archive docs
- Use archive docs as source of truth

**Do use for:**
- Understanding why we made architecture changes
- Auditing decision history
- Rollback reference if needed

**Cleanup:**
- Files older than 12 months can be deleted
- Keep audit trail: what was archived, why, when
```

---

**This system is now law. Future documents follow these standards without exception.**

