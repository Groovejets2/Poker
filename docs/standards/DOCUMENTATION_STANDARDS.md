# Documentation Standards - OpenClaw Poker Project

**Effective Date:** 2026-02-19
**Version:** 1.1
**Last Updated:** 2026-02-26 21:30 GMT+13

---

## Purpose

This document establishes strict, clinical documentation standards for the OpenClaw Poker Project to ensure consistency, traceability, and professional quality across all project artefacts.

---

## Storage and Organisation

### Location
- **Primary Location:** E:\poker-project\
- **Secondary Location:** None (do not use C: drive, do not use media/movie drives)
- **External Location:** Not permitted

### Folder Structure
```
E:\poker-project\
├── specifications/      (functional requirements, architectural specs)
├── design/             (design documents, API specs, schemas)
├── code/               (source code and scripts)
├── tests/              (test cases and results)
└── archive/            (superseded documents)
```

### Naming Convention

**Format:** YYYY-MM-DD_document-name_vX.X.md

**Examples:**
- `2026-02-19_project-charter_v1.0.md`
- `2026-02-19_dealer-requirements_v1.1.md`
- `2026-02-20_hand-evaluation-spec_v1.0.md`

**Rules:**
- Date is ISO 8601 format (YYYY-MM-DD)
- Document name is lowercase with hyphens
- Version follows semantic versioning (vMAJOR.MINOR)
- All files are Markdown (.md) unless specified otherwise

---

## Version Control

### Semantic Versioning

- **v1.0** — Initial version
- **v1.1** — Minor corrections, clarifications, no structural changes
- **v1.2, v1.3, etc.** — Additional minor updates
- **v2.0** — Major changes, significant restructuring, or complete rewrite
- **v3.0+** — Reserved for major revisions

### Document Creation Policy

**MANDATORY: Check for Existing Documents First**

Before creating ANY new document:
1. **Search** the `docs/` folder for similar documents
2. **Check** the relevant INDEX.md file
3. **Ask:** Does a document with this purpose already exist?
4. **If YES:** Update the existing document (bump version) instead of creating a new one
5. **If NO:** Proceed with new document creation

**Examples of Violations:**
- Creating `CURRENT_SESSION_STATE.md` when `RESUME_STATE.md` already exists
- Creating `API-SPEC-v2.md` when `API-SPECIFICATION.md` should be updated
- Creating `SETUP-NEW.md` when `SETUP-GUIDE.md` should be revised

**Penalty for Violation:** Document must be consolidated immediately

### Archival Process

When a document is superseded:
1. Do not delete it
2. Move it to `archive/` folder
3. Rename it with suffix `_ARCHIVED` before the version number
4. Example: `2026-02-19_project-charter_v1.0_ARCHIVED.md`
5. Create a note in the INDEX referencing the new version

---

## Formatting Rules

### Language
- **Mandatory:** British English spelling and vocabulary
- **Examples:** "colour" (not "color"), "organisation" (not "organization"), "realise" (not "realize")

### Style
- **No emojis, icons, or decorative symbols**
- Plain text formatting only
- Use standard Markdown for structure (headings, lists, tables)
- Avoid ALL CAPS except for acronyms (e.g., API, MVP, USD, GMT)

### Structure

**Every document must include:**

1. **Title** — Clear, descriptive heading
2. **Metadata** — At the bottom:
   - Document Created: YYYY-MM-DD HH:MM GMT+13
   - Version: X.X
   - Status: DRAFT | APPROVED | IN PROGRESS | SUPERSEDED
3. **Table of Contents** — For documents longer than 1000 words
4. **Introduction/Purpose** — 1-2 sentences explaining the document's purpose
5. **Body Content** — Logically organised sections
6. **Conclusion/Summary** — Recap of key points (if applicable)

### Markdown Standards

**Headings:**
```
# Title (h1 — only one per document)
## Section (h2)
### Subsection (h3)
#### Detail (h4 — use sparingly)
```

**Lists:**
```
- Bullet point
- Another point
  - Nested point

1. Numbered item
2. Second item
   1. Nested numbered
```

**Emphasis:**
- *italics* for minor emphasis
- **bold** for important terms or concepts
- `code` for technical terms, filenames, commands

**Tables:**
Use Markdown pipe tables. Avoid complex formatting.

```
| Column A | Column B |
|----------|----------|
| Cell 1   | Cell 2   |
```

**Avoid:**
- Colour-based formatting
- Decorative dividers (use blank lines instead)
- Excessive indentation
- Non-standard characters

---

## Data Files

### CSV Format
For structured data (task boards, budgets, logs):

**Naming:** YYYY-MM-DD_data-name_v1.0.csv

**Header Row Required:**
- First row must be column headers
- Use standard CSV format (comma-separated values)
- Escape commas in fields with quotes: `"value, with comma"`

**Example:**
```
Task ID,Task Name,Status,Token Budget,Actual Tokens,Date
1.1,Hand Evaluation,READY,1000,0,2026-02-19
```

---

## Code Documentation

### README per phase
Each Phase should have a README.md in the code/ folder:
- `E:\poker-project\code\PHASE_1_README.md`
- `E:\poker-project\code\PHASE_2_README.md`
- etc.

### Code Comments
- Use British English
- Comment complex logic, not obvious code
- No emojis in comments

---

## Git Integration

### Commit Messages
Format: `YYYY-MM-DD | Category | Brief description`

**Categories:** SPEC, DESIGN, CODE, TEST, FIX, ARCHIVE

**Examples:**
```
2026-02-19 | SPEC | Initial project charter v1.0
2026-02-19 | DESIGN | Task board created
2026-02-20 | CODE | Hand evaluation engine skeleton
```

### Repository Root
- `.gitignore` must exclude `archive/` from tracking
- All versioned documents tracked in Git
- Binary files (.exe, .dll) excluded

---

## Review and Approval

### Before Publication
1. Document is written and saved with vX.X versioning
2. Author (me) prepares document
3. Approval required from: Jon (Project Lead)
4. Once approved, Status: APPROVED
5. Document is committed to Git

### Change Control
- All significant changes to approved documents require new version
- Minor typo fixes can update Status to vX.X without requoting approval (e.g., v1.0 to v1.1)
- Structural changes = new major version (v1.0 to v2.0)

---

## Quality Checklist

Before submitting any document, confirm:

- [ ] Correct naming convention (YYYY-MM-DD_name_vX.X.md)
- [ ] Saved in correct folder (specifications/, design/, code/, tests/, or archive/)
- [ ] British English spelling and vocabulary
- [ ] No emojis or icons
- [ ] Metadata block at bottom with date, version, status
- [ ] No formatting clutter or excessive emphasis
- [ ] Clear, professional tone
- [ ] Logically structured with headings
- [ ] All code snippets in backticks or code blocks
- [ ] Git commit message prepared

---

## Deviations

Any deviation from these standards requires written approval from Jon before implementation.

---

**Document Created:** 2026-02-19 23:12 GMT+13
**Version:** 1.0
**Status:** APPROVED
**Authority:** Jon (Project Lead), Angus-Plex (Documentation Lead)
