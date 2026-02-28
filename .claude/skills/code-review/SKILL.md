---
name: code-review
description: Perform a structured peer code review of the current branch or a specified set of files. Use when a feature is complete and ready for review before merging. Analyses code quality, logic, tests, documentation, and standards compliance.
argument-hint: "[branch-or-file] defaults to current branch vs develop"
---

# Code Review Skill - OpenClaw Poker Platform

This skill performs a structured peer code review. It analyses the diff against the base branch
and produces a written review report covering correctness, quality, standards, and risks.

---

## Review Scope

1. Determine what to review:
   - If `$ARGUMENTS` is a branch name: diff that branch against `develop`
   - If `$ARGUMENTS` is a file path: review that file
   - If no argument: diff current branch against `develop`

2. Gather the diff:
   ```bash
   git diff develop...HEAD
   ```

3. Also read any new or heavily modified files in full for context

---

## Review Checklist

Work through each section. For each item, mark it PASS, FAIL, or N/A with a brief note.

### 1. Correctness

- Logic is correct and handles edge cases
- No off-by-one errors or boundary condition mistakes
- Error handling is present and correct
- No silent failures (bare except, swallowed errors)
- Database operations are safe (no raw SQL injection risks)
- API response shapes match the actual backend contracts (see `AGENTS.md`)

### 2. Test Coverage

- New code has corresponding unit tests
- Tests cover happy path and at least one failure/edge case
- All existing tests still pass
- No tests were deleted without a documented reason
- Integration tests exist for any new API endpoints

### 3. Code Quality

- Functions and variables have clear, descriptive names
- No duplicated logic (DRY principle applied)
- Functions are focused — doing one thing
- No commented-out dead code left in
- No TODO/FIXME comments left in production code without a linked task
- Complexity is reasonable — no deeply nested conditionals without justification

### 4. TypeScript Standards (frontend + backend)

- All variables and parameters have explicit types — no implicit `any`
- Interfaces used for object shapes, not inline types for reuse
- `unknown` used instead of `any` where type is genuinely unknown
- No `as any` casts without a comment explaining why
- Async functions return `Promise<T>` with explicit types
- Null/undefined handled with optional chaining (`?.`) or explicit guards
- See `docs/standards/CODING_STANDARDS.md` for full rules

### 5. Python Standards (poker engine)

- Type hints present on all function signatures
- No bare `except:` clauses — always catch specific exceptions
- Docstrings on public methods
- No mutable default arguments
- British English in comments and docstrings

### 6. Documentation Standards

- No emojis in any files (code, docs, or comments)
- British English spelling throughout
- CLAUDE.md updated if phase or status changed
- TASK-BOARD.md tasks marked complete
- Commit messages are clear and follow the project format
- No new documents created when an existing one should have been updated

### 7. Security

- No secrets, tokens, or passwords in code or comments
- JWT handling follows existing patterns (no new fallback secrets)
- User input is validated before use
- No new SQL queries bypass the ORM without justification

### 8. Performance

- No N+1 database queries introduced
- No unbounded loops over large datasets without pagination
- No synchronous I/O in async code paths

---

## Review Report Format

Produce a report in this structure:

```
Code Review Report
Branch: <branch-name>
Date: <today>
Reviewer: Claude (Sonnet 4.6)

OVERALL VERDICT: APPROVED | APPROVED WITH COMMENTS | CHANGES REQUIRED

Summary
<1-3 sentences on overall quality>

Issues Found

CRITICAL (must fix before merge):
- <file>:<line> — <description>

HIGH (strongly recommended):
- <file>:<line> — <description>

MEDIUM (improvements to consider):
- <file>:<line> — <description>

LOW (minor suggestions):
- <file>:<line> — <description>

Checklist Results
[PASS/FAIL/N/A] Correctness
[PASS/FAIL/N/A] Test Coverage
[PASS/FAIL/N/A] Code Quality
[PASS/FAIL/N/A] TypeScript Standards
[PASS/FAIL/N/A] Python Standards
[PASS/FAIL/N/A] Documentation Standards
[PASS/FAIL/N/A] Security
[PASS/FAIL/N/A] Performance

Recommendation
<Specific next steps — fix X before merging, or ready to merge>
```

---

## Verdict Definitions

- **APPROVED** — No issues or only LOW suggestions. Ready to merge.
- **APPROVED WITH COMMENTS** — MEDIUM issues found but no blockers. Can merge after noting them.
- **CHANGES REQUIRED** — CRITICAL or HIGH issues found. Must be fixed and re-reviewed before merging.

---

## Agent Behaviour During Review

- Be direct and objective. Do not soften findings to avoid conflict.
- If logic is wrong, say it is wrong and explain why.
- If a better approach exists, describe it clearly.
- Do not approve code that violates AGENTS.md rules.
- Challenge design decisions when there is a clearly better alternative.
- PRs exist to improve code quality, not just to tick a box.

---

## Version History

| Date | Version | Change |
|------|---------|--------|
| 2026-02-28 | 1.0 | Initial creation for Phase 3.4 |

**Status:** APPROVED
**Owner:** Jon + Development Team
