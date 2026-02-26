# Blueprint: Countdown Timer
> A retro 8-bit countdown experience — Pac-Man expressions, urgency color shifts, and persistent timers powered by FastAPI and PostgreSQL.

---

## Overview

**Blueprint: Countdown Timer** is a full-stack retro-themed countdown timer application built for anyone who wants a little personality in their productivity tooling. As the clock ticks down, an animated Pac-Man-style character reacts to the remaining time, and the UI shifts through urgency-driven color states to keep you visually informed at a glance.

**Key features:**

- Create, start, pause, and reset named countdown timers
- Timers persist across sessions via a PostgreSQL database
- Pac-Man-style character expressions that react to urgency levels
- Color-coded urgency system (calm → warning → critical) driven by configurable thresholds
- RESTful API backend built with FastAPI
- Reactive, type-safe React + Vite frontend written in TypeScript

**Intended audience:** Developers, productivity enthusiasts, and anyone who appreciates 8-bit aesthetics alongside practical tooling.

---

## Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| Primary Language | Python 3.11+ | Backend logic and API |
| Backend Framework | FastAPI | Async REST API, auto-generated OpenAPI docs |
| Database | PostgreSQL | Persistent timer storage |
| ORM / DB Access | Raw SQL via migrations | `migrations/001_create_timers.sql` |
| Frontend Framework | React 18+ | Component-based UI |
| Frontend Build Tool | Vite | Fast HMR and optimized production builds |
| Frontend Language | TypeScript | Strict type safety across all components |
| Styling | Tailwind CSS | Utility-first styling with retro theme |
| Python Testing | pytest | Unit and integration tests |
| Frontend Testing | Vitest / React Testing Library | Component and utility tests |

---

## Architecture

The application follows a layered, separation-of-concerns architecture split across two independent runtimes — a Python backend and a TypeScript frontend — communicating over HTTP.

```
┌─────────────────────────────────────────┐
│              React + Vite               │
│           (web/ directory)              │
│                                         │
│  App.tsx → TimerContainer               │
│    ├── TimerDisplay (countdown digits)  │
│    ├── CharacterFace (Pac-Man mood)     │
│    ├── ControlButtons (start/pause/reset│
│    └── DurationInput (set duration)     │
│                                         │
│  useTimer hook → timerApi.ts → HTTP     │
└──────────────────┬──────────────────────┘
                   │ REST (JSON)
┌──────────────────▼──────────────────────┐
│            FastAPI Backend              │
│            (app/ directory)             │
│                                         │
│  routers/timers.py  (CRUD endpoints)    │
│  routers/health.py  (health check)      │
│       │                                 │
│  services/timer_service.py              │
│       │                                 │
│  repos/timer_repo.py                    │
│       │                                 │
│  database.py (connection pool)          │
└──────────────────┬──────────────────────┘
                   │ SQL
┌──────────────────▼──────────────────────┐
│             PostgreSQL                  │
│         (timers table)                  │
└─────────────────────────────────────────┘
```

### Component Descriptions

| Component | Responsibility |
|---|---|
| `app/routers/timers.py` | HTTP route handlers for timer CRUD operations |
| `app/routers/health.py` | `/health` liveness endpoint |
| `app/services/timer_service.py` | Business logic: timer state transitions, validation |
| `app/repos/timer_repo.py` | Data access layer — all SQL queries live here |
| `app/models/timer.py` | Pydantic models and domain entity definitions |
| `app/database.py` | Database connection and pool management |
| `app/config.py` | Environment-based configuration via Pydantic settings |
| `web/src/hooks/useTimer.ts` | React hook managing timer state, polling, and side effects |
| `web/src/api/timerApi.ts` | Typed HTTP client for all backend API calls |
| `web/src/utils/urgency.ts` | Pure functions mapping remaining time to urgency levels |
| `web/src/components/CharacterFace.tsx` | Animated Pac-Man character that reacts to urgency |
| `web/src/components/TimerDisplay.tsx` | Retro digit display for the countdown |

---

## Project Structure

