# RESUME STATE - 2026-02-26 21:50 GMT+13

## Current Situation

**Status:** Phase 3.2 - API Integration Issues Fixed (Partially)
**Branch:** `feature/2026-02-24_phase-3.2-frontend-lobby-leaderboard`
**Servers Running:** Backend (port 5000), Frontend (port 5175)

## What Just Happened

### Problems Found & Fixed:
1. ✅ CSS PostCSS error - Moved Google Fonts to HTML head
2. ✅ API response structure mismatches - Added mapping layers
3. ✅ Field name inconsistencies - Temporary mappings created
4. ✅ Created AGENTS.md - Mandatory quality standards document

### Current Code State:
- **Frontend services** have TEMPORARY mapping layers converting backend field names
- **Backend** uses: `buy_in_chips`, `entry_fee_usd`, `tournament_wins`, `user_id`
- **Frontend** expects: `buy_in`, `entry_fee`, `tournaments_won`, `id`

### Temporary Mappings (NEED TO BE REMOVED):
```typescript
// In tournaments.service.ts
return tournaments.map((t: any) => ({
  ...t,
  buy_in: t.buy_in_chips,  // TEMPORARY
  entry_fee: t.entry_fee_usd,  // TEMPORARY
}));

// In leaderboard.service.ts
return leaderboard.map((player: any) => ({
  ...player,
  tournaments_won: player.tournament_wins,  // TEMPORARY
}));

// In auth.service.ts
return {
  token: response.data.token,
  user: {
    id: response.data.user_id,  // TEMPORARY
    username: response.data.username,
    email: response.data.email || '',
    role: response.data.role || 'player',
  },
};
```

## User Feedback

**Jon's Feedback:**
- ✅ Responsive design is PERFECT (layout, organization, screen size adaptation)
- ⚠️ Graphically needs MORE work (no graphics, boring, fonts just ok)
- ✅ Prefers `buy_in_chips` naming style over `buy_in`

## Next Tasks (ORDERED)

### 1. Save Current State ✅ (THIS FILE)

### 2. Create/Amend API Design Document
**Action:** Create comprehensive API specification with:
- Locked JSON contract for all endpoints
- Field naming standards guide
- Examine frontend vs backend naming conventions
- Pick best combined approach (prefer backend style: `buy_in_chips`)
- Document ALL endpoints with exact request/response formats

**Files to create/update:**
- `docs/specifications/API-SPECIFICATION.md` (comprehensive API contract)
- `docs/standards/API-FIELD-NAMING-GUIDE.md` (naming conventions)

### 3. Fix Frontend to Match API Spec
**Action:** Remove all temporary mapping layers, update frontend to use backend field names
- Update TypeScript interfaces
- Update component code
- Update test expectations

### 4. Run Unit Tests
**Action:** Verify all tests pass after changes
```bash
cd backend && npm test  # Should pass: 43/53 (10 RBAC failures known)
cd frontend && npm test  # Should pass: 16/16
```

### 5. Integration Test
**Action:** Manual testing with both servers running
- Register user
- Login
- View tournaments
- View leaderboard
- All navigation

## Latest Commits

```
88663eb - docs: Add AGENTS.md with mandatory quality standards
8c79aa6 - fix: Map backend API responses to frontend structures
56be67c - fix: Move Google Fonts to HTML head
5037604 - docs: Mark Phase 3.2 complete with premium theme
fe1c7f7 - test: Update test expectations to match new UI
f63eb04 - feat: Implement premium dark casino theme
```

## File Status

### Modified (Uncommitted): NONE (all clean)

### Recently Created:
- `AGENTS.md` - Quality standards (✅ committed)
- Frontend services with temporary mappings (✅ committed, ⚠️ need fixing)

### Backend API Endpoints (Current):
```
POST /api/auth/register
  Request: { username, email, password }
  Response: { user_id, username, message }

POST /api/auth/login
  Request: { username, password }
  Response: { token, user_id, username, role, expires_in }

GET /api/tournaments
  Response: {
    tournaments: [{
      id, name, description, status,
      buy_in_chips, entry_fee_usd, max_players,
      scheduled_at, created_at, updated_at,
      player_count, seats_available
    }],
    pagination: { total, page, limit, pages }
  }

GET /api/leaderboard
  Response: {
    leaderboard: [{
      rank, user_id, username,
      tournaments_played, tournament_wins,
      avg_finish, total_winnings
    }],
    updated_at
  }
```

## How to Resume from This Point

### If Claude Crashes:

1. **Read this file first** - `RESUME_STATE.md`
2. **Check branch** - Should be on `feature/2026-02-24_phase-3.2-frontend-lobby-leaderboard`
3. **Read AGENTS.md** - Mandatory quality standards
4. **Follow "Next Tasks" above** - In order

### Commands to Verify State:

```bash
# Check branch
git status
git log --oneline -5

# Check servers (should be running)
# Backend: http://localhost:5000
# Frontend: http://localhost:5175

# Test API directly
curl http://localhost:5000/api/tournaments
curl http://localhost:5000/api/leaderboard
```

## Known Issues

1. **Field naming inconsistency** - Backend uses `_chips`, `_usd` suffixes, frontend doesn't
2. **Temporary mapping layers** - Need to be removed once API spec locked in
3. **10 RBAC tests failing** - Known issue, documented in Phase 3.7
4. **Graphics/visuals** - Need more work per user feedback

## Documentation State

- ✅ CLAUDE.md - v1.9, up to date
- ✅ TASK-BOARD.md - v1.9, Phase 3.2 marked complete (needs amendment)
- ✅ AGENTS.md - v1.0, quality standards created
- ⏳ API-SPECIFICATION.md - NEEDS CREATION (next task)
- ⏳ API-FIELD-NAMING-GUIDE.md - NEEDS CREATION (next task)

## Success Criteria for Next Steps

**API Spec Creation:**
- [ ] All endpoints documented with exact JSON schemas
- [ ] Field naming conventions defined and justified
- [ ] Frontend and backend use SAME field names (no mapping)
- [ ] Locked in as the single source of truth

**Code Fixes:**
- [ ] Remove all temporary mapping code from services
- [ ] Update frontend interfaces to match backend exactly
- [ ] All unit tests pass (backend 43/53, frontend 16/16)
- [ ] Integration test passes (manual, both servers)

## Budget

- **Current:** ~$5.06 remaining
- **Estimated for this work:** 1-2 hours (~$1.24-2.48)
- **Margin:** Adequate

---

**Created:** 2026-02-26 21:50 GMT+13
**Purpose:** Resume point if session crashes during API spec creation
**Next Action:** Create API-SPECIFICATION.md and API-FIELD-NAMING-GUIDE.md
