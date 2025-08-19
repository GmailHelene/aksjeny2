#!/bin/bash

echo "🧹 Starting complete cache clear and deployment..."

# Stop any running Flask processes
echo "⏹️  Stopping Flask processes..."
pkill -f flask || true
pkill -f python || true

# Clear Python cache
echo "🗑️  Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Clear Flask cache
echo "🗑️  Clearing Flask cache..."
rm -rf instance/* 2>/dev/null || true
rm -rf flask_session/* 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true

# Clear browser cache hint
echo "💡 Remember to clear browser cache (Ctrl+Shift+R)"

# Git operations
echo "📦 Adding all changes to git..."
git add -A

echo "💾 Committing changes..."
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "Fix: Crypto and global stocks templates, clear cache - $TIMESTAMP" || echo "No changes to commit"

echo "📤 Pushing to repository..."
git push origin main

echo "✅ Deployment complete!"
echo "🔄 Please restart your Flask application"
