# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 | https://nodejs.org/en/download |
| PostgreSQL | 14.0 | https://www.postgresql.org/download/windows/ |
| PowerShell | 5.1 (built into Windows 10/11) | Pre-installed on Windows 10/11 |

**How to check if these are already installed:**
Open PowerShell (press `Windows Key + X`, then click "Windows PowerShell") and type:

```
python --version
node --version
psql --version
```

Each command should print a version number. If you see an error instead, that software needs to be installed.

**PostgreSQL setup note:** During PostgreSQL installation, you will be asked to create a password for the default `postgres` user. Write this password down — you will need it later. The default username is `postgres`.

---

## 2. Install

**Step 1 — Open PowerShell in the project folder.**

Navigate to the folder where you downloaded or extracted this project. Right-click inside the folder while holding `Shift`, then select "Open PowerShell window here." Alternatively, in PowerShell type:

```powershell
cd "C:\path\to\your\project"
```

Replace `C:\path\to\your\project` with the actual folder path.

**Step 2 — Install Python dependencies (backend).**

Run this command from the root of the project folder:

```powershell
pip install -r requirements.txt
```

Wait for it to finish. You will see packages being downloaded and installed.

**Step 3 — Install Node.js dependencies (frontend).**

Navigate into the `web` subfolder, then install:

```powershell
cd web
npm install
cd ..
```

This downloads the visual interface components. It may take a minute or two.

---

## 3. Credential / API Setup

This application does not connect to any third-party online services and does not require API keys or external accounts.

The only credential you need is access to your own **local PostgreSQL database**, which you installed in the Prerequisites step. No sign-up or external service is required.

**Create the database:**

Open PowerShell and run:

```powershell
psql -U postgres -c "CREATE DATABASE countdown_timer;"
```

When prompted, enter the PostgreSQL password you created during installation.

Then apply the initial database setup:

```powershell
psql -U postgres -d countdown_timer -f migrations/001_create_timers.sql
```

---

## 4. Configure .env

The `.env` file tells the application how to connect to your database and how to run. You create it by copying the provided example file.

**Create your .env file:**

```powershell
Copy-Item .env.example .env
```

This creates a file called `.env` in the project root. Open it with any text editor (Notepad works fine) and review the settings below.

**All environment variables explained:**

| Variable | What it does | Required? | Default value |
|---|---|---|---|
| `DATABASE_URL` | Full address to your PostgreSQL database, including username, password, host, and database name | Optional | `postgresql://postgres:postgres@localhost:5432/countdown_timer` |
| `CORS_ORIGINS` | Which web addresses are allowed to talk to the backend | Optional | `http://localhost:5173,http://localhost:3000` |
| `APP_ENV` | Sets whether the app runs in development or production mode | Optional | `development` |
| `DEBUG` | Shows extra error details when something goes wrong | Optional | `true` |
| `HOST` | The network address the backend server listens on | Optional | `127.0.0.1` |
| `PORT` | The port number the backend server uses | Optional | `8000` |
| `FRONTEND_URL` | The web address of the visual interface | Optional | `http://localhost:5173` |
| `DB_POOL_MIN_SIZE` | Minimum number of held-open database connections | Optional | `5` |
| `DB_POOL_MAX_SIZE` | Maximum number of simultaneous database connections | Optional | `20` |
| `DB_CONNECTION_TIMEOUT` | How many seconds to wait when connecting to the database before giving up | Optional | `30` |
| `DB_QUERY_TIMEOUT` | How many seconds a database query is allowed to run before it is cancelled | Optional | `60` |
| `LOG_LEVEL` | How much detail appears in the application logs (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | Optional | `INFO` |

**Important:** If your PostgreSQL password is not `postgres`, update the `DATABASE_URL` line in `.env`. Replace the second `postgres` (before the `@` symbol) with your actual password:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/countdown_timer
```

---

## 5. Run

**Starting the application (both backend and frontend together):**

From the project root folder in PowerShell, run the included boot script:

```powershell
.\boot.ps1
```

If PowerShell says "running scripts is disabled," run this command first to allow local scripts, then try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**What this starts:**
- The **backend API server** at `http://localhost:8000`
- The **frontend visual interface** at `http://localhost:5173`

**Starting the frontend manually (if needed):**

```powershell
cd web
npm run dev
```

**Starting the backend manually (if needed):**

From the project root:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Accessing the app:**

Once both services are running, open your web browser and go to:

```
http://localhost:5173
```

You should see the retro countdown timer interface.

---

## 6. Stop

**To stop the application:**

Click on the PowerShell window where the app is running and press:

```
Ctrl + C
```

Hold the `Ctrl` key and tap `C`. The server will shut down gracefully. If you opened separate PowerShell windows for the backend and frontend, press `Ctrl + C` in each one.

You do **not** need to do anything special to stop PostgreSQL — it runs as a background Windows service and can be left running.

---

## 7. Key Settings Explained

| Setting | Plain-language explanation |
|---|---|
| `PORT` | The "door number" the backend server answers on. The default is `8000`. If another program on your computer already uses port 8000, change this to something like `8080`. |
| `HOST` | Controls who can reach the backend. `127.0.0.1` means only your own computer can connect, which is safest for local use. |
| `APP_ENV` | Set to `development` while testing and exploring. Set to `production` when deploying for real use — this disables some developer-only features. |
| `DEBUG` | When `true`, you see detailed error messages in the browser and terminal. Set to `false` in production so sensitive details are not exposed. |
| `LOG_LEVEL` | Controls how chatty the application logs are. `DEBUG` shows everything (useful when troubleshooting). `INFO` shows normal activity. `WARNING` or `ERROR` shows only problems. |
| `DB_POOL_MIN_SIZE` | The number of database connections kept open and ready at all times. A larger number means faster responses under load, but uses more memory. |
| `DB_POOL_MAX_SIZE` | The upper limit on simultaneous database connections. Increase this only if many users are hitting the app at the same time. |
| `DB_CONNECTION_TIMEOUT` | If the database takes longer than this many seconds to respond when connecting, the app stops waiting and reports an error. |
| `DB_QUERY_TIMEOUT` | If a single database operation takes longer than this many seconds, it is cancelled. Prevents the app from freezing due to a slow query. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `psql: error: connection to server on socket failed` | PostgreSQL is not running | Open the Windows Start Menu, search for "Services," find "postgresql," right-click it, and choose "Start." |
| `FATAL: password authentication failed for user "postgres"` | Wrong password in `DATABASE_URL` | Open `.env`, find `DATABASE_URL`, and replace `postgres` (the password part before `@`) with the password you set during PostgreSQL installation. |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell security policy is blocking the script | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell, then try `.\boot.ps1` again. |
| Browser shows "Cannot connect" or blank page at `localhost:5173` | Frontend is not running | Make sure you ran `npm install` inside the `web/` folder and that the frontend started without errors. Check the PowerShell window for red error text. |
| `ModuleNotFoundError` when starting the backend | Python dependencies are missing or used the wrong Python | Run `pip install -r requirements.txt` again from the project root. If you have multiple Python versions, try `pip3 install -r requirements.txt`. |
| `address already in use` on port 8000 or 5173 | Another program is using that port | Change `PORT` in `.env` to a different number (e.g., `8080`) for the backend, or stop the other program using that port. For the frontend port, edit `web/vite.config.ts` and set a different `server.port` value. |