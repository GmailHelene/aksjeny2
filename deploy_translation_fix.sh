#!/bin/bash
# Emergency Translation Fix Deployment Script

echo "🚨 EMERGENCY TRANSLATION FIX DEPLOYMENT"
echo "========================================="

# Step 1: Clear Python cache
echo "1️⃣ Clearing Python cache files..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Step 2: Git operations
echo "2️⃣ Committing translation fix..."
git add app/utils/translation.py
git commit -m "URGENT: Fix IndentationError in translation.py line 545 - Complete site crash fix"

# Step 3: Deploy
echo "3️⃣ Deploying to production..."
git push origin main

echo "✅ Deployment complete!"
echo ""
echo "MANUAL STEPS REQUIRED:"
echo "- Restart production server (Railway/Docker/PM2)"  
echo "- Test: https://aksjeradar.trade/market-intel/sector-analysis"
echo "- Verify no 500 errors on any page"
