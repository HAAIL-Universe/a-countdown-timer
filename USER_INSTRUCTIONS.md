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

Each command should print a version number. If you see an error instead, install that software using the link above.

> **PostgreSQL setup tip:** During PostgreSQL installation, you will be asked to set a password for the default database user (`postgres`). Write this password down — you will need it in the configuration step.

---

## 2. Install

Open PowerShell and follow these steps in order.

**Step 1 — Navigate to the project folder.**
Replace `C:\path\to\project` with the actual location of the project on your computer:

```powershell
cd C:\path\to\project
```

**Step 2 — Install Python dependencies** (this runs from the main project folder):

```powershell
pip install -r requirements.txt
```

**Step 3 — Install frontend (website) dependencies** (this runs from the `web` subfolder):

```powershell
cd web
npm install
cd ..
```

You only need to run these install commands once. After that, you can skip straight to the **Run** section on future uses.

---

## 3. Credential / API Setup

No external credentials or third-party API keys are required for this application.

The only "credential" you need is access to your own PostgreSQL database, which you installed locally in the Prerequisites step. You will configure that connection in the next section using the username and password you chose during PostgreSQL setup.

---

## 4. Configure .env

The `.env` file tells the application how to connect to your database and which web addresses are allowed to talk to it.

**Step 1 — Create your `.env` file** by copying the provided example. Run this from the main project folder in PowerShell:

```powershell
Copy-Item .env.example .env
```

**Step 2 — Open `.env` in a text editor** (Notepad works fine):

```powershell
notepad .env
```

**Step 3 — Review and edit the values** using the table below as a guide.

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `DATABASE_URL` | The full address used to connect to your PostgreSQL database, including your username, password, server location, and database name. | Optional (has a default) | `postgresql://postgres:password@localhost:5432/timer_db` |
| `CORS_ORIGINS` | A comma-separated list of web addresses that are allowed to communicate with the backend. You generally do not need to change this. | Optional (has a default) | `http://localhost:5173,http://localhost:8000` |

**Example `.env` file:**

```
DATABASE_URL=postgresql://postgres:YourPasswordHere@localhost:5432/timer_db
CORS_ORIGINS=http://localhost:5173,http://localhost:8000
```

**Important:** Replace `YourPasswordHere` in `DATABASE_URL` with the PostgreSQL password you set during installation. Leave everything else in `DATABASE_URL` unchanged unless you set up PostgreSQL with a different username or port.

**Step 4 — Create the database.** Open the PostgreSQL command tool (search "psql" or "SQL Shell" in the Start menu), log in with your `postgres` user, and run:

```sql
CREATE DATABASE timer_db;
```

Then type `\q` and press Enter to exit.

---

## 5. Run

Make sure you are in the main project folder in PowerShell, then run the boot script:

```powershell
.\boot.ps1
```

This single command starts both the backend (FastAPI) and the frontend (React) at the same time.

Once it finishes starting up, open your web browser and go to:

```
http://localhost:5173
```

That is where the countdown timer app will appear.

> **If PowerShell blocks the script:** You may see a security warning the first time. Run this command once to allow local scripts, then try `.\boot.ps1` again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

**Starting only the frontend (if needed separately):**

```powershell
cd web
npm run dev
```

---

## 6. Stop

To stop the application, click on the PowerShell window where it is running and press:

```
Ctrl + C
```

Press it once and wait a moment. If the application does not stop, press `Ctrl + C` again. You can then close the PowerShell window safely.

If you started the frontend separately in its own PowerShell window, press `Ctrl + C` in that window as well.

---

## 7. Key Settings Explained

| Setting | Plain-Language Explanation |
|---|---|
| `DATABASE_URL` | Think of this as the full "address and key" to your database. It includes who you are (`postgres`), your password, where the database lives (`localhost` means your own computer), which "door" to use (`5432` is the default PostgreSQL port), and the name of the specific database (`timer_db`). |
| `CORS_ORIGINS` | A security setting that controls which browser addresses are allowed to send requests to the backend. The defaults (`5173` for the frontend, `8000` for the backend) match the development setup automatically. Only change this if you move the app to a different address. |
| Port `5173` | The address your browser uses to reach the visual (frontend) part of the app. This is set automatically by Vite (the frontend tool) and matches the default in `CORS_ORIGINS`. |
| Port `8000` | The address the backend API listens on. The frontend talks to this port behind the scenes. |

---

## 8. Troubleshooting

| Error / Symptom | Likely Cause | Fix |
|---|---|---|
| `could not connect to server` or `Connection refused` on startup | PostgreSQL is not running, or the password in `DATABASE_URL` is wrong. | Open the Windows Start menu, search for **Services**, find **postgresql**, and click **Start**. Also double-check the password in your `.env` file. |
| `database "timer_db" does not exist` | The database was never created. | Open psql (SQL Shell) and run `CREATE DATABASE timer_db;` as described in Section 4. |
| `pip is not recognized` | Python was installed but not added to Windows PATH. | Reinstall Python from python.org and check the box that says **"Add Python to PATH"** during setup. |
| `npm is not recognized` | Node.js is not installed or not on the Windows PATH. | Download and reinstall Node.js from nodejs.org, then restart PowerShell. |
| Browser shows blank page or `Cannot GET /` | The frontend is not running, or you are visiting the wrong port. | Make sure `.\boot.ps1` completed without errors, then visit `http://localhost:5173` (not port 8000). |
| PowerShell says `cannot be loaded because running scripts is disabled` | Windows is blocking PowerShell scripts by default. | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` in PowerShell, then try `.\boot.ps1` again. |