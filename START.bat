@echo off
color 0A
cls

echo ================================================================
echo                    JOB DEKHO - STARTING
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/2] Checking database...
if not exist "job_dekho.db" (
    echo Database not found. Initializing...
    python init_db.py
    if errorlevel 1 (
        echo ERROR: Database initialization failed!
        pause
        exit /b 1
    )
) else (
    echo Database found: job_dekho.db
)

echo.
echo [2/2] Starting Flask application...
echo.
echo ================================================================
echo   APPLICATION RUNNING AT: http://127.0.0.1:5000
echo ================================================================
echo.
echo TEST ACCOUNTS:
echo   Admin:   admin@jobdekho.com / admin123
echo   Student: rahul.sharma@student.com / student123  
echo   Company: hr@techcorp.com / company123
echo.
echo Press CTRL+C to stop the server
echo ================================================================
echo.

timeout /t 2 >nul
start http://127.0.0.1:5000

python app.py

pause
