#!/usr/bin/env python3
"""
EMERGENCY MASS FIX - Replace ALL url_for() calls with direct URLs
"""

import os
import re

# Mapping of common url_for patterns to direct URLs
URL_MAPPINGS = {
    "url_for('main.index')": "'/'",
    "url_for('main.login')": "'/login'",
    "url_for('main.logout')": "'/logout'",
    "url_for('main.register')": "'/register'",
    "url_for('main.contact')": "'/contact'",
    "url_for('main.demo')": "'/demo'",
    "url_for('main.about')": "'/about'",
    "url_for('pricing.pricing_page')": "'/pricing'",
    "url_for('pricing.index')": "'/pricing'",
    "url_for('portfolio.overview')": "'/portfolio/overview'",
    "url_for('portfolio.watchlist')": "'/portfolio/watchlist'",
    "url_for('portfolio.stock_tips')": "'/portfolio/stock-tips'",
    "url_for('portfolio.index')": "'/portfolio'",
    "url_for('analysis.sentiment')": "'/analysis/sentiment'",
    "url_for('analysis.technical')": "'/analysis/technical'",
    "url_for('analysis.recommendation')": "'/analysis/recommendation'",
    "url_for('analysis.currency_overview')": "'/analysis/currency_overview'",
    "url_for('analysis.market_overview')": "'/analysis/market-overview'",
    "url_for('analysis.ai')": "'/analysis/ai'",
    "url_for('stocks.details')": "'/stocks/details'",
    "url_for('stocks.search')": "'/stocks/search'",
    "url_for('stocks.list_oslo')": "'/stocks/oslo'",
    "url_for('market_intel.insider_trading')": "'/market-intel/insider-trading'",
    "url_for('dashboard.financial_dashboard')": "'/dashboard/financial'",
}

def fix_url_for_in_file(filepath):
    """Fix all url_for() calls in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # Apply direct mappings first
        for old_pattern, new_pattern in URL_MAPPINGS.items():
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                changes_made += 1
                print(f"  ✅ {old_pattern} -> {new_pattern}")
        
        # Handle parametrized url_for calls with regex
        patterns = [
            # url_for('blueprint.route', param=value)
            (r"url_for\('([^']+)',\s*([^)]+)\)", r"f'/{replace_route(\1)}?{\2}'"),
            # url_for('blueprint.route')
            (r"url_for\('([^']+)'\)", r"'/{replace_route(\1)}'"),
        ]
        
        for pattern, replacement in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    route = match[0]
                    # Convert route names to paths
                    route_path = route.replace('.', '/').replace('_', '-')
                    if len(match) > 1:
                        params = match[1]
                        old_full = f"url_for('{route}', {params})"
                        new_full = f"f'/{route_path}?{params}'"
                    else:
                        old_full = f"url_for('{route}')"
                        new_full = f"'/{route_path}'"
                    
                    if old_full in content:
                        content = content.replace(old_full, new_full)
                        changes_made += 1
                        print(f"  ✅ {old_full} -> {new_full}")
        
        # Save file if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📁 {filepath}: {changes_made} url_for() calls fixed")
            return changes_made
        else:
            return 0
            
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return 0

def main():
    print("🚨 EMERGENCY MASS url_for() FIX")
    print("=" * 50)
    print("Fixing ALL url_for() calls in authenticated routes...")
    print()
    
    # Files to fix (authenticated route files that are causing crashes)
    critical_files = [
        'app/routes/main.py',
        'app/routes/analysis.py', 
        'app/routes/portfolio.py',
        'app/routes/stocks.py',
        'app/routes/dashboard.py',
        'app/routes/market_intel.py',
        'app/routes/api.py',
        'app/utils/access_control.py'
    ]
    
    total_fixes = 0
    for file_path in critical_files:
        if os.path.exists(file_path):
            print(f"\n🔧 Fixing {file_path}...")
            fixes = fix_url_for_in_file(file_path)
            total_fixes += fixes
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n{'='*50}")
    print(f"🎯 TOTAL FIXES: {total_fixes} url_for() calls replaced")
    print("✅ All authenticated routes should now work!")
    print("🚀 Ready for deployment to Railway")

if __name__ == "__main__":
    main()
