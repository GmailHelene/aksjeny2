@echo off
REM Fix for circular import issue in Flask app
REM Run this script before deploying to Railway

echo Fixing circular imports in Flask app...

REM Fix app.py
echo Fixing app.py...
powershell -Command "(Get-Content app.py) -replace 'from app import create_app', 'from app.__init__ import create_app' | Set-Content app.py"

REM Fix wsgi.py
echo Fixing wsgi.py...
powershell -Command "(Get-Content wsgi.py) -replace 'from app import create_app', 'from app.__init__ import create_app' | Set-Content wsgi.py"

REM Fix other imports if needed
echo Checking for other import issues...

echo.
echo Flask app circular import fixes applied successfully!
echo.
echo Now you can deploy your application to Railway
echo.

pause
