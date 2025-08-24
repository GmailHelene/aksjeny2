@echo off
echo === Deploying Stock Data Fix ===

echo Adding changes to git...
git add app/routes/stocks.py

echo Committing changes...
git commit -m "Fix stock details to show real data for authenticated users - Priority fix for authenticated user price display"

echo Pushing to master branch...
git push origin master

echo.
echo === Changes pushed to GitHub ===
echo Railway should auto-deploy from master branch...

echo.
echo Waiting 30 seconds for Railway deployment...
timeout /t 30 /nobreak

echo.
echo === Testing deployment ===
curl -s "https://aksjeradar.trade/stocks/details/TSLA" | findstr /i "100.00"
if errorlevel 1 (
    echo Stock data fix appears to be working
) else (
    echo Still showing $100.00 - deployment may need more time
)

echo.
echo === Deployment script complete ===
echo Check https://aksjeradar.trade/stocks/details/TSLA for updated prices
pause
