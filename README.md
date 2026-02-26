# Blueprint: Countdown Timer

> A retro 8-bit countdown experience — Pac-Man expressions, urgency color shifts, and rock-solid persistence.

---

## Overview

**Blueprint: Countdown Timer** is a full-stack countdown timer application built with a nostalgic 8-bit aesthetic. Users can create, manage, and track countdown timers that persist across sessions via a PostgreSQL database. As time winds down, the interface reacts dynamically — Pac-Man-style character faces shift expression and the color palette escalates urgency, giving every deadline a personality.

**Who it's for:**
- Developers and power users who want a self-hosted, persistent timer with style.
- Teams needing a retro-flavored time-tracking tool for sprints, presentations, or events.
- Anyone who wants their deadlines to stare back at them.

---

## Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| **Backend Language** | Python 3.11+ | Primary application language |
| **Backend Framework** | FastAPI | Async REST API with automatic OpenAPI docs |
| **Database** | PostgreSQL | Persistent timer storage |
| **ORM / DB Access** | SQLAlchemy / psycopg2 | Via `app/database.py` |
| **Frontend Framework** | React 18+ | Component-based UI |
| **Frontend Language** | TypeScript | Strict typing across all components |
| **Build Tool** | Vite | Fast dev server and production bundler |
| **Styling** | Tailwind CSS | Utility-first styling with retro customization |
| **Frontend Testing** | Vitest / Testing Library | Component and utility unit tests |
| **Backend Testing** | Pytest | Service and API integration tests |
| **Migrations** | Raw SQL | Managed via `migrations/` directory |

---

## Architecture

The application follows a layered, separation-of-concerns architecture split between a Python backend and a React frontend.

```
┌─────────────────────────────────────────────────────┐
│                  React + Vite Frontend               │
│  (web/src/)                                          │
│  Components → Hooks → API Client → FastAPI Backend  │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP / REST (JSON)
┌───────────────────────▼─────────────────────────────┐
│                  FastAPI Backend (app/)               │
│                                                      │
│  Routers → Services → Repositories → Database        │
└───────────────────────┬─────────────────────────────┘
                        │ SQL
┌───────────────────────▼─────────────────────────────┐
│               PostgreSQL Database                    │
│        (schema managed via migrations/)              │
└─────────────────────────────────────────────────────┘
```

### Component Descriptions

| Component | Location | Responsibility |
|---|---|---|
| **Routers** | `app/routers/` | HTTP route definitions; request/response handling |
| **Services** | `app/services/` | Business logic — timer lifecycle, state computation |
| **Repositories** | `app/repos/` | Data access layer; all SQL queries isolated here |
| **Models** | `app/models/` | SQLAlchemy ORM models and Pydantic schemas |
| **Database** | `app/database.py` | Session management and engine configuration |
| **Config** | `app/config.py` | Environment-driven settings via Pydantic BaseSettings |
| **API Client** | `web/src/api/timerApi.ts` | Typed fetch wrapper for backend communication |
| **Hooks** | `web/src/hooks/useTimer.ts` | React state and timer tick logic |
| **Urgency Utils** | `web/src/utils/urgency.ts` | Computes color palette and expression level by time remaining |
| **CharacterFace** | `web/src/components/CharacterFace.tsx` | Pac-Man-style animated expression component |
| **TimerDisplay** | `web/src/components/TimerDisplay.tsx` | Formatted countdown rendering |
| **TimerContainer** | `web/src/components/TimerContainer.tsx` | Top-level timer orchestration component |

---

## Project Structure

