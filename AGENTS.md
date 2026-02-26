# AGENTS.md - AI Agent Instructions & Quality Standards

**Category:** standards
**Purpose:** Mandatory instructions for all AI agents working on this project
**Version:** 1.0
**Created:** 2026-02-26
**Owner:** Jon + Development Team
**Tags:** agent-instructions, quality-standards, testing-requirements, api-contracts

---

## 🚨 CRITICAL - READ BEFORE ANY CODING TASK

**These are MANDATORY requirements. Failure to follow results in broken code.**

---

## 1. API Integration - ZERO TOLERANCE FOR ASSUMPTIONS

### BEFORE Writing Any API Integration Code:

**❌ NEVER assume API response structure**
**✅ ALWAYS verify actual API responses first**

#### Mandatory Steps for API Work:

1. **Test the actual endpoint first:**
   ```bash
   # Example for tournaments endpoint
   curl http://localhost:5000/api/tournaments

   # Check what structure is ACTUALLY returned:
   # Is it an array? { tournaments: [] }? { data: [] }?
   # What are the field names? buy_in or buy_in_chips?
   ```

2. **Document the actual response structure:**
   ```typescript
   // BAD - Assumed structure
   interface Tournament {
     buy_in: number;  // WRONG! Backend uses buy_in_chips
   }

   // GOOD - Verified structure
   interface TournamentBackendResponse {
     tournaments: Array<{
       id: number;
       buy_in_chips: number;  // Verified via curl
       entry_fee_usd: number;  // Verified via curl
       // ... etc
     }>;
     pagination: {...};
   }
   ```

3. **Create mapping layer if needed:**
   ```typescript
   // If backend and frontend use different conventions,
   // create explicit mapping
   async getAll(): Promise<Tournament[]> {
     const response = await apiClient.get('/tournaments');
     const data = response.data.tournaments || response.data;

     return data.map((t: any) => ({
       ...t,
       buy_in: t.buy_in_chips,  // Map backend → frontend
       entry_fee: t.entry_fee_usd,
     }));
   }
   ```

4. **Test the integration manually:**
   - Start both backend and frontend
   - Open browser DevTools → Network tab
   - Click the feature that calls the API
   - Verify the request succeeds and data displays correctly

### API Contract Violations (Recent Failures):

**2026-02-26 - Phase 3.2 Frontend:**
- ❌ Assumed `/api/tournaments` returns array directly → Actually returns `{ tournaments: [] }`
- ❌ Used `buy_in` field → Backend uses `buy_in_chips`
- ❌ Used `entry_fee` field → Backend uses `entry_fee_usd`
- ❌ Assumed login returns `{ token, user: {...} }` → Actually flat object `{ token, user_id, username, role }`
- **Result:** "Failed to load tournaments" error, complete site breakage

---

## 2. Testing Requirements - ALL Tests MUST Pass

### Unit Tests (MUST pass before completion):

```bash
# Backend tests - ALL must pass
cd backend && npm test

# Frontend tests - ALL must pass
cd frontend && npm test
```

**❌ DO NOT mark phase complete if tests are failing**
**✅ Fix ALL test failures before moving on**

### Integration Tests (MANDATORY):

**After any API integration work:**

1. **Start both servers:**
   ```bash
   # Terminal 1
   cd backend && npm start

   # Terminal 2
   cd frontend && npm run dev
   ```

2. **Manual test ALL affected features:**
   - Click every button
   - Fill every form
   - Navigate all routes
   - Check browser console for errors
   - Verify data displays correctly

3. **Document test results:**
   ```markdown
   Integration Test Results:
   - ✅ Register new user → Success, redirects to /tournaments
   - ✅ Login → Success, JWT stored, redirects correctly
   - ✅ View tournaments → All 3 tournaments display
   - ✅ View leaderboard → 2 players display
   - ✅ Navigation → All links work
   ```

### CSS/Styling Tests:

**Before marking styling work complete:**

1. Hard refresh browser (Ctrl+Shift+R)
2. Check browser console for CSS errors
3. Verify fonts load (DevTools → Network → filter:font)
4. Check responsive design (resize browser window)
5. Test on multiple screen sizes

### Test Failure Response:

**When tests fail:**
1. ❌ DO NOT ignore failures
2. ❌ DO NOT mark task complete
3. ✅ Investigate the failure
4. ✅ Fix the root cause
5. ✅ Re-run tests until ALL pass
6. ✅ Document what was fixed

---

## 3. Documentation Requirements

### Update These Files After Every Phase:

1. **CLAUDE.md** - Current status, what's complete, next steps
2. **TASK-BOARD.md** - Mark tasks complete, update phase status
3. **Commit messages** - Clear explanation of what changed and why

### Commit Message Standards:

```bash
# GOOD commit messages
git commit -m "fix: Map backend API responses to frontend structures

Frontend services now handle actual backend response formats:
- Tournaments: Extract from { tournaments: [] } wrapper
- Auth: Map flat response to { token, user } structure
- Field mappings: buy_in_chips → buy_in, user_id → id

Fixes: 'Failed to load tournaments' error"

# BAD commit messages
git commit -m "fix stuff"
git commit -m "update code"
git commit -m "wip"
```

