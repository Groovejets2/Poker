---
name: create-pr
description: Create a pull request for the current branch. Use when a feature, bugfix, or hotfix branch is ready for review. Generates a structured PR body with summary, changes, and test results. Requires GitHub CLI (gh) or uses the GitHub REST API as fallback.
argument-hint: "[base-branch] defaults to develop"
---

# Create PR Skill - OpenClaw Poker Platform

This skill creates a GitHub pull request for the current branch with a structured body,
populated from the git log, test results, and project conventions.

---

## Pre-flight Checks

Before creating the PR, verify:

1. Confirm the working tree is clean: `git status --short` — warn if there are uncommitted changes
2. Identify the current branch: `git branch --show-current`
3. Confirm it is not `main` or `develop` — abort if so with a clear message
4. Determine the base branch:
   - If `$ARGUMENTS` is provided, use it as the base branch
   - If branch starts with `feature/` or `bugfix/` → base = `develop`
   - If branch starts with `release/` or `hotfix/` → base = `main`
   - Default: `develop`
5. Confirm the current branch has been pushed: `git status -sb` — push if behind

---

## Gather PR Content

1. Get the list of commits since diverging from base:
   ```bash
   git log <base-branch>...HEAD --oneline
   ```

2. Get the diff summary (files changed):
   ```bash
   git diff <base-branch>...HEAD --stat
   ```

3. Run tests and capture results. Check exit codes — if any command exits non-zero, abort PR creation and report which tests failed:
   - Backend: `cd backend && npm test 2>&1 | tail -5`
   - Frontend: `cd frontend && npm test 2>&1 | tail -5`
   - Python engine: `cd code && python -m pytest ../tests/ --tb=no -q 2>&1 | tail -3`
   - If any tests fail, stop here. Do not create the PR. Fix the failures first.

4. Read `TASK-BOARD.md` to find the phase tasks completed in this branch. If the phase is not mentioned, extract the phase number from the branch name (e.g., `phase-3.4`) and create a summary from the commit messages.

---

## PR Body Template

Construct the PR body using this structure:

```markdown
## Summary

<1-3 bullet points describing what this PR does, written in plain British English>

## Changes

<list of commits from git log, formatted as bullet points>

## Files Changed

<stat output from git diff — trimmed to key files only if very long>

## Test Results

- Backend: <X passed / X failed>
- Frontend: <X passed / X failed>
- Python engine: <X passed, 0 failed>

## Task Board

Phase <X.Y>: <description>
- [x] <completed task 1>
- [x] <completed task 2>

## Checklist

- [ ] All unit tests passing
- [ ] Integration tested manually
- [ ] Documentation updated (CLAUDE.md, TASK-BOARD.md)
- [ ] No emojis in code or docs
- [ ] British English used throughout
- [ ] Commit messages are clear and descriptive
```

---

## Create the PR

Extract the PR title from the branch name:
- Strip the leading branch type and slash: `feature/2026-02-28_my-feature` → `2026-02-28_my-feature`
- Strip the date prefix (YYYY-MM-DD_): `2026-02-28_my-feature` → `my-feature`
- Replace hyphens with spaces and capitalise the first letter: `My feature`

Detect the repository remote URL to build dynamic API paths:
```bash
git remote get-url origin
# Example output: https://github.com/Groovejets2/Poker.git
# Extract: owner=Groovejets2, repo=Poker
```

### Option A: GitHub CLI (preferred)

Check if `gh` is installed first: `gh --version`

If available:
```bash
gh pr create \
  --base <base-branch> \
  --title "<branch-description>" \
  --body "<constructed-body>"
```

If not installed, fall through to Option B. Note: install with `winget install GitHub.cli`.

### Option B: GitHub REST API (fallback if gh is not installed)

Detect owner and repo from `git remote get-url origin`.

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/<owner>/<repo>/pulls \
  -d '{
    "title": "<title>",
    "body": "<body>",
    "head": "<current-branch>",
    "base": "<base-branch>"
  }'
```

Requires `GITHUB_TOKEN` environment variable. If not set, output the curl command
and tell the user to set `GITHUB_TOKEN` with a personal access token (repo scope).

### Option C: Manual fallback

If neither option works, output:
1. The fully constructed PR body (ready to paste into GitHub)
2. The GitHub URL to create a PR manually — detect from `git remote get-url origin`:
   `https://github.com/<owner>/<repo>/compare/<base-branch>...<current-branch>`

---

## Post-creation Steps

1. Output the PR URL (or manual link)
2. Update `TASK-BOARD.md` to note PR is open for the relevant phase
3. Remind user of review checklist items that need manual verification (browser testing, etc.)

---

## Safety Rules

- Never create a PR from `main` or `develop` to itself
- Never create a PR if tests are failing — fix tests first
- Always include test results in the PR body
- Always target `develop` for features, `main` for hotfixes and releases

---

## Version History

| Date | Version | Change |
|------|---------|--------|
| 2026-02-28 | 1.1 | Fixed: dynamic repo detection, test exit code enforcement, title extraction clarity, TASK-BOARD.md fallback |
| 2026-02-28 | 1.0 | Initial creation for Phase 3.4 |

**Status:** APPROVED
**Owner:** Jon + Development Team
