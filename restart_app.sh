#!/bin/bash

echo "🔄 Restarting Flask application..."

# Kill existing Flask/Python processes
echo "⏹️  Stopping existing processes..."
pkill -f "python.*app.py" || true
pkill -f "flask run" || true
pkill -f "gunicorn" || true

# Wait a moment
sleep 2

# Clear Python cache for good measure
echo "🗑️  Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Start Flask in development mode
echo "🚀 Starting Flask application..."
cd /workspaces/aksjeny

# Export environment variables if needed
export FLASK_APP=app.py
export FLASK_ENV=development

# Start Flask
python app.py &

echo "✅ Flask application restarted!"
echo "🌐 Application should be available at http://localhost:5002"
