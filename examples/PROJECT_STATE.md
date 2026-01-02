# TaskFlow MVP :: Thread State

> ⚠️ **Example only.** All data, names, budgets, and scenarios are fictional.

## Last Updated: 2025-12-31

---

## Session Injection Block

```
<thread>TASKFLOW</thread>
<scope>LOCKED</scope>

<status>
Stage: Implementation
Focus: User authentication system
Last Updated: 2025-12-31
</status>

<locked_decisions>
1. Tech stack: Python/FastAPI backend, React frontend
2. Database: PostgreSQL with SQLAlchemy ORM
3. Auth: Email/password with JWT tokens (no OAuth for MVP)
4. Hosting: Railway free tier
5. No mobile app :: web only for MVP
</locked_decisions>

<rejected_ideas>
1. Django :: rejected, FastAPI is lighter for API-first
2. MongoDB :: rejected, relational data needs SQL
3. OAuth/social login :: rejected, adds complexity for MVP
4. GraphQL :: rejected, REST is sufficient
5. Microservices :: rejected, monolith for speed
</rejected_ideas>

<constraints>
• Budget: $0 (free tier only)
• Timeline: 4 weeks to MVP
• Team: Solo developer
• Must work offline-first (PWA)
</constraints>

<today_focus>Implement password reset flow</today_focus>
```

---

## Current Status

**Stage:** Implementation
**Focus:** User authentication system
**Blockers:** None

---

## Decisions Made

1. **Tech stack: Python/FastAPI + React** :: Best balance of speed and simplicity
2. **PostgreSQL with SQLAlchemy** :: Relational data, good ORM support
3. **JWT authentication** :: Stateless, works with API-first design
4. **Email/password only for MVP** :: OAuth adds too much complexity
5. **Railway for hosting** :: Free tier sufficient for MVP
6. **Web-only, no mobile** :: Ship faster, validate first
7. **PWA for offline** :: Service worker caches core functionality

---

## Rejected Ideas

1. ~~Django~~ :: Too heavy for API-only backend
2. ~~MongoDB~~ :: Data is relational (users, tasks, projects)
3. ~~OAuth/social login~~ :: Scope creep, add post-MVP
4. ~~GraphQL~~ :: Over-engineering for simple CRUD
5. ~~Microservices~~ :: Solo dev, monolith is faster
6. ~~Stripe integration~~ :: Free MVP first, monetize later
7. ~~Real-time sync~~ :: Polling is fine for MVP

---

## Open Questions

- [ ] Password reset: email link or code?
- [ ] Session timeout: 7 days or 30 days?
- [x] Rate limiting approach :: Resolved: Use slowapi middleware

---

## Constraints

• $0 budget (free tier hosting only)
• 4-week timeline to working MVP
• Solo developer (no code review available)
• Must support offline usage (PWA)
• No features that require paid services

---

## Architecture Notes

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI   │────▶│  PostgreSQL │
│   (PWA)     │◀────│   (REST)    │◀────│  (Railway)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

API endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/reset-password`
- `GET /tasks`
- `POST /tasks`
- `PUT /tasks/{id}`
- `DELETE /tasks/{id}`

---

## Last Session

**Date:** 2025-12-30
**Summary:** Implemented user registration and login. JWT tokens working. Basic task CRUD complete.
**Next Actions:**
1. Implement password reset flow
2. Add email verification
3. Set up rate limiting

---

## Archive

**Week 1 (Dec 15-21):**
- Initial project setup
- Database schema design
- Decided on FastAPI over Django

**Week 2 (Dec 22-28):**
- User model and migrations
- Registration endpoint
- Login with JWT
