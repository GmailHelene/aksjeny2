# Update portfolio routes to use unified access control
import os
import re
import sys
from datetime import datetime

def create_backup(file_path):
    """Create a backup of the file"""
    backup_path = f"{file_path}.bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(file_path, 'r', encoding='utf-8') as src:
        with open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(src.read())
    print(f"Created backup at {backup_path}")
    return backup_path

def replace_decorators(file_path):
    """Replace old access decorators with unified_access_required"""
    # Create backup
    backup_path = create_backup(file_path)
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if unified_access_required is already imported
    if 'from ..utils.access_control_unified import unified_access_required' not in content:
        # Add import for unified_access_required
        content = content.replace(
            'from ..utils.access_control import access_required, demo_access',
            'from ..utils.access_control import access_required, demo_access\nfrom ..utils.access_control_unified import unified_access_required'
        )
    
    # Replace @access_required with @unified_access_required
    modified_content = re.sub(
        r'@access_required',
        '@unified_access_required',
        content
    )
    
    # Replace @demo_access with @unified_access_required
    modified_content = re.sub(
        r'@demo_access',
        '@unified_access_required',
        modified_content
    )
    
    # Count the replacements
    access_required_count = content.count('@access_required')
    demo_access_count = content.count('@demo_access')
    
    # Write the modified content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"Replaced {access_required_count} @access_required and {demo_access_count} @demo_access decorators with @unified_access_required")
    
    return access_required_count + demo_access_count

def update_portfolio_file():
    """Update the portfolio.py file"""
    portfolio_path = os.path.join('app', 'routes', 'portfolio.py')
    if not os.path.exists(portfolio_path):
        print(f"Error: {portfolio_path} not found")
        sys.exit(1)
    
    num_replacements = replace_decorators(portfolio_path)
    print(f"Successfully updated {portfolio_path} with {num_replacements} replacements")
    
    return num_replacements > 0

if __name__ == "__main__":
    if update_portfolio_file():
        print("Successfully updated portfolio.py to use unified access control")
    else:
        print("No changes were needed in portfolio.py")
