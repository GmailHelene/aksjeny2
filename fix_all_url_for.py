#!/usr/bin/env python3
"""
Script to fix all url_for() calls in templates that cause BuildError in production
"""
import os
import re
import glob

# URL mappings for blueprint endpoints
URL_MAPPINGS = {
    # Analysis blueprint
    "url_for('analysis.index')": '"/analysis"',
    "url_for('analysis.market_overview')": '"/analysis/market-overview"',
    "url_for('analysis.technical')": '"/analysis/technical"',
    "url_for('analysis.fundamental')": '"/analysis/fundamental"',
    "url_for('analysis.warren_buffett')": '"/analysis/warren-buffett"',
    "url_for('analysis.benjamin_graham')": '"/analysis/benjamin-graham"',
    "url_for('analysis.ai')": '"/analysis/ai"',
    "url_for('analysis.screener')": '"/analysis/screener"',
    "url_for('analysis.sentiment')": '"/analysis/sentiment"',
    "url_for('analysis.short_analysis')": '"/analysis/short"',
    "url_for('analysis.prediction')": '"/analysis/prediction"',
    "url_for('analysis.recommendation')": '"/analysis/recommendation"',
    "url_for('analysis.oslo_overview')": '"/analysis/oslo-overview"',
    "url_for('analysis.global_overview')": '"/analysis/global-overview"', 
    "url_for('analysis.currency_overview')": '"/analysis/currency-overview"',
    "url_for('analysis.backtest')": '"/analysis/backtest"',
    "url_for('analysis.strategy_builder')": '"/analysis/strategy-builder"',
    "url_for('analysis.tradingview')": '"/analysis/tradingview"',
    "url_for('analysis.ai_predictions')": '"/analysis/ai-predictions"',
    
    # Portfolio blueprint
    "url_for('portfolio.index')": '"/portfolio"',
    "url_for('portfolio.stock_tips')": '"/portfolio/stock-tips"',
    
    # Market Intel blueprint
    "url_for('market_intel.insider_trading')": '"/market-intel/insider-trading"',
}

# Dynamic URL patterns (with parameters)
DYNAMIC_PATTERNS = [
    (r"url_for\('analysis\.technical',\s*symbol=([^)]+)\)", r'f"/analysis/technical?symbol={{\1}}"'),
    (r"url_for\('analysis\.warren_buffett',\s*ticker=([^)]+)\)", r'f"/analysis/warren-buffett?ticker={{\1}}"'),
    (r"url_for\('analysis\.benjamin_graham',\s*ticker=([^)]+)\)", r'f"/analysis/benjamin-graham?ticker={{\1}}"'),
    (r"url_for\('analysis\.ai',\s*ticker=([^)]+)\)", r'f"/analysis/ai?ticker={{\1}}"'),
    (r"url_for\('analysis\.fundamental',\s*ticker=([^)]+)\)", r'f"/analysis/fundamental?ticker={{\1}}"'),
    (r"url_for\('analysis\.recommendation',\s*ticker=([^)]+)\)", r'f"/analysis/recommendation?ticker={{\1}}"'),
    
    # Complex conditional url_for
    (r"url_for\('analysis\.recommendation',\s*ticker=ticker\)\s*if\s*ticker\s*else\s*url_for\('analysis\.recommendation'\)", 
     'f"/analysis/recommendation?ticker={ticker}" if ticker else "/analysis/recommendation"'),
]

def fix_file(filepath):
    """Fix a single template file"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply static URL mappings
        for old_pattern, new_url in URL_MAPPINGS.items():
            if old_pattern in content:
                content = content.replace(old_pattern, new_url)
                print(f"  Replaced: {old_pattern} -> {new_url}")
        
        # Apply dynamic patterns
        for pattern, replacement in DYNAMIC_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                print(f"  Applied dynamic pattern: {pattern}")
        
        # Special handling for form actions
        content = re.sub(
            r'action="\{\{\s*url_for\(\'analysis\.technical\'\)\s*\}\}"',
            'action="/analysis/technical"',
            content
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Updated {filepath}")
            return True
        else:
            print(f"  ⏭️  No changes needed in {filepath}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all template files"""
    print("🔧 Starting URL fix process for all templates...")
    
    # Find all HTML template files
    template_paths = []
    for root, dirs, files in os.walk('app/templates'):
        for file in files:
            if file.endswith('.html'):
                template_paths.append(os.path.join(root, file))
    
    print(f"Found {len(template_paths)} template files")
    
    fixed_count = 0
    for filepath in template_paths:
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\n✅ Fix complete! Updated {fixed_count} files out of {len(template_paths)} total.")
    print("🚀 All url_for() calls should now use direct URLs for production compatibility.")

if __name__ == "__main__":
    main()
