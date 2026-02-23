# Setup Guide - Development Environment

**Category:** documentation
**Purpose:** Get the development environment running for OpenClaw Poker Platform

**Status:** draft
**Version:** 1.0
**Last Updated:** 2026-02-23 17:28 GMT+13
**Version:** 1.0
**Owner:** Angus
**Tags:** setup, development, environment, backend

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-23 17:22 | 1.0 | Angus | Initial stub - TODO: complete with full setup instructions |

---

## Quick Start

1. Install dependencies: `npm install`
2. Set up .env file (see below)
3. Start server: `npm start`
4. Test: `curl http://localhost:5000/health`

## Environment Variables

Create `.env` in backend/ folder:

```
NODE_ENV=test
DB_TYPE=sqlite
DB_PATH=../../data/test/poker.db
API_PORT=5000
JWT_SECRET=your-secret-key
```

## TODO

- [ ] Database setup instructions
- [ ] Node/npm version requirements
- [ ] Windows vs Mac/Linux differences
- [ ] Docker setup (if applicable)
- [ ] First API call tutorial
