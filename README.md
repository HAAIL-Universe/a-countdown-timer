# Blueprint: Countdown Timer

> A retro 8-bit countdown experience — pixel-perfect urgency, Pac-Man expressions, and persistent timers powered by a modern full-stack architecture.

---

## Overview

**Blueprint: Countdown Timer** is a full-stack web application that brings nostalgic 8-bit energy to the humble countdown timer. Users can create, manage, and track countdown timers that persist across sessions via a PostgreSQL database. As time runs low, the interface responds with dynamic urgency color shifts and expressive Pac-Man-style character animations that react to the remaining duration.

**Who it's for:**
- Developers who want a reference implementation of a FastAPI + React + PostgreSQL full-stack project
- Retro gaming enthusiasts who want a fun, functional productivity tool
- Anyone who needs a visually engaging timer with backend persistence

---

## Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| **Language (Backend)** | Python 3.11+ | Primary server-side language |
| **Backend Framework** | FastAPI | Async REST API with automatic OpenAPI docs |
| **Database** | PostgreSQL | Persistent timer storage |
| **ORM / DB Access** | SQLAlchemy / psycopg2 | Via `app/database.py` |
| **Migrations** | Raw SQL | Managed via `migrations/` directory |
| **Frontend Framework** | React 18+ | Component-based UI |
| **Frontend Language** | TypeScript | Strict typing across all frontend modules |
| **Build Tool** | Vite | Fast dev server and production bundler |
| **Styling** | Tailwind CSS | Utility-first CSS with retro theme customization |
| **Testing (Backend)** | pytest | Unit and API integration tests |
| **Testing (Frontend)** | Vitest / React Testing Library | Component and utility tests |
| **Package Manager (Frontend)** | npm | Managed via `package-lock.json` |

---

## Architecture

The application follows a layered, separation-of-concerns architecture across two distinct runtime contexts: a Python backend and a React frontend.

```
┌─────────────────────────────────────────────────────┐
│                   Browser Client                    │
│  React + Vite + TypeScript (web/)                   │
│  ┌──────────┐ ┌───────────┐ ┌────────────────────┐  │
│  │ useTimer │ │ timerApi  │ │ CharacterFace /     │  │
│  │  (hook)  │ │  (fetch)  │ │ TimerDisplay / UI  │  │
│  └──────────┘ └───────────┘ └────────────────────┘  │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP / REST (JSON)
┌───────────────────────▼─────────────────────────────┐
│              FastAPI Backend (app/)                 │
│  ┌──────────┐ ┌──────────────┐ ┌─────────────────┐  │
│  │ Routers  │ │   Services   │ │      Repos      │  │
│  │ timers   │ │ timer_service│ │   timer_repo    │  │
│  │ health   │ └──────────────┘ └─────────────────┘  │
│  └──────────┘                                       │
└───────────────────────┬─────────────────────────────┘
                        │ SQLAlchemy / psycopg2
┌───────────────────────▼─────────────────────────────┐
│                  PostgreSQL Database                │
│              (timers table via migrations/)         │
└─────────────────────────────────────────────────────┘
```

### Component Descriptions

| Component | Location | Responsibility |
|---|---|---|
| **Routers** | `app/routers/` | HTTP request handling, input validation, response shaping |
| **Services** | `app/services/` | Business logic — timer state transitions, duration calculations |
| **Repos** | `app/repos/` | Data access layer — all direct database queries |
| **Models** | `app/models/` | SQLAlchemy ORM models defining the database schema |
| **Config** | `app/config.py` | Environment variable loading and application settings |
| **Database** | `app/database.py` | SQLAlchemy engine and session factory |
| **timerApi** | `web/src/api/timerApi.ts` | Frontend HTTP client for all backend API calls |
| **useTimer** | `web/src/hooks/useTimer.ts` | React hook encapsulating timer state and lifecycle |
| **urgency utils** | `web/src/utils/urgency.ts` | Calculates urgency level for color shifts and expressions |
| **CharacterFace** | `web/src/components/CharacterFace.tsx` | Pac-Man-style animated face that reacts to urgency |
| **TimerDisplay** | `web/src/components/TimerDisplay.tsx` | Formatted countdown display with 8-bit styling |
| **TimerContainer** | `web/src/components/TimerContainer.tsx` | Top-level timer orchestration component |

---

## Project Structure

