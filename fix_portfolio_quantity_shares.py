#!/usr/bin/env python3
"""
Fix Step 14: Portfolio Functionality - Fix column reference inconsistencies
Replace all instances of stock.quantity with stock.shares to match the database model
"""
import os
import re

def fix_portfolio_routes():
    """Fix the portfolio.py file to use 'shares' instead of 'quantity'"""
    portfolio_file = "app/routes/portfolio.py"
    
    if not os.path.exists(portfolio_file):
        print(f"❌ File not found: {portfolio_file}")
        return False
    
    print(f"🔧 Fixing {portfolio_file}...")
    
    # Read the file
    with open(portfolio_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count replacements
    replacements = [
        (r'stock\.quantity', 'stock.shares'),
        (r"'quantity': stock\.shares", "'quantity': stock.shares"),  # Keep display as 'quantity'
        (r'"quantity": stock\.shares', '"quantity": stock.shares'),  # Keep display as 'quantity'
    ]
    
    total_replacements = 0
    for pattern, replacement in replacements:
        matches = re.findall(pattern, content)
        count = len(matches)
        content = re.sub(pattern, replacement, content)
        total_replacements += count
        if count > 0:
            print(f"  ✅ Replaced {count} instances of '{pattern}' with '{replacement}'")
    
    if total_replacements == 0:
        print("  ℹ️ No replacements needed")
        return True
    
    # Write the file back
    with open(portfolio_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Fixed {total_replacements} total replacements in {portfolio_file}")
    return True

def main():
    print("🚀 Starting Portfolio Functionality Fix (Step 14)")
    print("=" * 60)
    
    success = fix_portfolio_routes()
    
    print("=" * 60)
    if success:
        print("✅ Step 14 - Portfolio Functionality: FIXED!")
        print("🔧 Fixed stock.quantity → stock.shares inconsistencies")
        print("📊 Portfolio calculations should now work correctly")
    else:
        print("❌ Step 14 - Portfolio Functionality: FAILED!")
    
    return success

if __name__ == "__main__":
    main()
