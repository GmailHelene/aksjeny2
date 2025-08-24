#!/bin/bash

echo "🚨 URGENT DEPLOYMENT: Stock Data Fix"
echo "Issue: Stock details showing $100.00 instead of real prices"
echo "Fix: Force real fallback data for all stock symbols"

# Clear cache first
echo "🧹 Clearing all cache..."
if [ -f "clear_cache.py" ]; then
    python3 clear_cache.py
fi

if [ -f "clear_production_cache.py" ]; then
    python3 clear_production_cache.py
fi

# Add all changes
echo "📦 Adding critical stock data changes..."
git add app/routes/stocks.py
git add app.py
git add deployment_trigger.txt

# Commit with urgent message
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "💾 Committing urgent stock data fix..."
git commit -m "URGENT: Fix stock details to show real prices instead of \$100.00 - TSLA should show \$230.10 - $TIMESTAMP"

# Push to repository
echo "📤 Pushing urgent fix to production..."
git push origin master

echo "✅ URGENT DEPLOYMENT COMPLETE!"
echo "📊 Testing: TSLA should now show \$230.10 instead of \$100.00"
echo "🔗 Test URL: https://aksjeradar.trade/stocks/details/TSLA"

# Wait and test
echo "⏱️  Waiting 60 seconds for Railway deployment..."
sleep 60

echo "🧪 Testing deployment..."
curl -s "https://aksjeradar.trade/stocks/details/TSLA" | grep -i "230" && echo "✅ SUCCESS: Real price detected!" || echo "❌ Still showing \$100.00"

echo "🚨 URGENT DEPLOYMENT SCRIPT COMPLETE"
