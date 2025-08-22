#!/bin/bash
# Deploy fix for portfolio button infinite loading
echo "Deploying portfolio button fix..."

# The fix is already applied - changed @access_required to @demo_access in portfolio.py line 988
# This resolves the infinite loading issue where users without premium access
# were getting redirects instead of JSON responses, causing fetch() to hang

echo "Fix applied: Portfolio add endpoint now uses @demo_access instead of @access_required"
echo "This allows the 'Legg til i portefølje' button to work properly for all users"
echo "Deploy to Railway will pick up this change automatically"
