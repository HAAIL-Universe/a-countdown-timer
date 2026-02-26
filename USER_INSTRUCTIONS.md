# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 | https://nodejs.org/en/download |
| PostgreSQL | 14.0 | https://www.postgresql.org/download/windows/ |
| PowerShell | 5.1 (built into Windows 10/11) | Already installed on most Windows machines |

> **Tip — Checking your versions:** Open PowerShell and run these commands one at a time to confirm everything is installed correctly:
> - `python --version`
> - `node --version`
> - `psql --version`

---

## 2. Install

Follow these steps in order. Open **PowerShell** in the root folder of the project before starting.

> **How to open PowerShell in the project folder:** Navigate to the project folder in File Explorer, click the address bar at the top, type `powershell`, and press Enter.

**Step 1 — Install Python dependencies (backend)**

Run this command from the root of the project folder:

```
pip install -r requirements.txt
```

Wait for it to finish. You will see a confirmation message when all packages are downloaded.

**Step 2 — Install JavaScript dependencies (frontend)**

Navigate into the `web` subfolder and install:

```
cd web
npm install
cd ..
```

This downloads all the pieces needed to run the visual timer interface in your browser.

**Step 3 — Set up the PostgreSQL database**

Open the **PostgreSQL command-line tool** (search for `psql` in your Start menu) and run:

```sql
CREATE DATABASE timer_db;
```

Then run the included migration to create the required tables. From the root project folder in PowerShell:

```
psql -U postgres -d timer_db -f migrations/001_create_timers.sql
```

You will be prompted for your PostgreSQL password (the default password set during PostgreSQL installation is usually `postgres`).

---

## 3. Credential / API Setup

No external credentials required.

This application runs entirely on your own computer using a local database. No third-party accounts, API keys, or internet-based services are needed.

---

## 4. Configure .env

The project includes a ready-made example configuration file. You need to copy it to create your own settings file.

**Run this command in the root project folder:**

```
Copy-Item .env.example .env
```

This creates a file called `.env` in the root folder. You can open it in any text editor (such as Notepad) to review or change the settings.

**All available settings are listed below:**

| Variable | What it does | Required? | Default value |
|---|---|---|---|
| `DATABASE_URL` | The address and login details for your PostgreSQL database. Points the app to where timer data is stored. | Optional | `postgresql+asyncpg://postgres:postgres@localhost:5432/timer_db` |
| `CORS_ORIGINS` | A list of web addresses that are allowed to communicate with the backend. Keeps the frontend and backend connected. | Optional | `http://localhost:5173,http://localhost:8000` |
| `BACKEND_HOST` | The network address the backend server listens on. `0.0.0.0` means it accepts connections from this machine. | Optional | `0.0.0.0` |
| `BACKEND_PORT` | The numbered "door" (port) the backend server uses. | Optional | `8000` |
| `FRONTEND_PORT` | The numbered "door" the visual interface uses in your browser. | Optional | `5173` |
| `ENVIRONMENT` | Tells the app whether it is running for development or production use. | Optional | `development` |
| `LOG_LEVEL` | How much detail the app writes to its activity log. `INFO` is a good balance. | Optional | `INFO` |

> **Important:** If your PostgreSQL password is different from the default `postgres`, update the `DATABASE_URL` line. For example, if your password is `mypassword`, change it to:
> `DATABASE_URL=postgresql+asyncpg://postgres:mypassword@localhost:5432/timer_db`

---

## 5. Run

**Starting the application (recommended — automatic boot script)**

The project includes a boot script that starts both the backend and frontend for you automatically. From the root project folder in PowerShell, run:

```
.\boot.ps1
```

> **If you see a permissions error**, PowerShell may be blocking scripts. Run this command first to allow it, then try again:
> ```
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

**Once started, open your browser and go to:**
- **Timer App (frontend):** http://localhost:5173
- **Backend API (for troubleshooting):** http://localhost:8000

---

**Starting manually (if the boot script does not work)**

Open **two separate PowerShell windows**.

*Window 1 — Start the backend:*
```
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

*Window 2 — Start the frontend:*
```
cd web
npm run dev
```

Then open your browser and go to http://localhost:5173.

---

## 6. Stop

**To stop the application:**

1. Click on the PowerShell window(s) running the app.
2. Press **Ctrl + C** on your keyboard.
3. You may be asked `Terminate batch job (Y/N)?` — type `Y` and press Enter.

If you used the boot script, pressing **Ctrl + C** once in that window will stop both the backend and frontend together.

---

## 7. Key Settings Explained

| Setting | Plain-language explanation |
|---|---|
| `BACKEND_PORT` | Think of this as the door number the backend server sits behind. The default `8000` is fine unless another program on your computer already uses that number. |
| `FRONTEND_PORT` | The door number your browser uses to reach the timer's visual interface. Default is `5173`. If you change this, update `CORS_ORIGINS` to match. |
| `DATABASE_URL` | The full address to reach your database, including your username, password, computer address, and database name — all in one line. |
| `CORS_ORIGINS` | A security setting that lists which web addresses are trusted to talk to the backend. If you change either port, add the new address here separated by a comma. |
| `ENVIRONMENT` | Set to `development` while using the app normally on your machine. You would only change this to `production` if deploying to a web server. |
| `LOG_LEVEL` | Controls how chatty the app is in its logs. `INFO` gives useful updates. `DEBUG` gives much more detail (helpful when something goes wrong). `WARNING` shows only problems. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `psycopg2` or `asyncpg` connection error on startup | PostgreSQL is not running or the password in `DATABASE_URL` is wrong | Open the Windows **Services** app (search "Services"), find **postgresql**, and click **Start**. Also double-check your password in the `.env` file. |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell script execution is blocked by Windows security settings | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` in PowerShell, then try again. |
| Browser shows "This site can't be reached" at localhost:5173 | The frontend has not started yet, or it started on a different port | Check the PowerShell window for the frontend — look for the line showing the actual address. Confirm `FRONTEND_PORT` in `.env` matches. |
| `relation "timers" does not exist` error in the backend log | The database migration script was not run | Run `psql -U postgres -d timer_db -f migrations/001_create_timers.sql` to create the required tables. |
| `npm install` fails with permission or network errors | Node.js is outdated or npm's cache is corrupted | Run `npm cache clean --force` then try `npm install` again. Make sure Node.js is version 18 or newer (`node --version`). |
| Timer data is not saved after closing the app | The app connected but the database was not set up correctly | Confirm the `timer_db` database exists in PostgreSQL and the migration was applied. Re-run the migration command from Step 2 if unsure. |