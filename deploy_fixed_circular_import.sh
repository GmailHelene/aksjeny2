#!/bin/bash

echo "===================================================="
echo "  FLASK APP DEPLOYMENT SCRIPT - FIXING IMPORT ERROR"
echo "===================================================="
echo 

# Function to check if a command succeeded
check_result() {
    if [ $? -ne 0 ]; then
        echo "❌ Error: $1"
        exit 1
    fi
}

# Create a temporary backup of app.py
echo "Creating backup of app.py..."
cp app.py app.py.bak
check_result "Failed to backup app.py"

# Rename app.py to avoid import conflict
echo "Renaming app.py to avoid circular import issues..."
mv app.py _app.py.renamed
check_result "Failed to rename app.py"

echo "Using application.py as the main entry point..."

# Set necessary environment variables
export FLASK_APP=application.py
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Deploy to Railway (adjust command as needed)
echo "Deploying to Railway..."
railway up
check_result "Railway deployment failed"

echo
echo "✅ Deployment complete!"
echo
echo "If you encounter any issues, check the logs with:"
echo "railway logs"
echo
