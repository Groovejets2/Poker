# Security Architecture - OpenClaw Poker Platform

**Category:** specifications
**Purpose:** Documents the security architecture for authentication, session management, and access control
**Status:** APPROVED
**Version:** 1.0
**Last Updated:** 2026-03-02
**Owner:** Jon + Development Team
**Tags:** security, authentication, jwt, cookies, rbac, phase-3.8-complete

---

## Table of Contents

1. [Overview](#1-overview)
2. [Threat Model](#2-threat-model)
3. [Authentication Architecture](#3-authentication-architecture)
4. [Token Strategy](#4-token-strategy)
5. [Session Lifecycle](#5-session-lifecycle)
6. [Backend Implementation](#6-backend-implementation)
7. [Frontend Implementation](#7-frontend-implementation)
8. [Role-Based Access Control](#8-role-based-access-control)
9. [CORS Configuration](#9-cors-configuration)
10. [Security Controls Summary](#10-security-controls-summary)
11. [Known Limitations and Trade-offs](#11-known-limitations-and-trade-offs)
12. [Environment Variables](#12-environment-variables)
13. [Change Log](#13-change-log)

---

## 1. Overview

This document describes the security architecture for the OpenClaw Poker Platform, covering
authentication, session management, token storage, access control, and cross-origin resource
sharing (CORS). It reflects the implementation delivered in Phase 3.8 (v0.3.3) and supersedes
the earlier localStorage-based approach used in Phase 3.2.

The platform uses a stateful, cookie-based authentication model. JSON Web Tokens (JWTs) are
issued as httpOnly cookies rather than returned in response bodies, mitigating the primary
XSS-based token theft vector. A separate refresh token, stored as a sha256 hash in the
database, enables long-lived sessions without permanent access token exposure.

---

## 2. Threat Model

The following threats are explicitly addressed by this architecture.

| Threat | Mitigation |
|--------|------------|
| XSS token theft | Tokens in httpOnly cookies; JavaScript cannot read them |
| CSRF attacks | `sameSite=strict` cookie attribute; no cross-site requests carry cookies |
| Refresh token reuse (session hijacking) | Token rotation on every refresh; reuse detected by hash mismatch, session nullified |
| Timing attacks on token comparison | `crypto.timingSafeEqual()` for constant-time hash comparison |
| Token forgery | JWT signature verification using separate `JWT_SECRET` and `REFRESH_SECRET` |
| Privilege escalation via registration | Role not accepted as a registration field; entity default (`player`) always applied |
| Unauthorised tournament creation | `requireRole(['admin'])` middleware on `POST /api/tournaments` |
| Credentials over plaintext | `secure` cookie flag enabled in production; HTTPS enforced |
| Overly broad CORS | Origins restricted to explicit allowlist via `CORS_ORIGIN` environment variable |

Threats not yet addressed (out of scope for v0.3.3):

- Bot upload endpoints (on hold indefinitely)
- Rate limiting per user (current limit is global: 100 requests/minute)
- Account lockout on repeated failed logins

---

## 3. Authentication Architecture

### 3.1 Dual-Token Model

The platform uses two tokens with different lifetimes and scopes:

| Token | Secret | Lifetime | Cookie path | Stored in DB |
|-------|--------|----------|-------------|--------------|
| `access_token` | `JWT_SECRET` | 15 minutes | `/` | No |
| `refresh_token` | `REFRESH_SECRET` | 7 days | `/api/auth` | sha256 hash only |

The access token grants access to protected API routes. It is short-lived, so its exposure
window is narrow if intercepted. The refresh token is long-lived and is used exclusively to
obtain a new access token; it is path-scoped to `/api/auth` so the browser only sends it to
refresh-related endpoints, never to game or tournament endpoints.

### 3.2 Stateful Refresh Tokens

The refresh token is *stateful* — the server stores a record of it (as a sha256 hash) in the
database on the `users` table. This enables:

- **Logout revocation:** Nullifying the stored hash immediately invalidates the refresh token.
- **Reuse detection:** If a previously rotated token is presented, the hash will not match,
  and the server invalidates the current session entirely.

The raw token is never stored. Only the sha256 hex digest (64 characters) is persisted.
sha256 is used rather than bcrypt because JWT strings routinely exceed bcrypt's 72-byte input
limit, which would silently truncate the hashed value.

### 3.3 JWT Payload

Both the access and refresh JWTs carry the same minimal payload:

```json
{
  "user_id": 1,
  "username": "jon",
  "role": "player"
}
```

The role is embedded in the JWT payload so that access control decisions can be made without
a database round-trip on every request.

---

## 4. Token Strategy

### 4.1 Why httpOnly Cookies Instead of localStorage

Prior to Phase 3.8, tokens were stored in `localStorage`. This approach has a fundamental
weakness: any JavaScript executing in the browser — including injected scripts from XSS
attacks or compromised third-party dependencies — can read `localStorage` and exfiltrate the
token.

httpOnly cookies are inaccessible to JavaScript entirely. The browser attaches them
automatically to qualifying requests. Combined with `sameSite=strict`, they are not sent with
cross-site requests, removing the primary CSRF risk that cookies historically introduced.

| Property | localStorage | httpOnly Cookie |
|----------|-------------|-----------------|
| Readable by JavaScript | Yes | No |
| Sent cross-site | Not applicable | Only if `sameSite=none` |
| XSS risk | High | Mitigated |
| CSRF risk | Low | Mitigated by `sameSite=strict` |

### 4.2 Cookie Attributes

All authentication cookies are set with the following base configuration:

```typescript
const COOKIE_BASE = {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict' as const,
};
```

The `secure` flag is gated on `NODE_ENV` so that local HTTP development continues to work.
In production, all cookies are transmitted over HTTPS only.

The `refresh_token` cookie additionally specifies `path: '/api/auth'`, scoping it to the
authentication endpoints.

---

## 5. Session Lifecycle

### 5.1 Login

1. Client sends `POST /api/auth/login` with `{ username, password }`.
2. Server verifies credentials (bcrypt comparison).
3. Server generates a signed access JWT (15 min) and a signed refresh JWT (7 days).
4. Server computes `sha256(refreshToken)` and stores the hash plus an expiry timestamp
   in the `users` table.
5. Server sets two httpOnly cookies (`access_token`, `refresh_token`) on the response.
6. Response body contains `{ user_id, username, role }` only — no token.

### 5.2 Authenticated Requests

The auth middleware reads the access token in this order:

1. `req.cookies.access_token` (httpOnly cookie — preferred)
2. `req.headers.authorization` (Bearer token — fallback for API clients)

If the token is absent or invalid, the middleware returns `401 UNAUTHORIZED`.

### 5.3 Session Restoration on Page Load

When the frontend application mounts, `AuthContext` calls `authService.checkSession()`,
which posts to `POST /api/auth/refresh`. If a valid refresh token cookie is present, the
server rotates both tokens and returns the session data. If not, the user is treated as
unauthenticated.

The `isLoading` state in `AuthContext` remains `true` until this check resolves, preventing
a flash of unauthenticated content on page load.

### 5.4 Token Refresh

When the frontend receives a `401` response:

1. The `api.ts` interceptor checks whether a refresh is already in progress (`isRefreshing`).
2. If not, it calls `POST /api/auth/refresh` and queues any concurrent requests in
   `failedQueue`.
3. On success, the queue is drained and all pending requests are retried.
4. On failure, the queue is rejected and the user is redirected to `/login`.

Server-side refresh logic:

1. Verify the refresh JWT signature (rejects expired tokens).
2. Look up the user in the database.
3. Compare `sha256(incomingRefreshToken)` against the stored `refresh_token_hash` using
   `crypto.timingSafeEqual()`. Mismatch causes immediate session nullification.
4. Check the stored `refresh_token_expires_at` timestamp as a secondary expiry guard.
5. Issue new access and refresh tokens; store the new hash; set new cookies.

### 5.5 Logout

1. Client sends `POST /api/auth/logout`.
2. Server decodes (does not verify) the `access_token` cookie to extract `user_id`.
   `jwt.decode()` is used deliberately — logout must succeed even with an expired access token.
3. Server sets `refresh_token_hash = null` and `refresh_token_expires_at = null` for that user.
4. Server clears both cookies via `res.clearCookie()`.
5. Any subsequent use of the old refresh token will find no matching hash in the database.

---

## 6. Backend Implementation

### 6.1 Auth Routes (`backend/src/routes/auth.ts`)

| Endpoint | Method | Auth required | Description |
|----------|--------|---------------|-------------|
| `/api/auth/register` | POST | No | Create new user account |
| `/api/auth/login` | POST | No | Authenticate and issue tokens |
| `/api/auth/refresh` | POST | No (refresh cookie) | Rotate tokens |
| `/api/auth/logout` | POST | No (access cookie) | Revoke session |

Key implementation details:

- `hashToken(token)` — `crypto.createHash('sha256').update(token).digest('hex')`
- `compareHashes(a, b)` — `crypto.timingSafeEqual(Buffer.from(a, 'hex'), Buffer.from(b, 'hex'))`
- `ACCESS_TOKEN_EXPIRY_SECS = 15 * 60` (900 seconds)
- `REFRESH_TOKEN_EXPIRY_SECS = 7 * 24 * 60 * 60` (604,800 seconds)

Both `JWT_SECRET` and `REFRESH_SECRET` are required at startup. The server calls
`process.exit(1)` if either is absent — no insecure fallback is permitted.

### 6.2 Auth Middleware (`backend/src/middleware/auth.ts`)

```typescript
const token = req.cookies?.access_token ?? req.headers.authorization?.split(' ')[1];
```

Cookie-first reading with Authorization header fallback allows both browser clients
(cookie-based) and API clients or test suites (header-based) to authenticate.

### 6.3 Server Configuration (`backend/src/server.ts`)

- `cookieParser()` middleware is registered before all routes.
- CORS origins are loaded from `process.env.CORS_ORIGIN` (comma-separated list) or fall
  back to a hardcoded development allowlist.
- `credentials: true` is set on the CORS configuration, which is required for
  cross-origin cookie delivery.

### 6.4 Database Schema

The `users` table has two additional columns added in Phase 3.8:

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `refresh_token_hash` | varchar(64) | Yes | sha256 hex digest of current refresh JWT |
| `refresh_token_expires_at` | datetime | Yes | Expiry timestamp for secondary check |

Both columns are `null` when the user has no active session (after logout or revocation).

Migration file: `backend/src/database/migrations/1740787200000-AddRefreshTokenToUser.ts`

---

## 7. Frontend Implementation

### 7.1 Axios Client (`frontend/src/services/api.ts`)

- `withCredentials: true` is set on the Axios instance, instructing the browser to include
  cookies in cross-origin requests.
- The request interceptor from Phase 3.2 (which read `localStorage`) has been removed.
- The response interceptor handles `401` responses with a queue pattern:

```
401 received
  -> isRefreshing?
       Yes -> add to failedQueue (will retry after refresh completes)
       No  -> set isRefreshing = true
           -> POST /api/auth/refresh
               Success -> processQueue(null) -> retry original requests
               Failure -> processQueue(error) -> redirect to /login
           -> set isRefreshing = false
```

### 7.2 Auth Service (`frontend/src/services/auth.service.ts`)

| Method | Description |
|--------|-------------|
| `login(credentials)` | POST to `/auth/login`; returns `SessionData` |
| `register(data)` | POST to `/auth/register`; then calls `login()` automatically |
| `checkSession()` | POST to `/auth/refresh`; returns `SessionData` or `null` |
| `logout()` | POST to `/auth/logout`; errors are silently swallowed (state cleared regardless) |

`localStorage` is no longer read or written by any auth method.

`SessionData` interface:

```typescript
interface SessionData {
  user_id: number;
  username: string;
  role: string;
}
```

### 7.3 Auth Context (`frontend/src/context/AuthContext.tsx`)

- `isLoading: boolean` — `true` until `checkSession()` resolves on mount. Consumers should
  render a loading state rather than unauthenticated content while this is `true`.
- `logout()` is `async` — it awaits the server call before clearing local state.
- `isAdmin` — derived from `user?.role === 'admin'`.

---

## 8. Role-Based Access Control

Implemented in Phase 3.6, carried forward unchanged.

### 8.1 Roles

| Role | Permissions |
|------|-------------|
| `player` | Default role for all registrations. Read access to tournaments and leaderboard. |
| `admin` | Can create tournaments (`POST /api/tournaments`). |
| `moderator` | Defined in entity; no additional route protection currently assigned. |

### 8.2 Middleware

`requireRole(roles: string[])` middleware is applied after `authMiddleware`. It checks
`req.user.role` against the allowed roles array. Returns `403 FORBIDDEN` with
`required_role` in the error body if access is denied.

### 8.3 Registration Security

The registration endpoint destructures only `{ username, email, password }` from the request
body. Any `role` field submitted by the client is silently ignored. The `role` column default
value (`player`) is applied by TypeORM at the entity level.

---

## 9. CORS Configuration

### 9.1 Development Default Allowlist

When `CORS_ORIGIN` is not set, the following origins are permitted:

- `http://localhost:3000`
- `http://localhost:5173`
- `http://localhost:5174`
- `http://localhost:5175`
- `https://openclaw-poker.local`

### 9.2 Production Configuration

Set `CORS_ORIGIN` in the production `.env` file as a comma-separated list:

```
CORS_ORIGIN=https://openclaw-poker.com,https://app.openclaw-poker.com
```

`credentials: true` must remain set for cookie-based auth to function across origins.

---

## 10. Security Controls Summary

| Control | Mechanism | Status |
|---------|-----------|--------|
| Token XSS protection | httpOnly cookies | Active (v0.3.3) |
| CSRF protection | sameSite=strict cookie attribute | Active (v0.3.3) |
| Refresh token rotation | New tokens issued on every refresh call | Active (v0.3.3) |
| Refresh token reuse detection | Hash mismatch triggers session nullification | Active (v0.3.3) |
| Timing-safe token comparison | `crypto.timingSafeEqual()` | Active (v0.3.3) |
| Stateful logout | DB hash nullified on logout | Active (v0.3.3) |
| Separate refresh secret | `REFRESH_SECRET` distinct from `JWT_SECRET` | Active (v0.3.3) |
| Required secrets at startup | `process.exit(1)` if JWT_SECRET or REFRESH_SECRET absent | Active (v0.3.6) |
| Role-based access control | `requireRole()` middleware | Active (v0.3.6) |
| Request body size limit | `express.json({ limit: '100kb' })` | Active (v0.3.6) |
| Rate limiting | 100 requests/minute globally via `express-rate-limit` | Active (v0.3.6) |
| HTTPS in production | `secure` cookie flag; enforced by deployment | Required at deploy |

---

## 11. Known Limitations and Trade-offs

### 11.1 Single Active Session Per User

The database stores one refresh token hash per user (Option A). Logging in from a second
device or browser invalidates any existing refresh token in the database, effectively logging
out the first session when the second session attempts to refresh.

To support multiple concurrent sessions, the hash would need to be stored in a separate
`refresh_tokens` table with one row per session. This is tracked as a future backlog item.

### 11.2 Multi-Tab Page-Load Race Condition

`checkSession()` is called on every page load, which rotates the refresh token. If two
browser tabs open simultaneously, the first tab's rotation invalidates the hash that the
second tab presents moments later. The second tab receives a `401` and redirects to login.

This is an acceptable trade-off given the single-session model. It will not occur under
normal single-tab use patterns.

### 11.3 Logout Relies on jwt.decode()

The logout endpoint uses `jwt.decode()` (no signature verification) to extract the `user_id`
from the access token. This allows logout to succeed even when the access token has expired.
The trade-off is that a crafted cookie with a forged `user_id` could trigger a logout for
that user ID. Since the cookie is httpOnly (not settable by JavaScript) and sameSite=strict
(not sent cross-site), the practical attack surface for this is very limited.

### 11.4 No Account Lockout

Repeated failed login attempts are not currently rate-limited at the user level — only at the
global 100 req/min level. Brute-force protection at the account level is a recommended
addition before public launch.

---

## 12. Environment Variables

All security-relevant environment variables for the backend:

| Variable | Required | Description |
|----------|----------|-------------|
| `JWT_SECRET` | Yes | Secret for signing access JWTs. Generate: `openssl rand -base64 32` |
| `REFRESH_SECRET` | Yes | Secret for signing refresh JWTs. Must differ from `JWT_SECRET` |
| `NODE_ENV` | Yes (prod) | Set to `production` to enable the `secure` cookie flag and SSL |
| `CORS_ORIGIN` | No | Comma-separated list of allowed origins. Defaults to localhost allowlist |
| `PORT` | No | API server port. Defaults to `5000` |

See `backend/.env.example` for a full template.

---

## 13. Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-03-02 | 1.0 | Sonnet 4.6 | Initial creation covering Phase 3.8 implementation (httpOnly cookies, refresh tokens) and Phase 3.6 RBAC |

---

**Document Created:** 2026-03-02 08:30 GMT+13
**Version:** 1.0
**Status:** APPROVED
