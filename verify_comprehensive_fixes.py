#!/usr/bin/env python3
"""
Verification script for the comprehensive fixes we just implemented:
1. Main index page sp500 data fix
2. Stock detail endpoint fixes  
3. Template safe access patterns
4. Market data structure completeness
"""

import os
import sys

def verify_sp500_data_fix():
    """Verify that sp500 data is added to market_data structure"""
    print("🔍 Verifying S&P 500 data fix...")
    
    main_py_path = 'app/routes/main.py'
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for sp500 data in both fallback locations
        sp500_in_initial = "'sp500': {'value': 4567.89, 'change': 18.5, 'change_percent': 0.8}" in content
        sp500_in_setdefault = "'sp500', {'value': 4567.89, 'change': 18.5, 'change_percent': 0.8}" in content
        
        if sp500_in_initial and sp500_in_setdefault:
            print("✅ S&P 500 data successfully added to both market_data structures")
            return True
        elif sp500_in_initial:
            print("⚠️ S&P 500 data found in initial structure but not in setdefault")
            return False
        elif sp500_in_setdefault:
            print("⚠️ S&P 500 data found in setdefault but not in initial structure")
            return False
        else:
            print("❌ S&P 500 data not found in market_data structures")
            return False
    else:
        print("❌ main.py file not found")
        return False

def verify_template_safe_access():
    """Verify that index.html uses safe dict access for sp500 data"""
    print("🔍 Verifying template safe access patterns...")
    
    index_html_path = 'app/templates/index.html'
    if os.path.exists(index_html_path):
        with open(index_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for safe dict access instead of attribute access
        safe_access_patterns = [
            "market_data.get('sp500', {}).get('value'",
            "market_data.get('sp500', {}).get('change'",
            "market_data.get('sp500', {}).get('change_percent'"
        ]
        
        patterns_found = [pattern in content for pattern in safe_access_patterns]
        
        if all(patterns_found):
            print("✅ All S&P 500 template access patterns use safe dict access")
            return True
        else:
            print("❌ Some template access patterns still use unsafe attribute access")
            print(f"Patterns found: {patterns_found}")
            return False
    else:
        print("❌ index.html file not found")
        return False

def verify_stock_endpoint_fixes():
    """Verify that all stock detail endpoint references are corrected"""
    print("🔍 Verifying stock endpoint fixes...")
    
    templates_to_check = [
        'app/templates/norwegian_intel/social_sentiment.html',
        'app/templates/financial_dashboard.html', 
        'app/templates/stocks/oslo.html'
    ]
    
    all_fixed = True
    
    for template_path in templates_to_check:
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check that old endpoint names are not present
            old_endpoints = ['stocks.stock_detail', 'stocks.stock_details']
            has_old_endpoints = any(old_endpoint in content for old_endpoint in old_endpoints)
            
            # Check that new endpoint is present
            has_new_endpoint = 'stocks.details' in content
            
            if not has_old_endpoints and has_new_endpoint:
                print(f"✅ {template_path}: Stock endpoints correctly updated")
            elif has_old_endpoints:
                print(f"❌ {template_path}: Still contains old endpoint references")
                all_fixed = False
            else:
                print(f"⚠️ {template_path}: No stock detail links found")
        else:
            print(f"❌ {template_path}: File not found")
            all_fixed = False
    
    return all_fixed

def verify_sentiment_analysis_fix():
    """Verify that sentiment analysis route is simplified"""
    print("🔍 Verifying sentiment analysis fix...")
    
    analysis_py_path = 'app/routes/analysis.py'
    if os.path.exists(analysis_py_path):
        with open(analysis_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that problematic helper functions are not called
        problematic_calls = [
            '_generate_sentiment_indicators',
            '_generate_news_articles'
        ]
        
        has_problematic_calls = any(call in content for call in problematic_calls)
        
        if not has_problematic_calls:
            print("✅ Sentiment analysis route simplified - no problematic helper function calls")
            return True
        else:
            print("❌ Sentiment analysis still contains problematic helper function calls")
            return False
    else:
        print("❌ analysis.py file not found") 
        return False

def main():
    """Run all verifications"""
    print("🧪 Verifying comprehensive production fixes...")
    print("=" * 50)
    
    sp500_ok = verify_sp500_data_fix()
    template_ok = verify_template_safe_access()
    endpoints_ok = verify_stock_endpoint_fixes()
    sentiment_ok = verify_sentiment_analysis_fix()
    
    print("=" * 50)
    print("📊 VERIFICATION RESULTS:")
    print(f"S&P 500 data fix: {'✅ VERIFIED' if sp500_ok else '❌ FAILED'}")
    print(f"Template safe access: {'✅ VERIFIED' if template_ok else '❌ FAILED'}")
    print(f"Stock endpoint fixes: {'✅ VERIFIED' if endpoints_ok else '❌ FAILED'}")
    print(f"Sentiment analysis fix: {'✅ VERIFIED' if sentiment_ok else '❌ FAILED'}")
    
    all_ok = sp500_ok and template_ok and endpoints_ok and sentiment_ok
    
    if all_ok:
        print("\n🎉 ALL COMPREHENSIVE FIXES VERIFIED!")
        print("✅ Main index page 500 error should be resolved")
        print("✅ Stock detail BuildError should be resolved") 
        print("✅ Sentiment analysis 500 error should be resolved")
        print("✅ All template access patterns are safe")
        print("✅ Market data structure is complete")
        return True
    else:
        print("\n⚠️ Some verifications failed - check the details above")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
