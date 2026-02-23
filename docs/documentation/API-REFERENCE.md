# API Reference

**Category:** documentation
**Purpose:** Complete API endpoint documentation and usage examples

**Status:** draft
**Version:** 1.0
**Last Updated:** 2026-02-23 17:28 GMT+13
**Version:** 1.0
**Owner:** Angus
**Tags:** api, backend, endpoints, reference

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-23 17:22 | 1.0 | Angus | Initial stub - TODO: auto-generate from OpenAPI spec |

---

## Base URL

```
http://localhost:5000/api
```

## Authentication

All endpoints except `/auth/login` and `/auth/register` require JWT token:

```
Authorization: Bearer <TOKEN>
```

## Endpoints (In Progress)

### Authentication
- `POST /auth/login` - Login user, get JWT token
- `POST /auth/register` - Create new user account

### Tournaments
- `GET /tournaments` - List tournaments
- `GET /tournaments/:id` - Get tournament details
- `POST /tournaments/:id/register` - Join tournament
- `DELETE /tournaments/:id/unregister` - Leave tournament

### Matches
- `GET /tournaments/:id/matches` - List matches in tournament
- `GET /matches/:id` - Get match details
- `POST /tournaments/:id/matches/:matchId/score` - Submit match results

### Leaderboard
- `GET /leaderboard` - Get global rankings
- `GET /leaderboard/:userId` - Get player stats

## TODO

- [ ] Full endpoint specifications with request/response examples
- [ ] Error codes and status messages
- [ ] Rate limiting documentation
- [ ] WebSocket endpoints (if applicable)
- [ ] Auto-generate from OpenAPI/Swagger spec
