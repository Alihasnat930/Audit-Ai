@echo off
REM ========================================
REM AuditAI - Environment Setup Script
REM Windows Batch Version
REM ========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   AuditAI Project Setup
echo ========================================
echo.

set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

REM Step 1: Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo [INFO] Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python found.
echo.

REM Step 2: Setup Backend
echo [2/5] Setting up Backend environment...
if not exist "backend\venv" (
    echo [INFO] Creating virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [INFO] Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
    echo [OK] Backend virtual environment created and dependencies installed.
) else (
    echo [OK] Backend virtual environment already exists.
)
echo.

REM Step 3: Check Node.js
echo [3/5] Setting up Frontend environment...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo [INFO] Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found.

if not exist "frontend\node_modules" (
    echo [INFO] Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    echo [OK] Frontend dependencies installed.
) else (
    echo [OK] Frontend dependencies already exist.
)
echo.

REM Step 4: Database Configuration
echo [4/5] Database configuration...
echo [INFO] Using Supabase - no local database required.
echo [INFO] Update your .env file with Supabase connection details:
echo [INFO]   DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
echo [INFO]   SUPABASE_KEY=your_supabase_key
echo [INFO]   SUPABASE_URL=your_supabase_url
echo [OK] Database configuration noted.
echo.

REM Step 5: Model Training
echo [5/5] AI Model Training (Optional)
echo [INFO] Training machine learning models...
echo [INFO] This may take a minute or two...
echo.
cd backend
call venv\Scripts\activate.bat
python ..\train_models.py
cd ..
echo [OK] Model training completed.
echo.

REM Summary
echo.
echo ========================================
echo   ✓ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Start the project with one of these commands:
echo.
echo    Option A: Double-click run.bat
echo    Option B: Run in PowerShell: .\run.bat
echo    Option C: Docker: docker-compose up
echo.
echo 2. Access the application:
echo.
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 3. Login with demo credentials:
echo.
echo    Email:    admin@auditai.com
echo    Password: demo123456
echo.
echo Troubleshooting:
echo - If database error: Ensure PostgreSQL is running or use Docker
echo - If Node.js error: Install from https://nodejs.org/
echo - If Python error: Install from https://www.python.org/
echo.
pause
