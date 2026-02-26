# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 | https://nodejs.org/en/download |
| PostgreSQL | 14.0 | https://www.postgresql.org/download/windows/ |
| PowerShell | 5.1 (built into Windows 10/11) | Already installed on most Windows machines |

**How to check if these are already installed:**
Open PowerShell (search "PowerShell" in the Start menu) and type each command below, then press Enter:

- `python --version`
- `node --version`
- `psql --version`

If you see a version number, that program is already installed.

---

## 2. Install

Follow these steps in order. All commands are run in **PowerShell**.

**Step 1 — Navigate to the project folder**

Open PowerShell and change into the project's root folder (replace the path with wherever you saved the project):

```
cd C:\path\to\your\project
```

**Step 2 — Install Python dependencies (backend)**

Run this command from the project root folder:

```
pip install -r requirements.txt
```

This downloads all the Python packages the backend needs. It may take a minute or two.

**Step 3 — Install Node.js dependencies (frontend)**

Move into the `web` folder and install the frontend packages:

```
cd web
npm install
```

Once finished, go back to the root folder:

```
cd ..
```

**Step 4 — Set up the database**

Open the PostgreSQL command tool (called `psql`) and create the database the app will use. In PowerShell:

```
psql -U postgres -c "CREATE DATABASE timer_db;"
```

You will be prompted for the password you chose when you installed PostgreSQL. If the database already exists, you can skip this step.

Next, run the included migration file to create the required tables:

```
psql -U postgres -d timer_db -f migrations/001_create_timers.sql
```

---

## 3. Credential / API Setup

No external credentials required.

This project runs entirely on your own computer. The only "credential" you need is the password for your local PostgreSQL database, which you set when you installed PostgreSQL. You will use that password in the next section when configuring the `.env` file.

---

## 4. Configure .env

The `.env` file tells the application important settings like where to find the database. You must create this file before running the app.

**Step 1 — Create your `.env` file from the example**

Run this command from the project root folder in PowerShell:

```
Copy-Item .env.example .env
```

**Step 2 — Open and edit the file**

Open `.env` in Notepad or any text editor:

```
notepad .env
```

**Step 3 — Fill in your values**

Here is every setting explained:

| Variable | What it does | Required? | Default value |
|---|---|---|---|
| `DATABASE_URL` | The full address the app uses to connect to your PostgreSQL database. Contains the username, password, server address, and database name. | Optional | `postgresql://postgres:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | A list of web addresses that are allowed to talk to the backend. You normally do not need to change this unless you move the app to a different port. | Optional | `http://localhost:5173,http://localhost:8000` |

**Example `.env` file (with a real password filled in):**

```
DATABASE_URL=postgresql://postgres:MyActualPassword@localhost:5432/timer_db
CORS_ORIGINS=http://localhost:5173,http://localhost:8000
```

> **Important:** Replace `MyActualPassword` in `DATABASE_URL` with the actual password you set for PostgreSQL during installation. If you left it as the default during install, it may already be `password`, but it is best to double-check.

Save and close the file when done.

---

## 5. Run

Use the included boot script to start the entire application (both backend and frontend) with a single command.

**Start the application (using the boot script):**

From the project root folder in PowerShell, run:

```
.\boot.ps1
```

If PowerShell shows a security warning like *"cannot be loaded because running scripts is disabled,"* run this command first to allow local scripts, then try again:

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**What happens after you run the boot script:**

- The **backend** (FastAPI) will start and handle data storage and logic.
- The **frontend** (React) will start in development mode and open the timer app in your browser, usually at:
  **http://localhost:5173**

**Starting only the frontend manually (if needed):**

```
cd web
npm run dev
```

---

## 6. Stop

To shut down the application gracefully:

1. Click on the PowerShell window where the app is running.
2. Press **Ctrl + C** on your keyboard.
3. PowerShell may ask *"Terminate batch job (Y/N)?"* — type **Y** and press **Enter**.

If you have separate PowerShell windows open for the backend and frontend, repeat this step in each window.

---

## 7. Key Settings Explained

| Setting | Where it lives | What it controls in plain language |
|---|---|---|
| `DATABASE_URL` | `.env` file | The "address" of your database, including who is logging in (`postgres`), the password, the server location (`localhost`), the port number (`5432`), and the name of the database (`timer_db`). Change the password part if yours is different. |
| `CORS_ORIGINS` | `.env` file | A security setting that controls which browser addresses are allowed to send requests to the backend. The two defaults cover the frontend and backend local addresses. Only change this if you run the app on a different port. |
| Port `5173` | Set by Vite (frontend tool) | The local address where the visual timer app opens in your browser. You can change it in `web/vite.config.ts` if that port is already in use on your machine. |
| Port `8000` | Set by FastAPI (backend) | The local address the backend listens on. The frontend sends timer data here. If you change it, update both the backend startup command and `CORS_ORIGINS`. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `psycopg2.OperationalError: could not connect to server` | The PostgreSQL service is not running, or the password in `DATABASE_URL` is wrong. | Open the Windows Start menu, search for **Services**, find **postgresql**, right-click and choose **Start**. Also double-check the password in your `.env` file. |
| `.\boot.ps1 cannot be loaded, running scripts is disabled` | PowerShell's security policy is blocking local scripts. | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell and then try `.\boot.ps1` again. |
| Browser shows a blank page or "cannot connect" at `localhost:5173` | The frontend has not started yet, or it started on a different port. | Check the PowerShell window for a message like `Local: http://localhost:XXXX`. Open that address in your browser instead. |
| `pip` is not recognized as a command | Python is installed but not added to your system PATH. | Reinstall Python from https://www.python.org/downloads/ and on the first installer screen, check the box that says **"Add Python to PATH"** before clicking Install. |
| `npm install` fails with `ENOENT` or `package.json not found` | You ran `npm install` from the wrong folder. | Make sure you are inside the `web` folder before running `npm install`. Use `cd web` first. |
| Timer data is not saved after restarting the app | The database migration was not run, so the tables do not exist yet. | Run `psql -U postgres -d timer_db -f migrations/001_create_timers.sql` from the project root folder and restart the app. |