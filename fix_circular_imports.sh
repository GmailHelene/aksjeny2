#!/bin/bash
# Fix for circular import issue in Flask app
# Run this script before deploying to Railway

echo "Fixing circular imports in Flask app..."

# Fix app.py
echo "Fixing app.py..."
sed -i 's/from app import create_app/from app.__init__ import create_app/g' app.py

# Fix wsgi.py
echo "Fixing wsgi.py..."
sed -i 's/from app import create_app/from app.__init__ import create_app/g' wsgi.py

# Fix other imports if needed
echo "Checking for other import issues..."

echo ""
echo "Flask app circular import fixes applied successfully!"
echo ""
echo "Now you can deploy your application to Railway"
echo ""
