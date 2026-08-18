# SolveBounty MVP Implementation Plan

This plan details the full implementation of the SolveBounty MVP according to **Engineering Specification v1.0**. The build delivers a production-ready monorepo comprising a Django REST Framework core backend (with custom user authentication, domain services, state machines, financial ledger, and Paystack integration), a Next.js React frontend (with challenge discovery, creation wizard, dashboard, and submission flows), a FastAPI AI microservice, and complete Docker orchestration and automated tests.

---

## Proposed System Architecture & Repository Layout

```
solvebounty/
├── apps/
│   ├── web/                        # Next.js (TypeScript, Tailwind CSS)
│   │   ├── app/
│   │   │   ├── (marketing)/        # Landing page, How It Works
│   │   │   ├── auth/               # Login, Register, Auth State
│   │   │   ├── challenges/         # Feed, Filters, Detail, Creation Wizard
│   │   │   ├── dashboard/          # Solver & Poster Management Portals
│   │   │   ├── layout.tsx & page.tsx
│   │   ├── components/             # UI Components (Navbar, Cards, Modals, Badges)
│   │   ├── lib/                    # API client, Auth state, Utilities
│   │   ├── services/               # Frontend API service adapters
│   │   ├── types/                  # TypeScript interfaces matching backend DDL
│   │   └── package.json
│   │
│   ├── api/                        # Django 5 + Django REST Framework Monolith
│   │   ├── config/                 # Settings (base/dev/prod), Celery, WSGI, URLs
│   │   ├── apps/
│   │   │   ├── accounts/           # Custom User (UUID), JWT, Role permissions
│   │   │   ├── profiles/           # User profiles, bio, reputation, portfolio
│   │   │   ├── skills/             # Master skill catalogue + seed command
│   │   │   ├── challenges/         # Challenges, Requirements, Prizes, State Machine
│   │   │   ├── submissions/        # Submissions, Files, Shortlisting
│   │   │   ├── payments/           # Paystack gateway adapter, Webhook HMAC
│   │   │   ├── payouts/            # Recipient resolution & Paystack Transfers
│   │   │   ├── ledger/             # Double-entry immutable audit ledger
│   │   │   ├── disputes/           # Evidence, Disputes, Resolution window
│   │   │   ├── reviews/            # Mutual reputation ratings
│   │   │   ├── notifications/      # Async in-app alerts & Celery tasks
│   │   │   ├── ai/                 # Client interface to AI service
│   │   │   └── audit/              # Structured action audit logging
│   │   ├── tests/                  # Pytest test suite for auth, state, & ledger
│   │   ├── manage.py
│   │   └── requirements.txt
│   │
│   └── ai/                         # FastAPI AI Microservice (Advisory layer)
│       ├── app/
│       │   ├── agents/             # Task architect, Matcher, Submission analyst
│       │   ├── schemas/            # Pydantic schemas
│       │   ├── providers/          # LLM interface adapter
│       │   └── main.py
│       └── requirements.txt
│
├── infrastructure/
│   ├── docker/
│   │   ├── api.Dockerfile
│   │   ├── web.Dockerfile
│   │   └── ai.Dockerfile
│   └── nginx/                      # Reverse proxy configuration
│
├── docker-compose.yml              # Multi-container orchestration
├── docker-compose.dev.yml
├── .env.example
├── Makefile
└── README.md
```

---

## User Review Required

> [!IMPORTANT]
> - **Database Compatibility**: For containerized runs, PostgreSQL 16 + pgvector will be used as the primary database. For lightweight local development without Docker, Django settings will gracefully support SQLite so tests and local servers can run immediately in any environment.
> - **Payment Gateway**: Paystack is integrated with standard HMAC-SHA512 webhook signature verification and server-side verification calls. Sandbox mock mode will be enabled by default if no live `PAYSTACK_SECRET_KEY` is provided.

---

## Proposed Changes

### Phase 1: Monorepo Foundation & Root Orchestration
- Create root `.gitignore`, `.env.example`, `Makefile`, `README.md`.
- Create `docker-compose.yml` and `docker-compose.dev.yml` covering PostgreSQL, Redis, Django API, Celery Worker, FastAPI AI Service, and Next.js Web Frontend.
- Create Dockerfiles in `infrastructure/docker/`.

### Phase 2: Django Backend Core (`apps/api`)
- Scaffold Django project with `config/settings/base.py`, `development.py`, `production.py`, `celery.py`, `urls.py`.
- **`apps/accounts`**:
  - Custom `User` model with UUID PK, roles (`SOLVER`, `POSTER`, `BOTH`, `ADMIN`, `MODERATOR`), and status enum.
  - JWT Authentication via `djangorestframework-simplejwt`.
  - Views: Register, Login, Token Refresh, Current User (`/api/v1/me/`).
