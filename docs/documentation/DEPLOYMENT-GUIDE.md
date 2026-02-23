# Deployment Guide - Production Setup

**Category:** documentation
**Purpose:** Deploy OpenClaw Poker Platform to production environment

**Status:** draft
**Version:** 1.0
**Last Updated:** 2026-02-23 17:28 GMT+13
**Version:** 1.0
**Owner:** Angus
**Tags:** deployment, production, operations, devops

---

## Change Log

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-02-23 17:22 | 1.0 | Angus | Initial stub - TODO: complete with full deployment instructions |

---

## Prerequisites

- Ubuntu/Debian server or cloud VM
- PostgreSQL 13+
- Node.js 18+
- PM2 (process manager)
- Nginx (reverse proxy)

## Production Environment Variables

Create `.env` on production server:

```
NODE_ENV=production
DB_TYPE=postgres
DB_HOST=<postgres-host>
DB_PORT=5432
DB_NAME=openclaw_poker
DB_USER=<postgres-user>
DB_PASSWORD=<secure-password>
API_PORT=3000
JWT_SECRET=<cryptographically-secure-key>
```

## TODO

- [ ] VPS setup and initial configuration
- [ ] PostgreSQL database creation and migration
- [ ] PM2 process manager setup
- [ ] Nginx reverse proxy configuration
- [ ] SSL/TLS certificate setup
- [ ] Backup and disaster recovery procedures
- [ ] Monitoring and alerting setup
- [ ] Database replication (optional)
- [ ] Load balancing (optional)
