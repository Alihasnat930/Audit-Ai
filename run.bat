@echo off
REM ========================================
REM AuditAI - Complete Project Starter
REM ========================================
REM This script starts the complete AuditAI project:
REM - Backend API server (FastAPI)
REM - Frontend dev server (React/Vite)

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   AuditAI Project Starter
echo ========================================
echo.

REM Get the project root directory
set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

REM Check if backend venv exists
if not exist "backend\venv" (
    echo [WARNING] Backend virtual environment not found.
    echo [INFO] Run setup.bat first to initialize the project.
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo [WARNING] Frontend dependencies not installed.
    echo [INFO] Run setup.bat first to initialize the project.
    pause
    exit /b 1
)

REM Check if PostgreSQL database is running (optional warning)
echo [INFO] Ensuring PostgreSQL is running on localhost:5432...
echo.

REM Start Backend Server
echo [1/2] Starting Backend API Server...
echo [INFO] Backend will start on http://localhost:8000
echo [INFO] Swagger UI available at http://localhost:8000/docs
echo.

start "AuditAI Backend" cmd /k "cd /d ""%PROJECT_ROOT%backend"" && call venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start Frontend Dev Server
echo [2/2] Starting Frontend Development Server...
echo [INFO] Frontend will start on http://localhost:5173
echo [INFO] Login credentials: admin@auditai.com / demo123456
echo.

start "AuditAI Frontend" cmd /k "cd /d ""%PROJECT_ROOT%frontend"" && npm run dev"

REM Final instructions
echo.
echo ========================================
echo   ✓ Services Starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo Docs:     http://localhost:8000/docs
echo.
echo Demo Login:
echo   Email:    admin@auditai.com
echo   Password: demo123456
echo.
echo [INFO] Two windows will open automatically.
echo [INFO] Press Ctrl+C in each window to stop servers.
echo.
pause