- **`apps/profiles`**:
  - `Profile` model with 1-to-1 link to `User`, reputation score, completed/won challenge counters.
  - Endpoints: `GET/PATCH /api/v1/me/profile/`, `GET /api/v1/users/{id}/`.
- **`apps/skills`**:
  - `Skill` model and `UserSkill` join table with proficiency.
  - Management command `seed_skills` to populate the default marketplace skills (Python, Django, Next.js, Power BI, SQL, AI, UI/UX, etc.).
- **`apps/challenges`**:
  - Models: `Challenge`, `ChallengeRequirement`, `ChallengeSkill`, `PrizeAllocation`.
  - State machine: `DRAFT` -> `PENDING_PAYMENT` -> `FUNDED` -> `OPEN` -> `CLOSED` -> `JUDGING` -> `WINNER_SELECTED` -> `COMPLETED` / `DISPUTED` / `CANCELLED`.
  - Services: `ChallengeService`, `WinnerSelectionService`.
  - ViewSets: Filtering by status, category, min/max prize, search, skill tagging.
- **`apps/submissions`**:
  - Models: `Submission`, `SubmissionFile`.
  - Endpoints: create submission, list submissions for challenge, shortlist, view submission details.
- **`apps/payments` & `apps/ledger`**:
  - Models: `Payment`, `PaymentEvent`, `LedgerEntry`.
  - `PaystackProvider` service: initialize transaction, verify transaction, verify webhook signature.
  - `LedgerService`: atomic transaction recording (credit escrow upon payment success, debit on payout).
  - Webhook endpoint: `/api/v1/payments/webhook/`.
- **`apps/payouts`**:
  - Models: `PayoutAccount`, `Payout`.
  - Services: Paystack transfer recipient creation and payout initiation.
- **`apps/disputes`, `apps/reviews`, `apps/notifications`, `apps/audit`**:
  - Dispute tracking, review creation after completion, in-app notifications, and audit logging.
- **Documentation & Tests**:
  - OpenAPI/Swagger documentation via `drf-spectacular`.
  - Pytest test suite testing Auth, Challenge creation, State transitions, Submissions, and Ledger.

### Phase 3: AI Microservice (`apps/ai`)
- FastAPI application in `apps/ai/app/main.py`.
- Endpoints:
  - `POST /ai/v1/challenge/draft` (Turns raw problem description into structured challenge title, requirements, skills, deliverables, and prize estimate).
  - `POST /ai/v1/challenge/classify` (Classifies domains and tags).
  - `POST /ai/v1/challenge/match` (Hybrid scoring: skills + semantic similarity + reputation).
  - `POST /ai/v1/submission/evaluate` (Generates requirements coverage score & constructive feedback).
- Configurable LLM provider interface with local mock fallback.

### Phase 4: Next.js Web Application (`apps/web`)
- Modern Next.js App Router application with Tailwind CSS.
- **Pages & Features**:
  - Marketing Homepage: Hero banner, value propositions ("01 POST, 02 FUND, 03 COMPETE, 04 CHOOSE, 05 PAY"), Featured challenges, stats.
  - Challenge Discovery (`/challenges`): Search bar, filter sidebar (status, budget slider, skill tags), responsive challenge cards.
  - Challenge Details (`/challenges/[id]`): Overview, requirements checklist, deliverables, prize breakdown, timeline, submission submission form / submission list.
  - Challenge Creation Wizard (`/challenges/create`): Multi-step form with problem statement, AI draft enhancement trigger, budget & prize breakdown, requirements builder, preview & payment kickoff.
  - Authentication UI (`/auth/login`, `/auth/register`): Modern login/signup cards with role selection and JWT token management.
  - User Dashboard (`/dashboard`): Tabbed solver/poster dashboard showing created challenges, active submissions, winner status, and earnings.
- UI Kit: Responsive navigation bar, status badges, progress bars, interactive modals.

---

## Verification Plan

### Automated Backend Tests
- Run `pytest` inside `apps/api` to verify:
  - User registration, login, and JWT issuance.
  - Challenge creation, ownership, and filtering.
  - Submissions creation and single-submission constraint.
  - Paystack webhook signature validation and idempotent ledger credit creation.
  - Winner selection permission and state machine enforcement.

### Build & Frontend Verification
- Run Next.js production build (`npm.cmd run build` / TypeScript type checking) inside `apps/web`.
- Verify all pages compile cleanly with zero TypeScript errors.

### Manual End-to-End Verification
1. Register a Poster account and a Solver account.
2. Poster uses the AI Challenge Builder to draft and create a bounty.
3. Verify challenge appears in the discovery feed.
4. Solver submits a solution with deliverables and notes.
5. Poster reviews the submission and selects the winner.
6. Check audit log and ledger entry creation.
