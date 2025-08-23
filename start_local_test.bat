@echo off
echo 🚀 AKSJERADAR LOKAL TESTING - QUICK START
echo ========================================

echo 📋 Sjekker Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python ikke funnet! Installer Python først.
    pause
    exit /b 1
)

echo 📦 Installerer nødvendige pakker...
pip install flask jinja2 requests werkzeug

echo 🏃 Starter lokal test server...
echo.
echo 📍 Server vil kjøre på: http://localhost:5555
echo 🔍 Test aksjesøk: http://localhost:5555/stocks/search?q=tesla
echo 📊 Test sammenligning: http://localhost:5555/stocks/compare
echo 🏠 Dashboard: http://localhost:5555
echo.
echo 💡 Tips: Åpne http://localhost:5555 i nettleseren
echo 🛑 Stopp med Ctrl+C
echo.

python local_test_server.py

echo.
echo 👋 Server stoppet!
pause
