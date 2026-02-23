# Git Flow Strategy - OpenClaw Poker Project

**Effective Date:** 2026-02-20
**Version:** 1.0

---

## Overview

This project uses a modified Git Flow model with strict branch discipline:

- **main** — Production-ready code only (tagged releases)
- **develop** — Integration branch for completed features
- **feature/** — Feature branches from develop
- **release/** — Release preparation branches
- **hotfix/** — Emergency fixes to production

---

## Branch Strategy

### Main Branch
- **Protected:** Yes (no direct commits)
- **Purpose:** Production-ready code only
- **Tags:** All releases tagged here (vX.X.X)
- **Merge from:** release/ and hotfix/ only
- **Merge back to:** develop (release closes)

### Develop Branch
- **Protected:** Yes (PRs required)
- **Purpose:** Integration point for completed features
- **Source:** feature/ branches merge here via PR
- **Target:** Features must be code-reviewed before merge

### Feature Branches
- **Naming:** `feature/YYYY-MM-DD_brief-description`
- **Source:** Branch from develop
- **Merge back:** PR into develop (require 1 approval minimum)
- **Deletion:** Delete after merge
- **Lifetime:** Keep short (1-3 days max)

**Example:**
```
feature/2026-02-20_hand-evaluation-engine
feature/2026-02-21_dealer-state-machine
```

### Release Branches
- **Naming:** `release/vX.X.X` (semantic versioning)
- **Source:** Branch from develop
- **Purpose:** Final testing and bug fixes before production
- **Merge to:** main (tag as vX.X.X) and back to develop
- **Lifetime:** Until release is tagged on main

**Example:**
```
release/v1.0.0
release/v1.1.0
```

### Hotfix Branches
- **Naming:** `hotfix/vX.X.X_brief-description`
- **Source:** Branch from main
- **Purpose:** Critical production fixes only
- **Merge to:** main (tag) and develop
- **Lifetime:** Until merged to main

**Example:**
```
hotfix/v1.0.1_hand-rank-calculation-bug
```

---

## Commit Message Standards

**Format:** `YYYY-MM-DD | Category | Brief description`

**Categories:**
- `FEAT` — New feature
- `FIX` — Bug fix
- `REFACTOR` — Code restructuring (no functional change)
- `TEST` — Test additions or modifications
- `DOCS` — Documentation updates
- `CHORE` — Build, dependency, or tooling changes

**Examples:**

```
2026-02-20 | FEAT | Implement hand evaluation engine with unit tests
2026-02-20 | FIX | Correct royal flush detection logic
2026-02-20 | TEST | Add 25 test cases for hand rankings
2026-02-20 | REFACTOR | Extract hand rank calculation to separate function
2026-02-20 | DOCS | Add docstrings to HandEvaluator class
```

**Guidelines:**
- One logical change per commit
- Write in imperative mood: "Add feature" not "Added feature"
- If commit addresses multiple areas, split into multiple commits
- Keep message body brief; add details only if necessary

---

## Pull Request (PR) Standards

### Before Creating a PR

1. Branch from develop (for features)
2. Make commits following standards above
3. Run all tests locally and ensure they pass
4. Update relevant documentation
5. Ensure code follows CODING_STANDARDS.md

### PR Checklist

```
Title: feature/2026-02-20_hand-eval: Implement hand evaluation engine

Description:
- Implements HandEvaluator class
- Supports 5-card and Texas Hold'em evaluation
- 25 unit tests added, all passing
- Docstrings complete
- No code duplication (DRY applied)

Closes: (link to task if applicable)

Checklist:
- [ ] Code follows CODING_STANDARDS.md
- [ ] All tests pass locally
- [ ] New code has unit tests
- [ ] Documentation updated
- [ ] No merge conflicts
```

### Merge Requirements

- Minimum 1 approval (Jon or code reviewer)
- All tests must pass
- No conflicts with develop
- Code review comments addressed
- Squash commits if there are multiple small commits (optional but recommended)

---

## Release Process

### Creating a Release

1. Create `release/vX.X.X` branch from develop
2. Update version numbers in code/config (if applicable)
3. Final testing and bug fixes only (no new features)
4. Create PR from release/ to main
5. Once approved, merge to main and tag

### Tagging

**Format:** `vX.X.X` (semantic versioning)

**Semantic Versioning:**
- **MAJOR** — Breaking changes
- **MINOR** — New features (backward compatible)
- **PATCH** — Bug fixes only

**Examples:**
```
v1.0.0 — Initial release
v1.1.0 — New feature added
v1.1.1 — Bug fix
v2.0.0 — Major refactor with breaking changes
```

**Tag Command:**
```bash
git tag -a v1.0.0 -m "Release v1.0.0: Hand evaluation and dealer engine"
git push origin v1.0.0
```

### After Release

1. Merge main back into develop
2. Delete release/ branch
3. Continue feature work on develop

---

## Example Workflow

### Feature Development

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/2026-02-20_hand-eval

# Make commits
git commit -m "2026-02-20 | FEAT | Implement hand evaluation engine"
git commit -m "2026-02-20 | TEST | Add unit tests for hand rankings"

# Push and create PR
git push origin feature/2026-02-20_hand-eval
# Create PR on GitHub: feature/2026-02-20_hand-eval → develop

# After approval and merge
git checkout develop
git pull origin develop
git branch -d feature/2026-02-20_hand-eval
```

### Release Workflow

```bash
# Prepare release
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Final fixes
git commit -m "2026-02-20 | FIX | Correct hand rank edge cases"

# Merge to main
git checkout main
git pull origin main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main
git push origin v1.0.0

# Merge back to develop
git checkout develop
git merge --no-ff main
git push origin develop

# Cleanup
git branch -d release/v1.0.0
```

### Hotfix Workflow

```bash
# Emergency fix
git checkout main
git pull origin main
git checkout -b hotfix/v1.0.1_bug-fix

# Fix and test
git commit -m "2026-02-20 | FIX | Correct hand evaluation bug"

# Merge to main
git checkout main
git merge --no-ff hotfix/v1.0.1_bug-fix
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git push origin main
git push origin v1.0.1

# Merge to develop
git checkout develop
git merge --no-ff main
git push origin develop

# Cleanup
git branch -d hotfix/v1.0.1_bug-fix
```

---

## Commands Reference

```bash
# Clone repository
git clone <url>

# List branches
git branch -a

# Create and switch to feature branch
git checkout -b feature/2026-02-20_description

# Commit with proper message
git commit -m "2026-02-20 | FEAT | Description"

# Push branch
git push origin feature/2026-02-20_description

# Switch back to develop
git checkout develop

# Pull latest develop
git pull origin develop

# Merge feature (after PR approval)
git merge feature/2026-02-20_description

# Delete local branch
git branch -d feature/2026-02-20_description

# Delete remote branch
git push origin --delete feature/2026-02-20_description

# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0"

# Push tag to remote
git push origin v1.0.0

# View commit log
git log --oneline --all --graph
```

---

## Rules

1. **Never commit directly to main or develop**
2. **All work must be in a feature/ branch**
3. **PRs require approval before merge**
4. **All tests must pass before merge**
5. **Releases must be tagged on main**
6. **Commit messages must follow format**
7. **Feature branches deleted after merge**
8. **Hotfixes only for production bugs**

---

**Document Created:** 2026-02-20 00:00 GMT+13
**Version:** 1.0
**Status:** APPROVED
