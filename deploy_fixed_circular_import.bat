@echo off
echo ====================================================
echo   FLASK APP DEPLOYMENT SCRIPT - FIXING IMPORT ERROR
echo ====================================================
echo.

REM Create a temporary backup of app.py
echo Creating backup of app.py...
copy app.py app.py.bak
if %ERRORLEVEL% neq 0 (
    echo [31m❌ Error: Failed to backup app.py[0m
    exit /b 1
)

REM Rename app.py to avoid import conflict
echo Renaming app.py to avoid circular import issues...
rename app.py _app.py.renamed
if %ERRORLEVEL% neq 0 (
    echo [31m❌ Error: Failed to rename app.py[0m
    exit /b 1
)

echo Using application.py as the main entry point...

REM Set necessary environment variables
set FLASK_APP=application.py
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Deploy to Railway (adjust command as needed)
echo Deploying to Railway...
railway up
if %ERRORLEVEL% neq 0 (
    echo [31m❌ Railway deployment failed[0m
    exit /b 1
)

echo.
echo [32m✅ Deployment complete![0m
echo.
echo If you encounter any issues, check the logs with:
echo railway logs
echo.

pause
