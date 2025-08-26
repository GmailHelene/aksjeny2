@echo off
REM Emergency Translation Fix Deployment Script for Windows

echo 🚨 EMERGENCY TRANSLATION FIX DEPLOYMENT
echo =========================================

REM Step 1: Clear Python cache
echo 1️⃣ Clearing Python cache files...
for /r %%i in (*.pyc) do del "%%i" 2>nul
for /d /r %%i in (__pycache__) do rd /s /q "%%i" 2>nul

REM Step 2: Git operations  
echo 2️⃣ Committing translation fix...
git add app/utils/translation.py
git commit -m "URGENT: Fix IndentationError in translation.py line 545 - Complete site crash fix"

REM Step 3: Deploy
echo 3️⃣ Deploying to production...
git push origin main

echo ✅ Deployment complete!
echo.
echo MANUAL STEPS REQUIRED:
echo - Restart production server (Railway/Docker/PM2)
echo - Test: https://aksjeradar.trade/market-intel/sector-analysis
echo - Verify no 500 errors on any page
pause
