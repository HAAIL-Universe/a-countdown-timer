# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 | https://nodejs.org/en/download |
| PostgreSQL | 14.0 | https://www.postgresql.org/download/windows/ |
| PowerShell | 5.1 (built into Windows 10/11) | Pre-installed on modern Windows |

**How to check if these are already installed:**
Open PowerShell (search "PowerShell" in the Start menu) and run these commands one at a time:

```
python --version
node --version
psql --version
```

Each command should print a version number. If you see an error instead, that software needs to be installed.

---

## 2. Install

Follow these steps in order. All commands are run in PowerShell.

**Step 1 — Navigate to the project folder**

Open PowerShell and change into the folder where this project lives. For example:

```
cd C:\Users\YourName\Downloads\countdown-timer
```

**Step 2 — Install Python dependencies (backend)**

From the root of the project folder, run:

```
pip install -r requirements.txt
```

This downloads all the Python packages the backend needs. It may take a minute or two.

**Step 3 — Install Node.js dependencies (frontend)**

Now move into the `web` subfolder and install the frontend packages:

```
cd web
npm install
cd ..
```

This downloads the React/Vite packages the visual interface needs.

---

## 3. Credential / API Setup

No external credentials required.

This application runs entirely on your own computer using a local PostgreSQL database. You do not need to sign up for any third-party services or obtain any API keys.

You will, however, need to create a PostgreSQL database on your machine. See **Configure .env** below for instructions.

**Setting up your local database:**

1. Open the **pgAdmin** application that was installed with PostgreSQL, or open PowerShell and run:
   ```
   psql -U postgres
   ```
2. Create the database by typing:
   ```
   CREATE DATABASE timer_db;
   ```
3. Type `\q` and press Enter to exit.
4. Run the setup migration to create the required table:
   ```
   psql -U postgres -d timer_db -f migrations/001_create_timers.sql
   ```

---

## 4. Configure .env

The `.env` file tells the application about your local settings (like your database password). You create it by copying the example file that comes with the project.

**Create your .env file — run this in PowerShell from the project root:**

```
Copy-Item .env.example .env
```

Then open the new `.env` file in Notepad or any text editor and adjust the values as needed.

**Environment variables explained:**

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `DATABASE_URL` | The full address of your PostgreSQL database, including username, password, host, and database name. | Optional | `postgresql://postgres:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | Tells the backend which web addresses are allowed to talk to it. Matches the frontend address. | Optional | `http://localhost:5173,http://localhost:3000` |
| `APP_ENV` | Sets whether the app runs in development or production mode. | Optional | `development` |
| `SERVER_PORT` | The port number the backend API listens on. | Optional | `8000` |
| `SERVER_HOST` | The network address the backend binds to. `127.0.0.1` means your own computer only. | Optional | `127.0.0.1` |
| `DEBUG` | When `True`, shows detailed error messages. Set to `False` for a live/public environment. | Optional | `True` |

**Important:** If your PostgreSQL password is not `password`, you must update `DATABASE_URL`. For example, if your password is `mysecret`, change it to:

```
DATABASE_URL=postgresql://postgres:mysecret@localhost:5432/timer_db
```

---

## 5. Run

**Starting the full application**

From the project root folder in PowerShell, run the boot script:

```
.\boot.ps1
```

This single command starts both the backend (FastAPI) and the frontend (React) together.

If PowerShell shows a security warning about running scripts, you may need to allow it first by running:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then try `.\boot.ps1` again.

**Once running, open your browser and go to:**

- **The app (timer UI):** http://localhost:5173
- **The backend API (optional, for checking):** http://localhost:8000

**Running the frontend only (if needed):**

```
cd web
npm run dev
```

---

## 6. Stop

To shut down the application gracefully:

1. Click on the PowerShell window where the application is running.
2. Press **Ctrl + C** on your keyboard.
3. If prompted with `Terminate batch job (Y/N)?`, type `Y` and press Enter.

If you opened separate PowerShell windows for the backend and frontend, repeat these steps in each window.

---

## 7. Key Settings Explained

| Setting | Plain-Language Explanation |
|---|---|
| `SERVER_PORT` | The "door number" the backend uses on your computer. `8000` is the default. Only change this if another program is already using port 8000. |
| `SERVER_HOST` | The network address the backend listens on. Leave this as `127.0.0.1` — it means only programs on your own computer can reach it, which is safer. |
| `DATABASE_URL` | The full connection string to your PostgreSQL database. Think of it as the address + login credentials for your database. Format: `postgresql://username:password@host:port/database_name`. |
| `APP_ENV` | Switch between `development` (extra error info shown) and `production` (leaner, faster, less verbose). For personal use, `development` is fine. |
| `DEBUG` | When set to `True`, the app shows detailed error messages in the browser and terminal — helpful for diagnosing problems. Set to `False` if you ever share access with others. |
| `CORS_ORIGINS` | A list of web addresses the backend trusts. If you change the port the frontend runs on, add that address here so the two parts of the app can still communicate. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `psycopg2.OperationalError: could not connect to server` | PostgreSQL is not running, or the `DATABASE_URL` password is wrong. | Open the Windows Services app (search "Services"), find **PostgreSQL**, and click Start. Also double-check the password in your `.env` file. |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell script execution is blocked by Windows security policy. | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell as Administrator, then try again. |
| `npm install` fails with `ENOENT` or `node not found` | Node.js is not installed or not added to the system PATH. | Re-install Node.js from https://nodejs.org and restart PowerShell after installation. |
| Browser shows blank page or "Cannot GET /" at http://localhost:5173 | The frontend hasn't finished starting yet, or the `web/` dependencies weren't installed. | Wait 10–15 seconds and refresh. If still blank, run `cd web && npm install` and restart. |
| `pip install -r requirements.txt` fails with `python not found` | Python is not installed or not on the system PATH. | Re-install Python from https://www.python.org — make sure to check **"Add Python to PATH"** during installation. |
| Timer data is lost after restarting the app | The database migration was never run. | Run `psql -U postgres -d timer_db -f migrations/001_create_timers.sql` from the project root to create the required database table. |