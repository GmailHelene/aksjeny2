#!/bin/bash

echo "🚂 Railway Emergency Fix Deployment"

# Clear all Python cache
echo "🧹 Clearing all cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true

# Add all changes
echo "📦 Adding all changes..."
git add -A

# Commit with fix message
echo "💾 Committing fixes..."
git commit -m "CRITICAL FIX: Fix crypto template error and stock data issues" || echo "No changes to commit"

# Force push to trigger Railway deployment
echo "🚀 Force pushing to Railway..."
git push origin main --force

echo "✅ Fix deployed! Check Railway dashboard for deployment status."
echo "📊 Monitor logs at: https://railway.app/dashboard"
