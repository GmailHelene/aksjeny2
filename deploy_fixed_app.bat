@echo off
echo ===================================================
echo DEPLOY SCRIPT FOR FIXING CIRCULAR IMPORT ISSUES
echo ===================================================
echo.
echo This script will deploy your application with the
echo fixed circular import structure to prevent errors
echo.
echo Starting deployment...
echo.

REM First, check if we can import the app to validate the fix
echo Validating fixes...
python -c "import importlib.util; import os; init_path = os.path.join(os.path.dirname(__file__), 'app', '__init__.py'); spec = importlib.util.spec_from_file_location('app_init', init_path); app_init = importlib.util.module_from_spec(spec); spec.loader.exec_module(app_init); app = app_init.create_app('production'); print('✅ App can be imported correctly')"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Error: Fix validation failed. Please check your code.
    echo.
    exit /b 1
)

echo.
echo ✅ Fix validation successful!
echo.
echo Deploying to Railway...
echo.

REM Run the Railway deployment command - adjust as needed
railway up

echo.
echo Deployment completed!
echo.
echo If you encounter any issues, check the logs with:
echo railway logs
echo.

pause
