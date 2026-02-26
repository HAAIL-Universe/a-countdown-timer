# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 | https://nodejs.org/en/download |
| PostgreSQL | 14.0 | https://www.postgresql.org/download/windows/ |
| PowerShell | 5.1 (built into Windows 10/11) | Already installed on modern Windows |

**How to check if these are already installed:**
Open PowerShell (search "PowerShell" in the Start menu) and type each command below, then press Enter:

- `python --version`
- `node --version`
- `npm --version`
- `psql --version`

If a version number appears, that program is already installed.

---

## 2. Install

Follow these steps in order. All commands are run in PowerShell.

**Step 1 — Navigate to the project folder**

Open PowerShell and change directory to wherever you saved the project. For example:
```
cd C:\Users\YourName\Downloads\countdown-timer
```

**Step 2 — Install Python dependencies (backend)**

From the root of the project folder, run:
```
pip install -r requirements.txt
```
This installs the Python packages the server needs. Wait for it to finish.

**Step 3 — Install JavaScript dependencies (frontend)**

Navigate into the `web` folder:
```
cd web
npm install
```
Then go back to the root folder:
```
cd ..
```

---

## 3. Credential / API Setup

No external credentials required.

This project runs entirely on your local computer. It does not connect to any third-party APIs, payment systems, or external services. You only need a working PostgreSQL database on your own machine (set up in the next section).

---

## 4. Configure .env

The `.env` file tells the application how to connect to your database and how to run itself. You need to create this file once before starting the app.

**Create the .env file by copying the example:**
```
copy .env.example .env
```

Then open the new `.env` file in Notepad or any text editor and adjust the values as needed.

**Environment Variables Explained:**

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `DATABASE_URL` | The address and login details for your PostgreSQL database | Optional | `postgresql://postgres:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | Which web addresses are allowed to talk to the backend | Optional | `http://localhost:5173,http://localhost:3000` |
| `APP_ENV` | Sets whether the app runs in development or production mode | Optional | `development` |
| `SERVER_PORT` | The port number the backend server listens on | Optional | `8000` |
| `SERVER_HOST` | The network address the backend server binds to | Optional | `127.0.0.1` |
| `DEBUG` | Turns on extra error messages to help diagnose problems | Optional | `True` |

**Important — Setting up your database:**

The default `DATABASE_URL` assumes:
- PostgreSQL username: `postgres`
- PostgreSQL password: `password`
- Database name: `timer_db`

If your PostgreSQL installation uses a different username or password, update `DATABASE_URL` accordingly. The format is:
```
postgresql://USERNAME:PASSWORD@localhost:5432/timer_db
```

You also need to create the `timer_db` database before running the app. Open PowerShell and run:
```
psql -U postgres -c "CREATE DATABASE timer_db;"
```
Enter your PostgreSQL password when prompted.

Then apply the database schema:
```
psql -U postgres -d timer_db -f migrations/001_create_timers.sql
```

---

## 5. Run

**Starting the application (recommended — uses the boot script):**

From the project root folder in PowerShell, run:
```
.\boot.ps1
```

This single command starts both the backend server and the frontend together.

> **Note:** If PowerShell shows a security error about running scripts, run this command first to allow local scripts, then try again:
> ```
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**Starting services individually (if the boot script does not work):**

Open **two separate PowerShell windows**.

In the first window (backend):
```
cd C:\path\to\countdown-timer
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

In the second window (frontend):
```
cd C:\path\to\countdown-timer\web
npm run dev
```

**Accessing the app:**

Once running, open your web browser and go to:
```
http://localhost:5173
```

The backend API is available at:
```
http://localhost:8000
```

---

## 6. Stop

**To stop the application:**

Click on the PowerShell window running the app and press:
```
Ctrl + C
```

You will see a message confirming the server has shut down. If you started the frontend and backend in separate windows, press `Ctrl + C` in each window.

It is safe to close the PowerShell windows after stopping.

---

## 7. Key Settings Explained

| Setting | Plain-Language Explanation |
|---|---|
| `SERVER_PORT` | The "door number" the backend uses on your computer. `8000` is the default. If another program already uses port 8000, change this to something like `8001`. |
| `SERVER_HOST` | Tells the server which network to listen on. `127.0.0.1` means "this computer only" — nothing outside your machine can reach it, which is safe for local use. |
| `DATABASE_URL` | The full address of your database, including username, password, and the database name. Think of it like a mailing address for the app to find its data. |
| `APP_ENV` | When set to `development`, the app shows detailed error messages. Change to `production` if you are sharing this with others. |
| `DEBUG` | When `True`, extra diagnostic information is printed to the console. Set to `False` to reduce console clutter once everything is working. |
| `CORS_ORIGINS` | A list of web addresses that are permitted to communicate with the backend. You should not need to change this for local use. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `psycopg2.OperationalError: could not connect to server` | PostgreSQL is not running or `DATABASE_URL` credentials are wrong | Open the Windows Start menu, search "Services", find "postgresql", and click Start. Also double-check your username and password in `.env`. |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell script execution is blocked by Windows security policy | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell, then try again. |
| Browser shows "This site can't be reached" at localhost:5173 | The frontend (npm) is not running | Make sure you ran `npm run dev` inside the `web` folder and that it shows "Local: http://localhost:5173" in the console. |
| `pip` is not recognized as a command | Python is not installed or not added to your system PATH | Re-install Python from https://www.python.org/downloads/ and check the box that says **"Add Python to PATH"** during installation. |
| `relation "timers" does not exist` | The database migration has not been applied | Run `psql -U postgres -d timer_db -f migrations/001_create_timers.sql` to create the required database tables. |
| Port 8000 is already in use | Another program is using port 8000 | Change `SERVER_PORT` in your `.env` file to a different number (e.g., `8001`) and restart the app. |