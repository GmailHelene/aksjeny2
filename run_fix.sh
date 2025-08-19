#!/bin/bash

echo "🔧 Running complete fix..."

# Make Python script executable
chmod +x fix_all_issues.py

# Run the fix
python3 fix_all_issues.py

echo ""
echo "✅ Fix complete!"
echo "🔍 Next steps:"
echo "1. Check Railway dashboard for deployment status"
echo "2. Wait 1-2 minutes for deployment to complete"
echo "3. Visit https://aksjeradar.trade to verify fixes"
echo "4. Clear browser cache (Ctrl+Shift+R) if needed"
