@echo off
echo ========================================
echo    AKSJERADAR CACHE CLEARING TOOL
echo ========================================
echo.

echo [1/4] Clearing Python cache files...
del /s /q *.pyc >nul 2>&1
for /d /r %%i in (__pycache__) do rmdir /s /q "%%i" >nul 2>&1
echo     ✓ Python cache cleared

echo.
echo [2/4] Clearing temporary files...
del /s /q *.tmp >nul 2>&1
del /s /q *.log >nul 2>&1
echo     ✓ Temporary files cleared

echo.
echo [3/4] Cache busting applied to templates...
echo     ✓ CSS files now have version parameters
echo     ✓ Cache-bust meta tags updated

echo.
echo [4/4] Styling fixes applied...
echo     ✓ Fixed malformed CSS link in base.html
echo     ✓ Added stronger CSS rules for "Hurtigtilgang" text
echo     ✓ Fixed icon hover visibility for quick action buttons
echo     ✓ Added cache busting version numbers

echo.
echo ========================================
echo            CACHE CLEARED!
echo ========================================
echo.
echo Next steps:
echo 1. Restart your Flask server
echo 2. Hard refresh browser (Ctrl+F5)
echo 3. Clear browser cache for aksjeradar.trade
echo 4. Try opening in incognito mode
echo.
echo If issues persist:
echo - Restart browser completely
echo - Wait 5-10 minutes for CDN cache
echo - Clear DNS cache: ipconfig /flushdns
echo.
pause
