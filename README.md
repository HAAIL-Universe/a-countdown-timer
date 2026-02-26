# Blueprint: Countdown Timer
> A retro 8-bit countdown experience — Pac-Man expressions, urgency color shifts, and rock-solid persistence.

---

## Overview

**Blueprint: Countdown Timer** is a full-stack countdown timer application built with a nostalgic 8-bit aesthetic. It features animated Pac-Man-style character expressions that react to the remaining time, dynamic urgency-based color shifts as the clock winds down, and a persistent backend that survives page refreshes and server restarts.

**Who it's for:**
- Developers and hobbyists who want a fun, visually engaging timer for presentations, game sessions, cooking, or productivity sprints.
- Engineers looking for a reference implementation of a FastAPI + React + PostgreSQL project with clean layered architecture.

**Key highlights:**
- 🎮 Retro 8-bit Pac-Man character face that changes expression based on urgency
- 🌈 Dynamic color palette that shifts as the deadline approaches
- 💾 PostgreSQL-backed persistence — timers survive restarts
- ⚡ Vite-powered React frontend with TypeScript
- 🧪 Backend and frontend tests included out of the box

---

## Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| **Primary Language** | Python 3.x | Backend application |
| **Backend Framework** | FastAPI | Async REST API |
| **Database** | PostgreSQL | Persistent timer storage |
| **ORM / DB Layer** | SQLAlchemy / raw SQL | Via `app/database.py` and migrations |
| **Frontend Framework** | React | Component-based UI |
| **Frontend Language** | TypeScript | Strict typing throughout |
| **Frontend Bundler** | Vite | Fast dev server and builds |
| **Styling** | Tailwind CSS | Utility-first styling |
| **Frontend Testing** | Vitest / React Testing Library | Component and utility tests |
| **Backend Testing** | Pytest | Service and API-level tests |

> Specific package versions are defined in `requirements.txt` (backend) and `web/package.json` (frontend).

---

## Architecture

The project follows a classic **three-tier architecture** with a clean separation of concerns inside each tier.

```
┌─────────────────────────────────────────────┐
│              React + Vite Frontend           │
│   web/src/                                   │
│   ├── Components (UI, CharacterFace, etc.)  │
│   ├── Hooks (useTimer)                      │
│   ├── API client (timerApi.ts)              │
│   └── Utils (urgency logic)                 │
└──────────────────┬──────────────────────────┘
                   │ HTTP / REST (JSON)
┌──────────────────▼──────────────────────────┐
│              FastAPI Backend                 │
│   app/                                       │
│   ├── Routers   → HTTP route handlers       │
│   ├── Services  → Business logic            │
│   ├── Repos     → Data access layer         │
│   ├── Models    → Data models               │
│   └── Config    → Settings / environment    │
└──────────────────┬──────────────────────────┘
                   │ SQL
┌──────────────────▼──────────────────────────┐
│              PostgreSQL Database             │
│   migrations/   → Versioned SQL scripts     │
└─────────────────────────────────────────────┘
```

### Component Descriptions

| Component | Path | Responsibility |
|---|---|---|
| **Routers** | `app/routers/` | Define HTTP endpoints; delegate to services |
| **Services** | `app/services/` | Encapsulate business rules (timer logic) |
| **Repos** | `app/repos/` | Abstract all database queries |
| **Models** | `app/models/` | Data shape definitions |
| **Database** | `app/database.py` | Connection pool and session management |
| **Config** | `app/config.py` | Environment-driven configuration via Pydantic settings |
| **API Client** | `web/src/api/timerApi.ts` | Frontend HTTP calls to the backend |
| **useTimer Hook** | `web/src/hooks/useTimer.ts` | Timer state management and countdown logic |
| **Urgency Utils** | `web/src/utils/urgency.ts` | Computes color and expression based on time remaining |
| **CharacterFace** | `web/src/components/CharacterFace.tsx` | Animated Pac-Man-style expression component |

---

## Project Structure

