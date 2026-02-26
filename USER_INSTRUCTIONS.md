# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 or newer | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 or newer | https://nodejs.org/en/download |
| PostgreSQL | 14.0 or newer | https://www.postgresql.org/download/windows/ |
| PowerShell | 5.1 or newer (included with Windows 10/11) | Pre-installed on Windows 10/11 |

**How to check if these are already installed:**
Open PowerShell (search "PowerShell" in the Start menu) and type the following commands one at a time:

```
python --version
node --version
npm --version
psql --version
```

Each command should print a version number. If you see an error instead, that program needs to be installed.

**PostgreSQL setup note:** During PostgreSQL installation, you will be asked to create a password for the default database user (`postgres`). Write this password down — you will need it in the configuration step.

---

## 2. Install

Once all prerequisites are installed, open PowerShell and follow these steps in order.

**Step 1 — Navigate to the project folder.**
Replace `C:\path\to\project` with the actual location of the project on your computer:

```
cd C:\path\to\project
```

**Step 2 — Install Python dependencies (for the backend):**

```
pip install -r requirements.txt
```

Wait for this to finish. You will see packages being downloaded and installed.

**Step 3 — Install JavaScript dependencies (for the frontend):**

```
cd web
npm install
cd ..
```

Wait for this to finish as well. This may take a minute or two.

---

## 3. Credential / API Setup

This project does not connect to any third-party paid services or require external API keys.

The only credential you need is access to your **local PostgreSQL database**, which you set up yourself during installation. You will use your PostgreSQL username and password in the configuration step below.

---

## 4. Configure .env

The application reads its settings from a file called `.env` located in the main project folder. This file is not included automatically — you must create it from the provided example.

**Step 1 — Create your `.env` file.**
In PowerShell, from the main project folder, run:

```
Copy-Item .env.example .env
```

**Step 2 — Open the `.env` file** in Notepad or any text editor and review each setting below.

**Step 3 — Create the database.**
Before running the app, create a database in PostgreSQL called `timer_db`. Open PowerShell and run:

```
psql -U postgres -c "CREATE DATABASE timer_db;"
```

Enter your PostgreSQL password when prompted.

---

### All Environment Variables

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `DATABASE_URL` | The full address of your PostgreSQL database, including username, password, and database name. | Optional | `postgresql://postgres:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | Tells the backend which web addresses are allowed to talk to it. Leave this as-is for local use. | Optional | `http://localhost:5173,http://localhost:3000` |
| `APP_ENV` | Sets whether the app runs in development or production mode. Use `development` for local use. | Optional | `development` |
| `SERVER_PORT` | The port number the backend server listens on. 8000 is the standard default. | Optional | `8000` |
| `SERVER_HOST` | The network address the backend server runs on. `127.0.0.1` means "this computer only." | Optional | `127.0.0.1` |
| `DEBUG` | When set to `True`, extra error detail is shown. Helpful for troubleshooting. | Optional | `True` |

**Important:** If your PostgreSQL password is not `password`, update the `DATABASE_URL` line in `.env` to match. For example, if your password is `mysecret`:

```
DATABASE_URL=postgresql://postgres:mysecret@localhost:5432/timer_db
```

---

## 5. Run

The project includes a boot script (`boot.ps1`) that starts everything for you automatically.

**To start the application, open PowerShell in the project folder and run:**

```
.\boot.ps1
```

If PowerShell says the script cannot be run due to security restrictions, first run this command to allow local scripts, then try again:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

The boot script will start both the backend (FastAPI) and the frontend (React). Once it's running:

- **Frontend (the timer app):** Open your web browser and go to → `http://localhost:5173`
- **Backend API:** Available at → `http://localhost:8000`

**Development mode (manual alternative):**
If you prefer to start each part separately, open **two** PowerShell windows.

*Window 1 — Backend:*
```
cd C:\path\to\project
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

*Window 2 — Frontend:*
```
cd C:\path\to\project\web
npm run dev
```

---

## 6. Stop

**To stop the application:**

- If you used the boot script (`.\boot.ps1`), click on the PowerShell window and press **Ctrl + C**. Confirm if prompted.
- If you started the backend and frontend in separate windows, press **Ctrl + C** in each window.

The application will shut down gracefully. It is safe to close the PowerShell windows afterward.

---

## 7. Key Settings Explained

| Setting | Plain-Language Explanation |
|---|---|
| `SERVER_PORT` | Think of a port like a door number on a building. The backend listens for requests on door `8000`. You only need to change this if another program on your computer is already using port 8000. |
| `SERVER_HOST` | This is the network "address" the backend runs on. `127.0.0.1` means it only accepts connections from your own computer, keeping it private and secure. |
| `APP_ENV` | Switching this to `production` changes how the app behaves — it hides detailed error messages and is optimized for performance. Leave it as `development` unless you are deploying this publicly. |
| `DEBUG` | When `True`, the app prints detailed information about errors to help with troubleshooting. Set to `False` if you find the extra output distracting. |
| `DATABASE_URL` | The full "address" of your database, including who is logging in (`postgres`), the password, the computer it's on (`localhost`), the port (`5432`), and the database name (`timer_db`). |
| `CORS_ORIGINS` | A security setting that controls which browser addresses can communicate with the backend. If you access the app from an unexpected address, add it here separated by a comma. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `psycopg2.OperationalError: could not connect to server` | PostgreSQL is not running, or the `DATABASE_URL` password is wrong. | Open the Windows Start menu, search for **Services**, find **postgresql**, and click **Start**. Also double-check the password in your `.env` file. |
| `.\boot.ps1 cannot be loaded because running scripts is disabled` | PowerShell's security policy is blocking the script. | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell and try again. |
| Browser shows `Cannot connect` or blank page at `localhost:5173` | The frontend (npm) is not running. | Make sure you ran `npm install` inside the `web/` folder and that the boot script or `npm run dev` is still running in PowerShell. |
| `ModuleNotFoundError` when starting the backend | Python dependencies were not installed, or the wrong Python is being used. | Re-run `pip install -r requirements.txt` from the main project folder. Make sure `python --version` shows 3.10 or newer. |
| `database "timer_db" does not exist` | The PostgreSQL database was never created. | Run `psql -U postgres -c "CREATE DATABASE timer_db;"` in PowerShell, then restart the app. |
| Timer data is lost after restarting | The database migration (table setup) may not have run. | Run the migration manually: `psql -U postgres -d timer_db -f migrations/001_create_timers.sql` |