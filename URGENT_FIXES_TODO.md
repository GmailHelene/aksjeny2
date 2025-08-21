# URGENT FIXES TODO - August 21, 2025

## ✅ FIXED IMMEDIATELY
- [x] Fix Jinja2 template error - 'content' block defined twice

## 🎨 COLOR AND STYLING FIXES
- [x] Fix buttons that changed from black to brown - reverted to black
- [x] Change all purple/violet colors to dark green (ROI calculator, backtest, news article)
- [x] Change light yellow backgrounds to dark yellow
- [x] Change light green backgrounds to dark green  
- [x] Change light pink backgrounds to dark pink/red
- [x] Fix ROI calculator banner - changed purple to dark green, icons should now show properly

## 🔧 NAVIGATION AND LAYOUT FIXES
- [x] Move "Ressurser" from main navigation to footer only
- [x] Fix mobile search field in footer - added more space above/below
- [x] Fix sector analysis dropdown menu going off mobile screen - made responsive
- [x] Move forum link as separate element in footer (not in submenu)
- [x] Remove "Screener visning" from main navigation under Analyse
- [x] Fix /analysis/ai search field responsiveness on mobile
- [ ] Compare screener solutions and remove duplicate from navigation

## 🚫 500 ERROR FIXES (HIGH PRIORITY)
- [ ] /profile - 500 error
- [ ] /compare - 500 error  
- [ ] /forum - 500 error
- [ ] /analysis/ai - improve search field responsiveness
- [ ] /norwegian-intel/social-sentiment - Build error
- [ ] /norwegian-intel/government-impact - 500 error
- [ ] /external-data/analyst-coverage - 500 error
- [ ] /external-data/market-intelligence - 500 error
- [ ] /market-intel/economic-indicators - 500 error
- [ ] /market-intel/sector-analysis - 500 error
- [ ] /market-intel/earnings-calendar - 500 error
- [ ] /stocks/compare - 500 error
- [ ] /norwegian-intel/oil-correlation - 500 error
- [ ] /norwegian-intel/shipping-intelligence - 500 error
- [ ] /portfolio/overview - 500 error
- [ ] /portfolio/analytics - 500 error
- [ ] /forum/category/--- - 500 error
- [ ] /forum/topic/--- - 500 error
- [ ] /forum/search?q=test - 500 error

## 🔧 FUNCTIONALITY FIXES
- [ ] Fix notification toggles on profile page (email notifications not updating)
- [ ] Fix ticker-specific recommendations URLs
- [ ] Check if /watchlist/ uses real data or hardcoded mockup for paying users
- [ ] Fix PWA app startup - black circle should show white logo

## 💔 EXISTING UNFIXED ISSUES
- [ ] /price-alerts/create - "Kunne ikke opprette prisvarsel"
- [ ] Fix sentiment analysis technical error for AFG.OL and other symbols
- [ ] TradingView charts not loading on stock details pages
- [ ] Buttons not working on stock details (Favoritt, Portefølje, Kjøp)
- [ ] Technical analysis tabs empty (RSI, MACD)
- [ ] /pro-tools/screener - "Method not allowed"
- [ ] /notifications - "Error loading notifications"
- [ ] Cannot delete portfolios (/portfolio/)
- [ ] Fix PC navigation positioning - move KONTO submenu to prevent off-screen

## PRIORITY ORDER
1. Fix 500 errors (blocks core functionality)
2. Fix navigation and layout issues
3. Fix color/styling issues
4. Fix functionality issues
5. Address existing unfixed issues
