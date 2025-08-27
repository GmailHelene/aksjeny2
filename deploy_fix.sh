#!/bin/bash

echo "================================================"
echo " FIXED DEPLOYMENT SCRIPT FOR CIRCULAR IMPORTS"
echo "================================================"
echo

echo "This script will deploy your application with" 
echo "the circular import fix to Railway."
echo

echo "1. Validating the fix..."
python3 -c "import sys; sys.path.insert(0, '.'); import flask; import flask_login; from app.__init__ import create_app; app = create_app('production'); print('✅ Fix validation successful!')"

if [ $? -ne 0 ]; then
    echo
    echo "❌ Validation failed. Please check your code."
    echo
    exit 1
fi

echo
echo "2. Deploying to Railway..."
echo

railway up

if [ $? -ne 0 ]; then
    echo
    echo "❌ Deployment failed."
    echo
    exit 1
fi

echo
echo "✅ Deployment completed successfully!"
echo
echo "To check logs, run:"
echo "railway logs"
echo
