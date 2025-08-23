#!/bin/bash
# AKSJERADAR LOKAL TESTING - QUICK START SCRIPT

echo "🚀 AKSJERADAR LOKAL TESTING - QUICK START"
echo "========================================"

echo "📋 Sjekker Python..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python ikke funnet! Installer Python først."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "📦 Installerer nødvendige pakker..."
$PYTHON_CMD -m pip install flask jinja2 requests werkzeug

echo "🏃 Starter lokal test server..."
echo ""
echo "📍 Server vil kjøre på: http://localhost:5555"
echo "🔍 Test aksjesøk: http://localhost:5555/stocks/search?q=tesla"
echo "📊 Test sammenligning: http://localhost:5555/stocks/compare"
echo "🏠 Dashboard: http://localhost:5555"
echo ""
echo "💡 Tips: Åpne http://localhost:5555 i nettleseren"
echo "🛑 Stopp med Ctrl+C"
echo ""

$PYTHON_CMD local_test_server.py

echo ""
echo "👋 Server stoppet!"
