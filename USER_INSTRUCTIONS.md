# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 | https://nodejs.org/en/download |
| PostgreSQL | 14.0 | https://www.postgresql.org/download/windows/ |
| PowerShell | 5.1 (built into Windows 10/11) | Pre-installed on Windows 10/11 |

**To verify your installations**, open PowerShell (search "PowerShell" in the Start menu) and run these commands one at a time:

```
python --version
node --version
npm --version
psql --version
```

Each command should print a version number. If you see an error instead, revisit the installation for that tool.

---

## 2. Install

Follow these steps in order. All commands are run in **PowerShell**.

**Step 1 — Navigate to the project folder**

Open PowerShell and change into the project's root folder (replace the path with wherever you saved the project):

```
cd C:\Users\YourName\countdown-timer
```

**Step 2 — Install Python dependencies (backend)**

From the project root folder, run:

```
pip install -r requirements.txt
```

This downloads all the Python packages the backend needs. It may take a minute or two.

**Step 3 — Install JavaScript dependencies (frontend)**

Navigate into the `web` subfolder, then install:

```
cd web
npm install
cd ..
```

This downloads all the packages the visual interface needs. Return to the root folder with `cd ..` when done.

---

## 3. Credential / API Setup

No external credentials required.

This project runs entirely on your own computer using a local database. You do not need to sign up for any service or obtain any API keys.

---

## 4. Configure .env

The `.env` file tells the application how to connect to your database and how to behave. The project includes a ready-made example file to get you started.

**Create your `.env` file** by running this command from the project root:

```
Copy-Item .env.example .env
```

This creates a copy of the example file named `.env`. You can then open it in any text editor (like Notepad) to make changes.

**List of every environment variable:**

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `DATABASE_URL` | The full address used to connect to your PostgreSQL database, including username, password, host, and database name | Optional | `postgresql://postgres:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | Which web addresses are allowed to talk to the backend. Rarely needs changing for local use | Optional | `http://localhost:5173,http://localhost:3000` |
| `APP_ENV` | Tells the app whether it is running in development or production mode | Optional | `development` |
| `SERVER_PORT` | The port number the backend server listens on | Optional | `8000` |
| `SERVER_HOST` | The network address the backend server binds to | Optional | `127.0.0.1` |
| `DEBUG` | Enables extra logging messages useful for diagnosing problems. Set to `False` in production | Optional | `True` |

**Important:** Update `DATABASE_URL` if your PostgreSQL setup uses a different username, password, or database name than the defaults. For example, if your PostgreSQL password is `mysecret`, change the line to:

```
DATABASE_URL=postgresql://postgres:mysecret@localhost:5432/timer_db
```

**Create the database** before running the app for the first time. Open PowerShell and run:

```
psql -U postgres -c "CREATE DATABASE timer_db;"
```

Then apply the database schema:

```
psql -U postgres -d timer_db -f migrations/001_create_timers.sql
```

---

## 5. Run

**Start the application** using the included boot script. From the project root folder in PowerShell, run:

```
.\boot.ps1
```

If PowerShell blocks the script with a security warning, run this once to allow local scripts, then try again:

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

The boot script starts both the backend and the frontend together. Once it finishes starting up, open your web browser and go to:

```
http://localhost:5173
```

You should see the retro 8-bit countdown timer.

**Development mode only** — To start just the frontend by itself (for example, if the backend is already running separately):

```
cd web
npm run dev
```

---

## 6. Stop

To stop the application, click on the PowerShell window that is running it and press:

```
Ctrl + C
```

Hold the **Ctrl** key and press **C**. PowerShell will ask you to confirm — press **Y** then **Enter** if prompted. This safely shuts down both the backend and frontend servers.

If you opened separate PowerShell windows for the backend and frontend, repeat **Ctrl + C** in each window.

---

## 7. Key Settings Explained

| Setting | Plain-Language Explanation |
|---|---|
| `SERVER_PORT` | The "door number" your backend server uses. If another program is already using port `8000`, change this to something else like `8001`. The frontend must also be told about the new port. |
| `SERVER_HOST` | The network address the backend listens on. The default `127.0.0.1` means "this computer only," which is safe for local use. Do not change this unless you know what you are doing. |
| `DATABASE_URL` | The full connection string for PostgreSQL. It follows the pattern `postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME`. All five parts must match your PostgreSQL setup exactly. |
| `APP_ENV` | Set to `development` while you are testing. Set to `production` when deploying to a real server. This affects how errors are displayed and how strictly the app behaves. |
| `DEBUG` | When set to `True`, the app prints detailed messages to help diagnose problems. Set it to `False` for a cleaner experience once everything is working. |
| `CORS_ORIGINS` | Controls which browser addresses can communicate with the backend. If you change the frontend port away from `5173`, add the new address here separated by a comma. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `psql: error: connection to server failed` | PostgreSQL is not running or not installed correctly | Open the Windows Start menu, search for "Services," find **postgresql**, and click **Start**. Or reinstall PostgreSQL from https://www.postgresql.org/download/windows/ |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell script execution is blocked by Windows security policy | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` in PowerShell, then try again |
| Browser shows a blank page or "Cannot connect" at `localhost:5173` | The frontend did not start, or you are using the wrong address | Make sure `npm install` completed without errors inside the `web/` folder. Check PowerShell for error messages and confirm you are visiting `http://localhost:5173` |
| `pip install` fails with `No module named pip` | Python was installed but `pip` (Python's package installer) is missing or not on your PATH | Reinstall Python from https://www.python.org/downloads/ and check the box that says **"Add Python to PATH"** during setup |
| `password authentication failed for user "postgres"` | The password in `DATABASE_URL` does not match your PostgreSQL password | Open `.env` in Notepad and update `DATABASE_URL` so the password section matches the one you set when you installed PostgreSQL |
| Timer data is not saved between sessions / database errors on startup | The database or its tables do not exist yet | Make sure you ran both the `CREATE DATABASE` command and the `psql ... -f migrations/001_create_timers.sql` command from **Section 4** |