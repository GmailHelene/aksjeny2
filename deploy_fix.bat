@echo off
echo ================================================
echo  FIXED DEPLOYMENT SCRIPT FOR CIRCULAR IMPORTS
echo ================================================
echo.

echo This script will deploy your application with 
echo the circular import fix to Railway.
echo.

echo 1. Validating the fix...
python -c "import sys; sys.path.insert(0, '.'); import flask; import flask_login; from app.__init__ import create_app; app = create_app('production'); print('✅ Fix validation successful!')"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Validation failed. Please check your code.
    echo.
    exit /b 1
)

echo.
echo 2. Deploying to Railway...
echo.

railway up

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Deployment failed.
    echo.
    exit /b 1
)

echo.
echo ✅ Deployment completed successfully!
echo.
echo To check logs, run:
echo railway logs
echo.

pause
