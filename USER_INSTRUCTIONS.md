# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 or higher | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 or higher | https://nodejs.org/en/download |
| PostgreSQL | 14.0 or higher | https://www.postgresql.org/download/windows/ |
| PowerShell | 5.1 or higher (built into Windows 10/11) | Pre-installed on Windows 10/11 |

**Checking what you already have:**
Open PowerShell and run these commands one at a time to check versions:
```
python --version
node --version
npm --version
psql --version
```

> **Important PostgreSQL note:** During PostgreSQL installation, you will be asked to set a password for the default `postgres` user. Write this password down — you will need it later.

---

## 2. Install

Follow these steps in order. All commands are run in PowerShell.

**Step 1 — Navigate to the project folder.**
Replace `C:\path\to\project` with the actual location of the project on your computer:
```
cd C:\path\to\project
```

**Step 2 — Install Python dependencies (backend).**
Run this from the root of the project folder:
```
pip install -r requirements.txt
```
Wait for it to finish. You should see a success message at the end.

**Step 3 — Install JavaScript dependencies (frontend).**
Navigate into the `web` subfolder and install:
```
cd web
npm install
cd ..
```
Wait for it to finish. This may take a minute or two.

**Step 4 — Create the database.**
Open the PostgreSQL command-line tool by running:
```
psql -U postgres
```
Enter the password you set during PostgreSQL installation, then run this command inside the PostgreSQL prompt:
```
CREATE DATABASE timer_db;
```
Then type `\q` and press **Enter** to exit.

**Step 5 — Run the database migration.**
Back in PowerShell (in the project root), apply the initial database setup:
```
psql -U postgres -d timer_db -f migrations/001_create_timers.sql
```
Enter your PostgreSQL password when prompted.

---

## 3. Credential / API Setup

No external credentials required.

This application runs entirely on your local machine. The only "credentials" needed are your PostgreSQL username and password, which you set up yourself during installation (see Section 2, Step 4 above).

---

## 4. Configure .env

The `.env` file tells the application how to connect to your database and how to run. You must create this file before starting the app.

**Step 1 — Create your `.env` file by copying the example:**
```
copy .env.example .env
```

**Step 2 — Open the `.env` file** in Notepad or any text editor and review the settings below.

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `DATABASE_URL` | The full address used to connect to your PostgreSQL database. Must match your PostgreSQL username, password, and database name. | Optional | `postgresql://postgres:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | Tells the backend which web addresses are allowed to talk to it. Leave this as-is unless you change the frontend port. | Optional | `http://localhost:5173,http://localhost:3000` |
| `APP_ENV` | Sets whether the app runs in development or production mode. | Optional | `development` |
| `SERVER_PORT` | The port number the backend API listens on. | Optional | `8000` |
| `SERVER_HOST` | The network address the backend binds to. `127.0.0.1` means it is only accessible on your own computer (recommended). | Optional | `127.0.0.1` |
| `DEBUG` | When set to `True`, the app shows detailed error messages. Useful while getting started. | Optional | `True` |

> **Most important setting:** If your PostgreSQL password is not `password`, you must update the `DATABASE_URL` line. For example, if your password is `MySecret99`, change it to:
> `DATABASE_URL=postgresql://postgres:MySecret99@localhost:5432/timer_db`

---

## 5. Run

Once installation and configuration are complete, use the boot script to start the entire application with a single command.

**Start the application (development mode):**
```
.\boot.ps1
```

> If PowerShell says it cannot run scripts, run this command first to allow local scripts, then try again:
> ```
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

The boot script starts both the backend (FastAPI) and the frontend (React) together.

**Once running, open your web browser and go to:**
```
http://localhost:5173
```

The retro countdown timer interface should appear in your browser.

**To view the backend API directly (optional):**
```
http://localhost:8000
```

**API documentation (auto-generated, optional):**
```
http://localhost:8000/docs
```

---

## 6. Stop

To shut the application down gracefully:

1. Click on the PowerShell window where the app is running.
2. Press **Ctrl + C** on your keyboard.
3. PowerShell may ask *"Terminate batch job (Y/N)?"* — type `Y` and press **Enter**.

Both the backend and frontend will stop. It is safe to close the PowerShell window afterward.

---

## 7. Key Settings Explained

| Setting | Plain-Language Explanation |
|---|---|
| `DATABASE_URL` | Think of this as the "home address + password" for your database. If you change your PostgreSQL password or use a different database name, update this value to match. |
| `SERVER_PORT` | The "door number" the backend API listens on. If another program is already using port `8000`, change this to something else like `8001`, and update `CORS_ORIGINS` accordingly. |
| `SERVER_HOST` | Determines who can reach the backend. `127.0.0.1` means only your own computer. Do not change this unless you know what you are doing. |
| `APP_ENV` | Use `development` while setting up and testing. If you ever deploy this for others to use, change to `production`. |
| `DEBUG` | When `True`, you get detailed error messages if something breaks — helpful for troubleshooting. Set to `False` in a live/production environment. |
| `CORS_ORIGINS` | Lists the web addresses the frontend uses. If you change `SERVER_PORT` on the frontend (in `web/package.json`), add the new address here. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `could not connect to server` or `Connection refused` when starting | PostgreSQL is not running | Open the Windows Start menu, search for **Services**, find **postgresql**, right-click it, and select **Start**. |
| `password authentication failed for user "postgres"` | The password in `DATABASE_URL` does not match your PostgreSQL password | Open `.env` and update `DATABASE_URL` with the correct password you set during PostgreSQL installation. |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell script execution is blocked by Windows | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell, then try `.\boot.ps1` again. |
| Browser shows `localhost refused to connect` or blank page | The frontend or backend did not finish starting | Wait 10–15 seconds and refresh. If still blank, check the PowerShell window for red error messages and refer to the other rows in this table. |
| `npm install` fails with permission errors | npm needs elevated permissions or cache is corrupted | Try running PowerShell as Administrator (right-click PowerShell → "Run as administrator") and repeat `cd web` then `npm install`. |
| `pip install -r requirements.txt` fails with `pip not found` | Python was not added to the system PATH during installation | Reinstall Python from https://www.python.org/downloads/ and check the box that says **"Add Python to PATH"** during setup. |