```
.
├── app/                        # FastAPI backend application
│   ├── main.py                 # Application entry point, middleware, router registration
│   ├── config.py               # Environment configuration (Pydantic Settings)
│   ├── database.py             # DB connection and pool setup
│   ├── models/
│   │   └── timer.py            # Pydantic request/response models
│   ├── repos/
│   │   └── timer_repo.py       # Raw SQL data access layer
│   ├── routers/
│   │   ├── health.py           # GET /health
│   │   └── timers.py           # Timer CRUD endpoints
│   └── services/
│       └── timer_service.py    # Timer business logic
│
├── migrations/
│   └── 001_create_timers.sql   # Initial schema: timers table
│
├── tests/                      # Python test suite (pytest)
│   ├── conftest.py             # Shared fixtures and test DB setup
│   ├── test_timer_service.py   # Unit tests for timer service logic
│   └── test_timers_api.py      # Integration tests for API endpoints
│
├── web/                        # React + Vite frontend
│   ├── index.html              # HTML shell
│   ├── vite.config.ts          # Vite build configuration
│   ├── tailwind.config.ts      # Tailwind CSS configuration
│   ├── tsconfig.json           # TypeScript compiler options
│   └── src/
│       ├── main.tsx            # React entry point
│       ├── App.tsx             # Root component
│       ├── index.css           # Global styles / Tailwind directives
│       ├── types/
│       │   └── timer.ts        # Shared TypeScript types
│       ├── api/
│       │   └── timerApi.ts     # API client functions
│       ├── hooks/
│       │   └── useTimer.ts     # Timer state management hook
│       ├── utils/
│       │   ├── urgency.ts      # Urgency level calculation
│       │   └── urgency.test.ts # Urgency utility tests
│       └── components/
│           ├── TimerContainer.tsx
│           ├── TimerDisplay.tsx
│           ├── CharacterFace.tsx
│           ├── CharacterFace.test.tsx
│           ├── ControlButtons.tsx
│           └── DurationInput.tsx
│
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── package-lock.json           # Root-level lock file
```

---

## Setup & Installation

### Prerequisites

- Python **3.11+**
- Node.js **18+** and npm
- PostgreSQL **14+** running locally or via a remote host
- `git`

### 1. Clone the Repository

```bash
git clone <repository-url>
cd blueprint-countdown-timer
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and fill in your values (see Environment Variables section)
```

### 3. Backend Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Database Setup

Ensure your PostgreSQL instance is running, then apply the migration:

```bash
psql -U <your_db_user> -d <your_db_name> -f migrations/001_create_timers.sql
```

### 5. Frontend Setup

```bash
cd web
npm install
cd ..
```

---

## Usage / Running

### Start the Backend

From the project root with your virtual environment activated:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive API docs (Swagger UI): `http://localhost:8000/docs`  
ReDoc: `http://localhost:8000/redoc`

### Start the Frontend

In a separate terminal:

```bash
cd web
npm run dev
```

The frontend will be available at `http://localhost:5173` (Vite default).

### Build the Frontend for Production

```bash
cd web
npm run build
# Output will be in web/dist/
```

---

## Environment Variables

Copy `.env.example` to `.env` and populate the following keys before running the application. **Never commit real secrets to version control.**

| Variable | Description |
|---|---|
| `DATABASE_URL` | Full PostgreSQL connection string (e.g. `postgresql://user:pass@localhost:5432/dbname`) |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port (default: `5432`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `APP_ENV` | Runtime environment (`development`, `production`, `test`) |
| `ALLOWED_ORIGINS` | Comma-separated list of CORS-allowed origins (e.g. `http://localhost:5173`) |
| `VITE_API_BASE_URL` | Base URL for the frontend API client to reach the backend |

> **Note:** Frontend environment variables must be prefixed with `VITE_` to be exposed by Vite at build time.

---

## API Routes

Base URL: `http://localhost:8000`

### Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness check — returns service status |

### Timers

| Method | Path | Description |
|---|---|---|
| `GET` | `/timers` | List all timers |
| `POST` | `/timers` | Create a new timer |
| `GET` | `/timers/{timer_id}` | Retrieve a specific timer by ID |
| `PUT` | `/timers/{timer_id}` | Update a timer (duration, label, etc.) |
| `DELETE` | `/timers/{timer_id}` | Delete a timer |
| `POST` | `/timers/{timer_id}/start` | Start or resume a timer |
| `POST` | `/timers/{timer_id}/pause` | Pause a running timer |
| `POST` | `/timers/{timer_id}/reset` | Reset a timer to its original duration |

Full request/response schemas are available at `/docs` when the backend is running.

---

## Testing

### Backend Tests (pytest)

```bash
# From the project root with the virtual environment activated
pytest tests/ -v
```

To run a specific test file:

```bash
pytest tests/test_timer_service.py -v
pytest tests/test_timers_api.py -v
```

Test fixtures and shared configuration are located in `tests/conftest.py`. A separate test database is recommended; set `DATABASE_URL` to a test database in your environment before running tests.

### Frontend Tests (Vitest)

```bash
cd web
npm run test
```

To run in watch mode:

```bash
npm run test -- --watch
```

Frontend tests are co-located with their subjects:

- `web/src/components/CharacterFace.test.tsx` — component rendering and expression logic
- `web/src/utils/urgency.test.ts` — urgency threshold utility functions

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository and create a feature branch from `main`.
2. Follow the existing code style — `black` + `ruff` for Python, ESLint + Prettier for TypeScript