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
Open PowerShell (search "PowerShell" in the Start Menu) and type each command below, pressing Enter after each:

```
python --version
node --version
npm --version
psql --version
```

Each should show a version number. If you see an error instead, that software needs to be installed.

---

## 2. Install

Follow these steps in order. All commands are typed into PowerShell.

**Step 1 — Navigate to the project folder.**
Replace `C:\path\to\project` with the actual location of the project on your computer:

```
cd C:\path\to\project
```

**Step 2 — Create a PostgreSQL database.**
Open the PostgreSQL command prompt (installed with PostgreSQL, search "SQL Shell" in Start Menu) and run:

```
CREATE DATABASE timer_db;
CREATE USER "user" WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE timer_db TO "user";
\q
```

**Step 3 — Apply the database structure.**
Back in PowerShell, run:

```
psql -U user -d timer_db -f migrations/001_create_timers.sql
```

**Step 4 — Install Python dependencies** (run from the main project folder):

```
pip install -r requirements.txt
```

**Step 5 — Install frontend (website) dependencies** (navigate into the `web` folder first):

```
cd web
npm install
cd ..
```

---

## 3. Credential / API Setup

No external credentials required.

This application runs entirely on your own computer using a local database. You do not need any API keys, accounts, or third-party services.

---

## 4. Configure .env

The `.env` file is a simple text file that holds settings for the application. You need to create it from the provided example file.

**Create your `.env` file by running this command in PowerShell from the main project folder:**

```
Copy-Item .env.example .env
```

Then open `.env` in any text editor (such as Notepad) and adjust the values if needed. Below is a full explanation of every setting:

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `DATABASE_URL` | The full address of your PostgreSQL database, including username, password, and database name | Optional | `postgresql://user:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | Which web addresses are allowed to talk to the backend. Rarely needs changing during local use. | Optional | `http://localhost:3000,http://localhost:5173` |
| `ENVIRONMENT` | Sets whether the app runs in development (testing) or production (live) mode | Optional | `development` |
| `HOST` | The network address the backend listens on. `0.0.0.0` means "all local addresses" | Optional | `0.0.0.0` |
| `PORT` | The numbered "door" on your computer the backend uses. Change this if something else is already using port 8000. | Optional | `8000` |
| `LOG_LEVEL` | How much detail the app writes to its activity log. `INFO` is a good balance. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR` | Optional | `INFO` |
| `DB_POOL_MIN_SIZE` | Minimum number of simultaneous database connections kept open | Optional | `10` |
| `DB_POOL_MAX_SIZE` | Maximum number of simultaneous database connections allowed | Optional | `20` |
| `DB_POOL_TIMEOUT` | How many seconds to wait before giving up on a database connection | Optional | `30` |
| `REQUEST_TIMEOUT` | How many seconds the backend waits before cancelling a slow request | Optional | `30` |

**For most users, you only need to update `DATABASE_URL`** if your PostgreSQL username or password is different from the defaults (`user` / `password`).

---

## 5. Run

**Starting the full application using the boot script:**

From the main project folder in PowerShell, run:

```
.\boot.ps1
```

This single command starts both the backend (Python/FastAPI) and frontend (React website) together.

**If PowerShell blocks the script** with a security warning, first run this once to allow it:

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Then try `.\boot.ps1` again.

**Starting each part manually (if needed):**

*Backend only* — from the main project folder:
```
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

*Frontend only* — from the `web` folder:
```
cd web
npm run dev
```

**Once running, open your web browser and go to:**
- **Timer app (frontend):** http://localhost:5173
- **Backend API (for troubleshooting):** http://localhost:8000

---

## 6. Stop

To stop the application, click on the PowerShell window where it is running and press:

```
Ctrl + C
```

Hold the **Ctrl** key and press **C** at the same time. You may need to press it once for the frontend and once for the backend if they are running in separate windows. The application will shut down safely.

---

## 7. Key Settings Explained

| Setting | Plain-Language Explanation |
|---|---|
| `PORT` | Think of this like a door number on your computer. The backend listens at door number `8000`. If another program is already using that door, change this to something like `8001`. You would then visit `http://localhost:8001` instead. |
| `ENVIRONMENT` | When set to `development`, the app shows extra error details to help diagnose problems. When set to `production`, it hides those details for security. Use `development` while learning and testing. |
| `DATABASE_URL` | This is the full "address" to find your database. The format is `postgresql://USERNAME:PASSWORD@LOCATION:PORT/DATABASE_NAME`. If you changed your PostgreSQL username or password during installation, update this accordingly. |
| `LOG_LEVEL` | Controls how chatty the application is in its activity log. `DEBUG` shows everything (useful when something goes wrong). `INFO` shows normal activity. `WARNING` and `ERROR` show only problems. |
| `DB_POOL_MIN_SIZE` / `DB_POOL_MAX_SIZE` | The app keeps a set of database "telephone lines" open and ready. Min is the number always kept open; Max is the most it will ever open at once. For personal use, the defaults are more than enough. |
| `REQUEST_TIMEOUT` | If the app is waiting for something (like a database response) and it takes longer than this many seconds, it gives up and shows an error. Increase this number on slow computers. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `could not connect to server` or database connection error | PostgreSQL is not running, or `DATABASE_URL` credentials are wrong | Open Windows Services (search "Services" in Start Menu), find **PostgreSQL**, and click **Start**. Also double-check the username and password in your `.env` file match what you set up in PostgreSQL. |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell's security policy is blocking the script | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` in PowerShell, then try again. |
| Browser shows `This site can't be reached` at localhost:5173 | The frontend did not start, or is still starting up | Wait 15–20 seconds and refresh. If still failing, start the frontend manually: `cd web` then `npm run dev`. Check for errors printed in the PowerShell window. |
| `pip` is not recognized as a command | Python was not added to your system PATH during installation | Re-run the Python installer, choose **Modify**, and check the box for **Add Python to PATH**. Restart PowerShell afterwards. |
| `npm` is not recognized as a command | Node.js was not added to PATH, or was just installed | Restart PowerShell after installing Node.js. If still not working, restart your computer so the PATH update takes effect. |
| Timer data is lost after restarting / `relation "timers" does not exist` | The database migration script was not run | From the project folder, run: `psql -U user -d timer_db -f migrations/001_create_timers.sql` |