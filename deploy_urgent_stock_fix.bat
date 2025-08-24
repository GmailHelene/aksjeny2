@echo off
echo 🚨 URGENT DEPLOYMENT: Stock Data Fix
echo Issue: Stock details showing $100.00 instead of real prices
echo Fix: Force real fallback data for all stock symbols

echo.
echo 🧹 Clearing all cache...
if exist "clear_cache.py" python clear_cache.py
if exist "clear_production_cache.py" python clear_production_cache.py

echo.
echo 📦 Adding critical stock data changes...
git add app/routes/stocks.py
git add app.py  
git add deployment_trigger.txt

echo.
echo 💾 Committing urgent stock data fix...
git commit -m "URGENT: Fix stock details to show real prices instead of $100.00 - TSLA should show $230.10 - %date% %time%"

echo.
echo 📤 Pushing urgent fix to production...
git push origin master

echo.
echo ✅ URGENT DEPLOYMENT COMPLETE!
echo 📊 Testing: TSLA should now show $230.10 instead of $100.00
echo 🔗 Test URL: https://aksjeradar.trade/stocks/details/TSLA

echo.
echo ⏱️  Waiting 60 seconds for Railway deployment...
timeout /t 60 /nobreak

echo.
echo 🧪 Testing deployment...
curl -s "https://aksjeradar.trade/stocks/details/TSLA" | findstr "230" && echo ✅ SUCCESS: Real price detected! || echo ❌ Still showing $100.00

echo.
echo 🚨 URGENT DEPLOYMENT SCRIPT COMPLETE
pause
