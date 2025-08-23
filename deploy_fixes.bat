@echo off
echo 🚀 DEPLOYING STOCK SEARCH & COMPARE FIXES
echo ==========================================

echo 📋 Adding all changes to git...
git add .

echo 💾 Committing fixes...
git commit -m "Fix stock search and compare functionality - Remove conflicting route from main.py that was intercepting stocks blueprint - Verify @demo_access decorators on stocks.search and stocks.compare routes - Ensure both endpoints are in public_endpoints whitelist - Fix route conflicts that prevented proper blueprint resolution"

echo 🚢 Pushing to production...
git push origin main

echo ⏰ Deployment complete! Railway should deploy in 2-3 minutes.
echo 🔍 Run final_verification_script.py after deployment to verify fixes.
echo.
echo 📊 Expected results after deployment:
echo   ✅ /stocks/search?q=tesla - Shows search interface, finds Tesla results
echo   ✅ /stocks/compare - Shows comparison tool interface  
echo   ❌ Should NOT show 'demo-modus aktivert' or promotional content
echo.
echo 🏁 Deployment script complete!
pause
