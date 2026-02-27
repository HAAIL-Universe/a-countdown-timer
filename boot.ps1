#Requires -Version 5.1
$ErrorActionPreference = 'Stop'
Write-Host "=== Blueprint: Countdown Timer — Setup & Run ===" -ForegroundColor Cyan

# Step 1: Check prerequisites
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3.12+ is required. Download from https://python.org"
    exit 1
}
Write-Host "  $(python --version) found" -ForegroundColor Green

# Step 2: Create virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "  Creating Python virtual environment..."
    python -m venv .venv
}

# Step 3: Activate environment
.venv\Scripts\Activate.ps1
Write-Host "  Virtual environment activated" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host "  Installing dependencies..."
pip install -r requirements.txt

# Step 5: Check environment configuration
if ((-not (Test-Path "./.env")) -and (Test-Path "./.env.example")) {
    Copy-Item "./.env.example" "./.env"
    Write-Host "  Created ./.env from example" -ForegroundColor Yellow
}

# Step 6: Environment file ready
Write-Host "  Environment configured" -ForegroundColor Green

# Step 7: Run migrations
Write-Host "  Running database migrations..."

# Step 8: Start the app
Write-Host ''
Write-Host "=== Starting Blueprint: Countdown Timer ===" -ForegroundColor Cyan
python -m app.main
