---
name: gitflow
description: GitFlow workflow automation for the OpenClaw Poker project. Use when creating branches, merging features, cutting releases, or applying hotfixes. Enforces branching conventions and merge order.
argument-hint: "[action] e.g. feature-start, feature-finish, release-start, release-finish, hotfix-start, hotfix-finish"
---

# GitFlow Skill - OpenClaw Poker Platform

This skill automates the GitFlow branching workflow. It enforces conventions and merge order
to keep the repository clean and release-ready at all times.

---

## Branch Conventions

| Branch Type | Pattern | Base Branch | Merges Into |
|-------------|---------|-------------|-------------|
| Feature | `feature/YYYY-MM-DD_short-description` | `develop` | `develop` |
| Release | `release/X.Y.Z` | `develop` | `main` + `develop` |
| Hotfix | `hotfix/YYYY-MM-DD_short-description` | `main` | `main` + `develop` |
| Bugfix | `bugfix/YYYY-MM-DD_short-description` | `develop` | `develop` |

**Main branches:**
- `main` — production-ready code only; every commit is a deployable release
- `develop` — integration branch; all features merge here first

---

## Actions

The argument `$ARGUMENTS` determines which action to run. Parse it and follow the matching
section below.

---

### feature-start

**Usage:** `/gitflow feature-start <description>`

Steps:
1. Confirm working tree is clean: `git status --short` — abort if dirty
2. Switch to develop and pull latest: `git checkout develop && git pull origin develop`
3. Create feature branch with today's date: `git checkout -b feature/YYYY-MM-DD_<description>`
   - Use today's date in YYYY-MM-DD format
   - Replace spaces with hyphens in the description
4. Push and set upstream: `git push -u origin feature/YYYY-MM-DD_<description>`
5. Report the new branch name to the user

---

### feature-finish

**Usage:** `/gitflow feature-finish [branch-name]`

If branch-name is omitted, use the current branch.

Steps:
1. Confirm current branch matches `feature/*` pattern — abort if not
2. Confirm working tree is clean: `git status --short` — commit or stash any changes first
3. Run all tests before merging:
   - Backend: `cd backend && npm test`
   - Frontend: `cd frontend && npm test`
   - Python engine: `cd code && python -m pytest ../tests/ -v --tb=short`
   - Abort if any tests fail; report which tests failed
4. Switch to develop: `git checkout develop && git pull origin develop`
5. Merge the feature branch (no fast-forward): `git merge --no-ff <feature-branch> -m "Merge <feature-branch> into develop"`
6. Push develop: `git push origin develop`
7. Delete the local feature branch: `git branch -d <feature-branch>`
8. Delete the remote feature branch: `git push origin --delete <feature-branch>`
9. Report completion and suggest next step (create PR or start new feature)

---

### release-start

**Usage:** `/gitflow release-start <version>` e.g. `/gitflow release-start 0.3.0`

Steps:
1. Confirm working tree is clean
2. Switch to develop and pull: `git checkout develop && git pull origin develop`
3. Verify all tests pass (backend + frontend + python engine) — abort if any fail
4. Create release branch: `git checkout -b release/<version>`
5. Bump version in `package.json` (backend and frontend both):
   - Update `"version"` field to `<version>`
6. Commit the version bump: `git commit -am "chore: Bump version to <version> for release"`
7. Push release branch: `git push -u origin release/<version>`
8. Report the release branch name and remind user to do final testing

---

### release-finish

**Usage:** `/gitflow release-finish <version>`

Steps:
1. Confirm current branch is `release/<version>`
2. Confirm working tree is clean
3. Run full test suite — abort if any failures
4. Merge into main: `git checkout main && git pull origin main && git merge --no-ff release/<version> -m "Release v<version>"`
5. Tag the release: `git tag -a v<version> -m "Release v<version>"`
6. Push main with tags: `git push origin main && git push origin --tags`
7. Merge back into develop: `git checkout develop && git merge --no-ff release/<version> -m "Merge release/<version> back into develop"`
8. Push develop: `git push origin develop`
9. Delete release branch locally and remotely: `git branch -d release/<version> && git push origin --delete release/<version>`
10. Update `CLAUDE.md` and `TASK-BOARD.md` with the new version and completion status
11. Report success with the tag name

---

### hotfix-start

**Usage:** `/gitflow hotfix-start <description>`

Steps:
1. Confirm working tree is clean
2. Switch to main and pull: `git checkout main && git pull origin main`
3. Create hotfix branch: `git checkout -b hotfix/YYYY-MM-DD_<description>`
4. Push and set upstream: `git push -u origin hotfix/YYYY-MM-DD_<description>`
5. Report the branch name and remind user to fix only the specific issue

---

### hotfix-finish

**Usage:** `/gitflow hotfix-finish <version>`

Steps:
1. Confirm current branch matches `hotfix/*` — abort if not
2. Confirm working tree is clean
3. Run full test suite — abort if any failures
4. Read the current version from `backend/package.json` and increment the patch version
5. Commit the fix: `git commit -am "fix: <description> (hotfix v<version>)"`
6. Merge into main: `git checkout main && git merge --no-ff <hotfix-branch> -m "Hotfix v<version>: <description>"`
7. Tag: `git tag -a v<version> -m "Hotfix v<version>"`
8. Push main + tags: `git push origin main && git push origin --tags`
9. Merge into develop: `git checkout develop && git merge --no-ff <hotfix-branch> -m "Merge hotfix into develop"`
10. Push develop: `git push origin develop`
11. Delete hotfix branch: `git branch -d <hotfix-branch> && git push origin --delete <hotfix-branch>`
12. Update `CLAUDE.md` with hotfix notes
13. Report completion

---

## Safety Rules

- Never commit directly to `main` or `develop` — always use feature/release/hotfix branches
- Never merge to `main` without all tests passing
- Never skip the merge-back-to-develop step after a release or hotfix
- Never delete `main` or `develop` branches
- Always use `--no-ff` merges to preserve branch history
- If the working tree is dirty, stop and tell the user to commit or stash first

---

## Version History

| Date | Version | Change |
|------|---------|--------|
| 2026-02-28 | 1.0 | Initial creation for Phase 3.4 |

**Status:** APPROVED
**Owner:** Jon + Development Team
