#!/bin/bash

echo "🚂 Railway Deployment Script"

# Clear cache
echo "🧹 Clearing cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Add all changes
echo "📦 Adding changes..."
git add -A

# Commit
echo "💾 Committing..."
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "Deploy to Railway: $TIMESTAMP" || echo "No changes to commit"

# Push to trigger Railway deployment
echo "🚀 Pushing to trigger Railway deployment..."
git push origin main

echo "✅ Pushed! Railway will automatically deploy the changes."
echo "📊 Check deployment status at: https://railway.app/dashboard"
