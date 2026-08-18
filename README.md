# SolveBounty

> **Have a problem? Put a prize on it.**
> High-stakes problem solving, verified bounties, and secure escrow payouts. (Market: Nigeria First)

---

## 1. System Architecture

```
┌────────────────────────────────────────────────────────┐
│             Next.js (App Router, TypeScript)           │
│                 Frontend Client & Admin                │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS / JSON REST (/api/v1/)
                            ▼
┌────────────────────────────────────────────────────────┐
│             Django REST Framework (Core Monolith)      │
│  Auth • Profiles • Challenges • Submissions • Payments │
│       Payouts • Ledger • Audit • Disputes • Reviews    │
└───────────────┬────────────────────────────┬───────────┘
                │                            │
                ▼                            ▼
┌───────────────────────────────┐ ┌──────────────────────┐
│     PostgreSQL / SQLite       │ │    Redis + Celery    │
│  (Single Source of Truth)     │ │  (Async Tasks/Events)│
└───────────────────────────────┘ └──────────┬───────────┘
                                             │
                                             ▼
                                  ┌──────────────────────┐
                                  │ FastAPI (AI Service) │
                                  │ (Advisory Layer Only)│
                                  └──────────────────────┘
```

---

## 2. Quickstart (Instant Local Run with SQLite)

### Prerequisites
- Python 3.10+
- Node.js 18+

### Step 1: Clone and Configure Environment
```bash
cp .env.example .env
```

### Step 2: Backend Setup (Django + DRF)
```bash
# Install Python dependencies
pip install -r apps/api/requirements.txt

# Run migrations (uses SQLite automatically if DATABASE_URL is not set)
python apps/api/manage.py migrate

# Seed skills catalogue
python apps/api/manage.py seed_skills

# Run backend server
python apps/api/manage.py runserver 0.0.0.0:8000
```
Backend API will be live at `http://localhost:8000/api/v1/`.
Interactive OpenAPI Swagger docs available at `http://localhost:8000/api/docs/`.

### Step 3: Frontend Setup (Next.js)
```bash
cd apps/web
npm install
npm run dev
```
Web app will be live at `http://localhost:3000`.

### Step 4: AI Microservice (FastAPI - Optional)
```bash
pip install -r apps/ai/requirements.txt
cd apps/ai
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```
AI API docs available at `http://localhost:8001/docs`.

---

## 3. Running Automated Pytest Suite

```bash
cd apps/api
pytest
```

100% test coverage across:
- JWT Authentication & Registration
- Challenge State Machine Transitions
- Submissions & Single-entry Constraints
- Paystack Gateway & Double-Entry Ledger Escrow Credits
- Winner Selection & NUBAN Bank Payout Debits

---

## 4. Key Financial Invariants
1. `payments`: Tracks external gateway intent & Paystack transaction metadata.
2. `payment_events`: Preserves immutable raw webhook payloads signed with HMAC-SHA512.
3. `ledger_entries`: Double-entry accounting system tracking all escrow credits (`CHALLENGE_FUNDING`) and debits (`WINNER_PAYOUT`).
4. `payouts`: Manages automated solver bank payouts via Paystack Transfers.
