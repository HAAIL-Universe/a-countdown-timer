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
Open PowerShell (search "PowerShell" in the Start menu) and type each command below, then press Enter:

```
python --version
node --version
npm --version
psql --version
```

Each command should print a version number. If you see an error instead, that software needs to be installed.

---

## 2. Install

Follow these steps in order. All commands are run in PowerShell.

**Step 1 — Navigate to the project folder**

Replace `C:\path\to\project` with the actual folder where you saved the project files:

```
cd C:\path\to\project
```

**Step 2 — Install Python dependencies (backend)**

Run this command from the root of the project folder:

```
pip install -r requirements.txt
```

Wait for it to finish. You will see packages being downloaded and installed.

**Step 3 — Install JavaScript dependencies (frontend)**

Now move into the `web` folder and install the frontend packages:

```
cd web
npm install
cd ..
```

This may take a minute or two. When done, return to the root project folder.

---

## 3. Credential / API Setup

No external credentials required.

This application runs entirely on your own computer using a local database. No API keys, third-party accounts, or internet services are needed.

---

## 4. Configure .env

The `.env` file tells the application how to connect to your database and which web addresses are allowed to talk to the backend.

**Step 1 — Create your .env file**

Run this command from the root project folder in PowerShell:

```
Copy-Item .env.example .env
```

This creates a new file called `.env` from the provided example. Open it in any text editor (Notepad works fine).

**Step 2 — Review and edit the variables**

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `DATABASE_URL` | The full address used to connect to your PostgreSQL database. Includes the username, password, server location, and database name. | Optional | `postgresql://postgres:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | A list of web addresses that are allowed to communicate with the backend server. Keeps the app secure. | Optional | `http://localhost:5173,http://localhost:8000` |

**Step 3 — Set up the database**

Before running the app, you need to create the database that the timer data will be stored in. Open a PostgreSQL prompt (search "psql" in Start menu) and run:

```
CREATE DATABASE timer_db;
```

If your PostgreSQL username is not `postgres` or your password is not `password`, update the `DATABASE_URL` in your `.env` file to match. The format is:

```
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/timer_db
```

---

## 5. Run

Use the provided boot script to start the full application with a single command.

**Starting the application (recommended method):**

From the root project folder in PowerShell, run:

```
.\boot.ps1
```

> **Note:** If PowerShell shows a security warning about running scripts, type the following command first, then try again:
> ```
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

**Starting services manually (alternative method):**

If the boot script does not work, you can start the backend and frontend separately. Open **two** PowerShell windows.

*In the first PowerShell window (backend):*
```
cd C:\path\to\project
uvicorn app.main:app --reload
```

*In the second PowerShell window (frontend):*
```
cd C:\path\to\project\web
npm run dev
```

**Accessing the application:**

Once running, open your web browser and go to:

```
http://localhost:5173
```

You should see the retro countdown timer interface.

---

## 6. Stop

**If you used the boot script:**

Click on the PowerShell window that is running the app and press:

```
Ctrl + C
```

Press it once for each service if prompted. This safely shuts down both the backend and frontend.

**If you started services in separate windows:**

Go to each PowerShell window and press `Ctrl + C` in each one. You can then close the windows.

---

## 7. Key Settings Explained

| Setting | Plain-Language Explanation |
|---|---|
| `DATABASE_URL` | Think of this like a home address for your database. It tells the app where the database lives (`localhost` means your own computer), which door to knock on (port `5432` is PostgreSQL's default), and the username and password to get in. Only change this if you set up PostgreSQL with a different username, password, or database name. |
| `CORS_ORIGINS` | This is a security list of approved web addresses that can send requests to the backend. The two defaults cover both the frontend page (`5173`) and the backend itself (`8000`). Only advanced users should need to change this. |
| Port `5173` | The address where the visual timer interface is served in your browser. This is set automatically by Vite (the frontend tool) and does not need to be changed for normal use. |
| Port `8000` | The address where the backend API runs. The frontend talks to this behind the scenes to save and load timers. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `psycopg2.OperationalError: could not connect to server` | PostgreSQL is not running, or the connection details in `.env` are wrong. | Open the Windows Start menu, search for "Services," find "postgresql," and click Start. Double-check your `DATABASE_URL` username and password in `.env`. |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell's security policy is blocking the script. | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` in PowerShell, then try again. |
| Browser shows `This site can't be reached` at localhost:5173 | The frontend (npm) is not running. | Open a PowerShell window, navigate to the `web` folder (`cd web`), and run `npm run dev`. |
| `ModuleNotFoundError` when starting the backend | Python dependencies were not installed, or the wrong Python is being used. | Run `pip install -r requirements.txt` again from the root project folder. Make sure `python --version` shows 3.10 or higher. |
| Timer data is not saving between sessions | The database migration has not been applied. | Open psql, connect to `timer_db`, and run the contents of the file `migrations/001_create_timers.sql` manually. |
| `npm install` fails with permission errors | Node.js or npm needs elevated permissions, or there is a network issue. | Right-click the PowerShell icon and choose "Run as Administrator," then re-run `npm install` inside the `web` folder. |