---

## 4. CSS & Frontend Asset Rules

### Google Fonts / External Assets:

**✅ ALWAYS put external resources in HTML `<head>`:**
```html
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/..." rel="stylesheet" />
</head>
```

**❌ NEVER use `@import` for external fonts in CSS:**
```css
/* WRONG - Causes PostCSS errors */
@import url('https://fonts.googleapis.com/...');
@import "tailwindcss";

/* RIGHT - TailwindCSS first, no external imports */
@import "tailwindcss";
```

**Why:** TailwindCSS expands before the font import, violating CSS `@import` order rules.

### Recent CSS Failure (2026-02-26):
- ❌ Used `@import url('...')` for Google Fonts in CSS
- **Result:** PostCSS error, blank white screen, site completely broken
- ✅ **Fix:** Moved fonts to HTML `<head>` with preconnect

---

## 5. Phase Completion Checklist

**Before marking ANY phase complete:**

- [ ] All unit tests passing (`npm test` in both backend and frontend)
- [ ] All integration tests verified manually
- [ ] Both servers started and tested together
- [ ] Browser console has NO errors
- [ ] All features work as expected (clicked every button)
- [ ] API responses verified with curl/Postman
- [ ] CSS loads without errors (check Network tab)
- [ ] Responsive design tested (resize browser)
- [ ] CLAUDE.md updated with completion status
- [ ] TASK-BOARD.md updated with ✅ checkmarks
- [ ] All code committed with clear messages
- [ ] All commits pushed to remote
- [ ] User has tested the feature (if requested)

**⚠️ If ANY checkbox is unchecked, phase is NOT complete**

---

## 6. Common Mistakes to AVOID

### API Integration:
- ❌ Assuming response structure without checking
- ❌ Mismatched field names (buy_in vs buy_in_chips)
- ❌ Not handling wrapped responses ({ data: [] } vs [])
- ❌ Skipping manual integration testing

### Testing:
- ❌ Ignoring test failures ("I'll fix them later")
- ❌ Not running tests before marking complete
- ❌ Only running unit tests, skipping integration tests

### CSS/Styling:
- ❌ Using `@import` for external fonts in CSS
- ❌ Not checking browser console for errors
- ❌ Not doing hard refresh after CSS changes

### Documentation:
- ❌ Vague commit messages
- ❌ Not updating CLAUDE.md after completion
- ❌ Not documenting test results

---

## 7. When Starting a New Task

**Step 1: Read Task Requirements**
- TASK-BOARD.md → Find current phase and tasks
- CLAUDE.md → Check current status and blockers

**Step 2: Understand Dependencies**
- What APIs will I use? → Test them first with curl
- What data structures? → Check actual backend responses
- What tests exist? → Read test files to understand expectations

**Step 3: Plan Before Coding**
- Write down expected API responses
- Create data mapping layer if needed
- Identify potential mismatches

**Step 4: Code with Verification**
- Write code
- Run tests continuously
- Check browser console frequently
- Use curl to verify API calls

**Step 5: Complete with Quality**
- ALL tests pass
- Manual integration test complete
- Documentation updated
- Code committed and pushed

---

## 8. Emergency Recovery Procedures

### If Site is Broken:

1. **Check browser console first:**
   - F12 → Console tab
   - Look for red errors
   - Note the exact error message

2. **Check server logs:**
   ```bash
   # Backend errors
   cd backend && npm start
   # Watch terminal for errors

   # Frontend errors
   cd frontend && npm run dev
   # Watch terminal for CSS/PostCSS errors
   ```

3. **Test API directly:**
   ```bash
   # Health check
   curl http://localhost:5000/health

   # Test broken endpoint
   curl http://localhost:5000/api/tournaments
   ```

4. **Check recent commits:**
   ```bash
   git log --oneline -5
   # What changed recently?
   # Can we revert?
   ```

5. **Fix systematically:**
   - Identify root cause
   - Fix one issue at a time
   - Test after each fix
   - Don't move on until working

---

## 9. Quality Standards

**Code is NOT done until:**
- ✅ It works in production (both servers running)
- ✅ ALL tests pass
- ✅ User has tested (if requested)
- ✅ No console errors
- ✅ Documentation updated
- ✅ Committed with clear message

**"It works on my machine" is NOT acceptable**
**"Tests pass but feature doesn't work" is NOT acceptable**
**"I'll fix it later" is NOT acceptable**

---

## 10. Agent Responsibilities

**As an AI agent on this project, I am responsible for:**

1. **Quality Over Speed** - Take time to verify API contracts
2. **Testing Everything** - Unit tests + integration tests
3. **Clear Communication** - Document what I did and why
4. **User Experience** - If it's broken for the user, it's broken
5. **Learning from Mistakes** - Read this file before every task

**I will NOT:**
- ❌ Assume API structures without testing
- ❌ Mark tasks complete when tests fail
- ❌ Skip manual integration testing
- ❌ Ignore browser console errors
- ❌ Write vague commit messages

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-26 | 1.0 | Initial creation after Phase 3.2 API failures |

---

**Last Updated:** 2026-02-26
**Next Review:** After any major quality incident

**This document is MANDATORY reading before starting any development task.**