```
blueprint-countdown-timer/
├── app/                        # FastAPI backend application
│   ├── main.py                 # Application entry point, middleware, router registration
│   ├── config.py               # Settings and environment variable binding
│   ├── database.py             # Database engine and session factory
│   ├── models/
│   │   └── timer.py            # Timer ORM model and Pydantic schemas
│   ├── repos/
│   │   └── timer_repo.py       # Timer CRUD repository
│   ├── routers/
│   │   ├── health.py           # GET /health endpoint
│   │   └── timers.py           # Timer REST endpoints
│   └── services/
│       └── timer_service.py    # Timer business logic
│
├── migrations/
│   └── 001_create_timers.sql   # Initial database schema
│
├── tests/                      # Backend test suite (Pytest)
│   ├── conftest.py             # Shared fixtures and test DB setup
│   ├── test_timer_service.py   # Unit tests for timer service
│   └── test_timers_api.py      # Integration tests for API routes
│
├── web/                        # React + Vite frontend
│   ├── index.html              # HTML entry point
│   ├── vite.config.ts          # Vite configuration and proxy settings
│   ├── tailwind.config.ts      # Tailwind CSS configuration
│   ├── tsconfig.json           # TypeScript compiler options
│   └── src/
│       ├── main.tsx            # React application bootstrap
│       ├── App.tsx             # Root application component
│       ├── index.css           # Global styles and Tailwind imports
│       ├── types/timer.ts      # Shared TypeScript type definitions
│       ├── api/timerApi.ts     # Backend API client
│       ├── hooks/useTimer.ts   # Timer state and tick hook
│       ├── utils/
│       │   ├── urgency.ts      # Urgency level and color computation
│       │   └── urgency.test.ts # Urgency utility unit tests
│       └── components/
│           ├── CharacterFace.tsx       # 8-bit face expression component
│           ├── CharacterFace.test.tsx  # Component tests
│           ├── TimerDisplay.tsx        # Countdown display
│           ├── TimerContainer.tsx      # Timer orchestration
│           ├── ControlButtons.tsx      # Start / pause / reset controls
│           └── DurationInput.tsx       # Timer duration entry form
│
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── package-lock.json           # Root-level lockfile
```

---

## Setup & Installation

### Prerequisites

- Python **3.11+**
- Node.js **18+** and npm
- PostgreSQL **14+** running locally or remotely
- `pip` and `venv` for Python dependency management

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/blueprint-countdown-timer.git
cd blueprint-countdown-timer
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

See the [Environment Variables](#environment-variables) section for all required keys.

### 3. Set Up the Backend

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Provision the Database

Ensure your PostgreSQL instance is running, then apply the migration:

```bash
psql -U <your_db_user> -d <your_db_name> -f migrations/001_create_timers.sql
```

### 5. Set Up the Frontend

```bash
cd web
npm install
```

---

## Usage / Running

### Start the Backend (FastAPI)

From the project root with your virtual environment active:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive API documentation: `http://localhost:8000/docs`

### Start the Frontend (React + Vite)

In a separate terminal:

```bash
cd web
npm run dev
```

The frontend will be available at `http://localhost:5173` and proxies API requests to the backend automatically via `vite.config.ts`.

### Production Build (Frontend)

```bash
cd web
npm run build
# Output is generated in web/dist/
```

---

## Environment Variables

Copy `.env.example` to `.env` and populate the following keys before running the application. **Never commit real credentials.**

| Variable | Description |
|---|---|
| `DATABASE_URL` | Full PostgreSQL connection string (e.g. `postgresql://user:pass@localhost:5432/dbname`) |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port (default: `5432`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `SECRET_KEY` | Application secret key for security utilities |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins (e.g. `http://localhost:5173`) |
| `DEBUG` | Enable debug mode (`true` / `false`) |
| `VITE_API_BASE_URL` | Frontend: base URL of the FastAPI backend |

---

## API Routes

All routes are prefixed from the FastAPI application root. Full interactive documentation is available at `/docs` when the server is running.

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
| `PUT` | `/timers/{id}` | Update an existing timer |
| `DELETE` | `/timers/{id}` | Delete a timer |
| `POST` | `/timers/{id}/start` | Start or resume a timer |
| `POST` | `/timers/{id}/pause` | Pause a running timer |
| `POST` | `/timers/{id}/reset` | Reset a timer to its original duration |

> Refer to `app/routers/timers.py` for exact request/response schemas and `http://localhost:8000/docs` for the live OpenAPI explorer.

---

## Testing

### Backend Tests (Pytest)

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run all backend tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run a specific test file
pytest tests/test_timer_service.py
pytest tests/test_timers_api.py
```

Test fixtures and shared configuration live in `tests/conftest.py`, which sets up an isolated test database session.

### Frontend Tests (Vitest)

```bash
cd web

# Run all frontend tests
npm run test

# Run tests in watch mode
npm run test -- --watch

# Run with coverage
npm run test -- --coverage
```

Frontend tests cover:
- `web/src/components/CharacterFace.test.tsx` — Character expression rendering
- `web/src/utils/urgency.test.ts` — Urgency level and color shift logic

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository and create a feature branch (`git checkout -b feature/your-feature`).
2. Follow existing code style and architecture conventions.
3. Write or update tests for any changed functionality.
4. Ensure all tests pass before submitting a pull request.
5. Open a pull request with a clear description of the change and its motivation.

For major changes, please open an issue first to discuss the proposed approach.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

> *"The ghost of your deadline is always right behind