```
.
├── app/                        # FastAPI backend application
│   ├── main.py                 # Application entry point, middleware, router registration
│   ├── config.py               # Settings loaded from environment variables
│   ├── database.py             # SQLAlchemy engine, session management
│   ├── models/
│   │   └── timer.py            # Timer ORM model
│   ├── repos/
│   │   └── timer_repo.py       # Timer database access methods
│   ├── routers/
│   │   ├── health.py           # GET /health endpoint
│   │   └── timers.py           # Timer CRUD endpoints
│   └── services/
│       └── timer_service.py    # Timer business logic
├── migrations/
│   └── 001_create_timers.sql   # Initial database schema migration
├── tests/                      # Backend pytest test suite
│   ├── conftest.py             # Fixtures, test database setup
│   ├── test_timer_service.py   # Unit tests for timer service
│   └── test_timers_api.py      # Integration tests for timer API routes
├── web/                        # React + Vite frontend
│   ├── index.html              # HTML entry point
│   ├── vite.config.ts          # Vite build and dev server configuration
│   ├── tailwind.config.ts      # Tailwind CSS configuration
│   ├── tsconfig.json           # TypeScript compiler configuration
│   ├── package.json            # Frontend dependencies and scripts
│   └── src/
│       ├── main.tsx            # React DOM entry point
│       ├── App.tsx             # Root application component
│       ├── index.css           # Global styles and Tailwind imports
│       ├── api/
│       │   └── timerApi.ts     # HTTP client for backend API
│       ├── components/
│       │   ├── CharacterFace.tsx       # Animated Pac-Man character
│       │   ├── CharacterFace.test.tsx  # Component tests
│       │   ├── ControlButtons.tsx      # Start / pause / reset controls
│       │   ├── DurationInput.tsx       # Timer duration input form
│       │   ├── TimerContainer.tsx      # Main timer layout component
│       │   └── TimerDisplay.tsx        # Formatted time display
│       ├── hooks/
│       │   └── useTimer.ts     # Timer state and countdown logic
│       ├── types/
│       │   └── timer.ts        # Shared TypeScript interfaces and types
│       └── utils/
│           ├── urgency.ts      # Urgency level computation
│           └── urgency.test.ts # Urgency utility unit tests
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── forge_plan.json             # Project blueprint metadata
```

---

## Setup & Installation

### Prerequisites

- Python **3.11+**
- Node.js **18+** and npm
- PostgreSQL **14+** running locally or remotely
- `git`

### 1. Clone the Repository

```bash
git clone <repository-url>
cd blueprint-countdown-timer
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your local values (see [Environment Variables](#environment-variables) below).

### 3. Backend Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Database Setup

Ensure your PostgreSQL server is running, then apply the migration:

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

### Run the Backend

From the project root with your virtual environment activated:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive API docs (Swagger UI) are at `http://localhost:8000/docs`.

### Run the Frontend

```bash
cd web
npm run dev
```

The frontend dev server will start at `http://localhost:5173` and proxy API requests to the backend.

### Build the Frontend for Production

```bash
cd web
npm run build
```

Compiled assets will be output to `web/dist/`.

---

## Environment Variables

Copy `.env.example` to `.env` and populate the following keys before running the application. **Never commit real credentials.**

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (e.g. `postgresql://user:pass@localhost:5432/dbname`) |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port (default: `5432`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `SECRET_KEY` | Application secret key for security utilities |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins |
| `ENVIRONMENT` | Deployment environment (`development`, `production`) |
| `VITE_API_BASE_URL` | *(Frontend)* Base URL for the backend API |

> **Note:** Frontend environment variables prefixed with `VITE_` are injected at build time by Vite and must be set in `web/.env` or `web/.env.local`.

---

## API Routes

All routes are served from the FastAPI backend at the configured host/port.

### Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Returns service health status |

### Timers

| Method | Path | Description |
|---|---|---|
| `GET` | `/timers` | List all timers |
| `POST` | `/timers` | Create a new timer |
| `GET` | `/timers/{timer_id}` | Retrieve a specific timer by ID |
| `PUT` | `/timers/{timer_id}` | Update a timer (duration, name, state) |
| `DELETE` | `/timers/{timer_id}` | Delete a timer |

> Full request/response schemas are available via the auto-generated Swagger UI at `/docs` or ReDoc at `/redoc`.

---

## Testing

### Backend Tests (pytest)

```bash
# From the project root with virtual environment activated
pytest tests/ -v
```

To run a specific test file:

```bash
pytest tests/test_timer_service.py -v
pytest tests/test_timers_api.py -v
```

To generate a coverage report:

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Frontend Tests (Vitest)

```bash
cd web
npm run test
```

To run in watch mode:

```bash
npm run test -- --watch
```

Key