```
.
├── app/                        # FastAPI backend application
│   ├── main.py                 # Application entry point, CORS, router registration
│   ├── config.py               # Pydantic settings (reads from .env)
│   ├── database.py             # PostgreSQL connection and session factory
│   ├── models/
│   │   └── timer.py            # Timer data model
│   ├── repos/
│   │   └── timer_repo.py       # Database queries for timers
│   ├── routers/
│   │   ├── health.py           # GET /health endpoint
│   │   └── timers.py           # CRUD endpoints for timers
│   └── services/
│       └── timer_service.py    # Core timer business logic
│
├── migrations/
│   └── 001_create_timers.sql   # Initial schema migration
│
├── tests/                      # Backend test suite (Pytest)
│   ├── conftest.py             # Fixtures and test DB setup
│   ├── test_timer_service.py   # Unit tests for service layer
│   └── test_timers_api.py      # Integration tests for API routes
│
├── web/                        # React + Vite frontend
│   ├── index.html              # HTML shell
│   ├── vite.config.ts          # Vite configuration
│   ├── tailwind.config.ts      # Tailwind CSS configuration
│   ├── tsconfig.json           # TypeScript configuration
│   └── src/
│       ├── main.tsx            # React entry point
│       ├── App.tsx             # Root application component
│       ├── index.css           # Global styles
│       ├── api/
│       │   └── timerApi.ts     # Backend API client
│       ├── components/
│       │   ├── CharacterFace.tsx       # Animated Pac-Man face
│       │   ├── CharacterFace.test.tsx  # Component tests
│       │   ├── ControlButtons.tsx      # Start/Stop/Reset controls
│       │   ├── DurationInput.tsx       # Timer duration input
│       │   ├── TimerContainer.tsx      # Top-level timer layout
│       │   └── TimerDisplay.tsx        # Countdown display
│       ├── hooks/
│       │   └── useTimer.ts     # Timer state and countdown hook
│       ├── types/
│       │   └── timer.ts        # Shared TypeScript types
│       └── utils/
│           ├── urgency.ts      # Urgency level computation
│           └── urgency.test.ts # Utility unit tests
│
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── package-lock.json           # Root-level lock file
```

---

## Setup & Installation

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18 or higher and **npm**
- **PostgreSQL** 14 or higher (running locally or via a managed service)

---

### 1. Clone the Repository

```bash
git clone <repository-url>
cd blueprint-countdown-timer
```

---

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in the required values (see [Environment Variables](#environment-variables)).

---

### 3. Backend Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

---

### 4. Database Setup

Ensure your PostgreSQL server is running, then apply the migration:

```bash
psql -U <your_db_user> -d <your_db_name> -f migrations/001_create_timers.sql
```

---

### 5. Frontend Setup

```bash
cd web
npm install
```

---

## Usage / Running

### Run the Backend (FastAPI)

From the project root with the virtual environment activated:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive API docs (Swagger UI) are at `http://localhost:8000/docs`.

---

### Run the Frontend (Vite Dev Server)

In a separate terminal:

```bash
cd web
npm run dev
```

The frontend will be available at `http://localhost:5173` (or the port reported by Vite).

> The Vite dev server is configured to proxy `/api` requests to the FastAPI backend. Verify this in `web/vite.config.ts` if you change default ports.

---

### Build the Frontend for Production

```bash
cd web
npm run build
```

Built assets will be output to `web/dist/`.

---

## Environment Variables

Copy `.env.example` to `.env` and populate the following keys:

| Variable | Description |
|---|---|
| `DATABASE_URL` | Full PostgreSQL connection string (e.g. `postgresql://user:password@localhost:5432/dbname`) |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port (default: `5432`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins (e.g. `http://localhost:5173`) |
| `DEBUG` | Enable debug mode (`true` / `false`) |

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore` by default.

---

## API Routes

Base URL: `http://localhost:8000`

### Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Returns service health status |

### Timers

| Method | Path | Description |
|---|---|---|
| `GET` | `/timers` | List all timers |
| `POST` | `/timers` | Create a new timer |
| `GET` | `/timers/{id}` | Retrieve a specific timer by ID |
| `PUT` | `/timers/{id}` | Update a timer (duration, state) |
| `DELETE` | `/timers/{id}` | Delete a timer |

> Full request/response schemas are available in the interactive Swagger UI at `/docs` or the ReDoc UI at `/redoc` when the backend is running.

---

## Testing

### Backend Tests (Pytest)

From the project root with the virtual environment activated:

```bash
# Run all backend tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_timer_service.py
pytest tests/test_timers_api.py
```

Test fixtures and database setup are defined in `tests/conftest.py`. Ensure a test database is configured (or that your environment variables point to an appropriate test database) before running integration tests.

---

### Frontend Tests (Vitest)

```bash
cd web

# Run tests once
npm run test

# Run in watch mode
npm run test -- --watch

# Run with coverage
npm run test -- --coverage
```

Frontend tests cover:
- **`CharacterFace.test.tsx`** — Component rendering and expression changes
- **`urgency.test.ts`** — Urgency level computation utility

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes with clear, descriptive commits.
4. Add or update tests to cover your changes.
5. Ensure all tests pass: `pytest` and `npm run test`
6. Open a Pull Request with a description of your changes.

Please follow existing code style conventions and