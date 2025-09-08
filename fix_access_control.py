# This script will fix access control by adding more routes to the DEMO_ACCESSIBLE list
# This ensures authenticated users can access the profile and portfolio routes

from app.utils.access_control_unified import DEMO_ACCESSIBLE, PREMIUM_ONLY

# Routes to add to DEMO_ACCESSIBLE
NEW_DEMO_ROUTES = [
    # Portfolio routes
    'portfolio.portfolio_overview',
    'portfolio.create_portfolio', 
    'portfolio.view_portfolio',
    'portfolio.delete_portfolio',
    'portfolio.add_stock_to_portfolio',
    'portfolio.remove_stock_from_portfolio',
    'portfolio.watchlist',
    'portfolio.stock_tips',
    'portfolio.quick_add_stock',
    # Additional routes to include all portfolio functions
    'portfolio.index',
    'portfolio.create_watchlist',
    'portfolio.add_to_watchlist',
    'portfolio.add_tip',
    'portfolio.tip_feedback',
    # Profile routes
    'profile.profile_page',
    'profile.update_profile',
    'profile.remove_favorite',
    'main.profile',
    'main.update_profile'
]

# Check if routes are already in DEMO_ACCESSIBLE
ADDED_COUNT = 0
for route in NEW_DEMO_ROUTES:
    if route not in DEMO_ACCESSIBLE:
        DEMO_ACCESSIBLE.add(route)
        print(f"Added {route} to DEMO_ACCESSIBLE")
        ADDED_COUNT += 1
        
        # Also remove from PREMIUM_ONLY if it exists there
        if route in PREMIUM_ONLY:
            PREMIUM_ONLY.remove(route)
            print(f"Removed {route} from PREMIUM_ONLY")

print(f"Added {ADDED_COUNT} routes to DEMO_ACCESSIBLE")
print(f"Total routes in DEMO_ACCESSIBLE: {len(DEMO_ACCESSIBLE)}")

# Now update all access_required decorators to unified_access_required
import re
import os

def update_file_decorators(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace @access_required with @unified_access_required
    updated_content = re.sub(r'@access_required', '@unified_access_required', content)
    
    # Replace @demo_access with @unified_access_required
    updated_content = re.sub(r'@demo_access', '@unified_access_required', updated_content)
    
    # Only write if changes were made
    if updated_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    return False

# Update portfolio.py
portfolio_path = os.path.join('app', 'routes', 'portfolio.py')
if os.path.exists(portfolio_path):
    if update_file_decorators(portfolio_path):
        print(f"Updated decorators in {portfolio_path}")
    else:
        print(f"No changes needed in {portfolio_path}")
else:
    print(f"File not found: {portfolio_path}")

print("Access control updates complete!")
