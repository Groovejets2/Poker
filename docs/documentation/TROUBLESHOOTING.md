# Troubleshooting Guide

**Category:** documentation
**Purpose:** Debug and resolve common issues in OpenClaw Poker Platform

**Status:** draft
**Version:** 1.0
**Last Updated:** 2026-02-23 17:28 GMT+13
**Version:** 1.0
**Owner:** Angus
**Tags:** debugging, troubleshooting, errors, support

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-23 17:22 | 1.0 | Angus | Initial stub - TODO: populate with common issues as they arise |

---

## Common Issues

### Server won't start

**Error:** `Error: Cannot find module 'typeorm'`

**Solution:**
1. Ensure you ran `npm install` in backend/ folder
2. Verify `node_modules/` exists
3. Run `npm install` again if needed

---

### Database connection failed

**Error:** `Error during TypeORM DataSource initialization`

**Solution:**
1. Check `.env` file exists with correct DB_PATH (test) or DB credentials (prod)
2. For test: Verify `data/test/` folder exists
3. For prod: Verify PostgreSQL is running and credentials are correct

---

### JWT errors

**Error:** `JsonWebTokenError: invalid token`

**Solution:**
1. Ensure JWT_SECRET matches on server and client
2. Check token hasn't expired (3600 second expiry)
3. Verify Authorization header format: `Bearer <TOKEN>`

---

## TODO

- [ ] API response errors and solutions
- [ ] Database migration issues
- [ ] Performance troubleshooting
- [ ] Port conflicts
- [ ] Memory/CPU issues
- [ ] CORS errors
- [ ] Rate limiting issues
