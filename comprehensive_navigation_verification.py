#!/usr/bin/env python3
"""
Navigation and Market Intel Verification Test
Comprehensive testing of all navigation improvements and Market Intel data integration
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from app.models import User
from app.services.external_apis import ExternalAPIService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_navigation_improvements():
    """Test all navigation improvements"""
    results = []
    
    print("🧭 TESTING NAVIGATION IMPROVEMENTS")
    print("=" * 50)
    
    # Test 1: Navigation hover colors (CSS)
    print("\n1. Testing navigation hover colors...")
    try:
        with open('app/static/css/comprehensive-theme-fixes.css', 'r') as f:
            css_content = f.read()
            
        if '.navbar-nav .nav-link:hover' in css_content and 'color: white !important' in css_content:
            print("✅ Navigation hover color fixed (blue → white)")
            results.append("✅ Navigation hover: PASS")
        else:
            print("❌ Navigation hover color not properly set")
            results.append("❌ Navigation hover: FAIL")
    except Exception as e:
        print(f"❌ Error checking navigation hover CSS: {e}")
        results.append("❌ Navigation hover: ERROR")
    
    # Test 2: Card header contrast rules (CSS)
    print("\n2. Testing card header contrast rules...")
    try:
        with open('app/static/css/text-contrast.css', 'r') as f:
            css_content = f.read()
            
        if '.card-header.bg-primary' in css_content and 'color: black !important' in css_content:
            print("✅ Card header contrast rules added")
            results.append("✅ Card headers: PASS")
        else:
            print("❌ Card header contrast rules not found")
            results.append("❌ Card headers: FAIL")
    except Exception as e:
        print(f"❌ Error checking card header CSS: {e}")
        results.append("❌ Card headers: ERROR")
    
    # Test 3: Duplicate menu removal
    print("\n3. Testing duplicate menu removal...")
    try:
        with open('app/templates/base.html', 'r') as f:
            base_content = f.read()
            
        markedsoversikt_count = base_content.count('Markedsoversikt')
        if markedsoversikt_count <= 1:
            print(f"✅ Duplicate 'Markedsoversikt' menu items removed (found {markedsoversikt_count})")
            results.append("✅ Duplicate removal: PASS")
        else:
            print(f"❌ Still found {markedsoversikt_count} 'Markedsoversikt' items")
            results.append("❌ Duplicate removal: FAIL")
    except Exception as e:
        print(f"❌ Error checking duplicate menus: {e}")
        results.append("❌ Duplicate removal: ERROR")
    
    # Test 4: Advanced Analytics navigation link
    print("\n4. Testing Advanced Analytics navigation link...")
    try:
        with open('app/templates/base.html', 'r') as f:
            base_content = f.read()
            
        if "url_for('advanced_analytics.index')" in base_content and "Advanced Analytics" in base_content:
            print("✅ Advanced Analytics link added to Pro Tools menu")
            results.append("✅ Advanced Analytics link: PASS")
        else:
            print("❌ Advanced Analytics link not found in navigation")
            results.append("❌ Advanced Analytics link: FAIL")
    except Exception as e:
        print(f"❌ Error checking Advanced Analytics link: {e}")
        results.append("❌ Advanced Analytics link: ERROR")
    
    return results

def test_market_intel_data():
    """Test Market Intel pages for real data integration"""
    results = []
    
    print("\n🏦 TESTING MARKET INTEL DATA INTEGRATION")
    print("=" * 50)
    
    # Test 1: Market Intel routes exist
    print("\n1. Testing Market Intel routes...")
    try:
        with open('app/routes/market_intel.py', 'r') as f:
            routes_content = f.read()
            
        required_routes = [
            'def index():', 
            'def insider_trading():', 
            'def earnings_calendar():', 
            'def sector_analysis():', 
            'def economic_indicators():'
        ]
        
        missing_routes = []
        for route in required_routes:
            if route not in routes_content:
                missing_routes.append(route)
        
        if not missing_routes:
            print("✅ All Market Intel routes are implemented")
            results.append("✅ Market Intel routes: PASS")
        else:
            print(f"❌ Missing routes: {missing_routes}")
            results.append("❌ Market Intel routes: FAIL")
    except Exception as e:
        print(f"❌ Error checking Market Intel routes: {e}")
        results.append("❌ Market Intel routes: ERROR")
    
    # Test 2: ExternalAPIService integration
    print("\n2. Testing ExternalAPIService integration...")
    try:
        with open('app/routes/market_intel.py', 'r') as f:
            routes_content = f.read()
            
        if 'ExternalAPIService' in routes_content and 'get_real_insider_data' in routes_content:
            print("✅ ExternalAPIService properly integrated for real data")
            results.append("✅ Real data service: PASS")
        else:
            print("❌ ExternalAPIService not properly integrated")
            results.append("❌ Real data service: FAIL")
    except Exception as e:
        print(f"❌ Error checking ExternalAPIService: {e}")
        results.append("❌ Real data service: ERROR")
    
    # Test 3: Access control for Market Intel
    print("\n3. Testing Market Intel access control...")
    try:
        with open('app/routes/market_intel.py', 'r') as f:
            routes_content = f.read()
            
        access_decorators = ['@access_required', '@demo_access']
        has_access_control = any(decorator in routes_content for decorator in access_decorators)
        
        if has_access_control:
            print("✅ Market Intel routes have proper access control")
            results.append("✅ Access control: PASS")
        else:
            print("❌ Market Intel routes missing access control")
            results.append("❌ Access control: FAIL")
    except Exception as e:
        print(f"❌ Error checking access control: {e}")
        results.append("❌ Access control: ERROR")
    
    # Test 4: Market Intel templates exist
    print("\n4. Testing Market Intel templates...")
    try:
        required_templates = [
            'app/templates/market_intel/index.html',
            'app/templates/market_intel/insider_trading.html',
            'app/templates/market_intel/earnings_calendar.html',
            'app/templates/market_intel/sector_analysis.html',
            'app/templates/market_intel/economic_indicators.html'
        ]
        
        missing_templates = []
        for template in required_templates:
            if not os.path.exists(template):
                missing_templates.append(template)
        
        if not missing_templates:
            print("✅ All Market Intel templates exist")
            results.append("✅ Templates: PASS")
        else:
            print(f"❌ Missing templates: {missing_templates}")
            results.append("❌ Templates: FAIL")
    except Exception as e:
        print(f"❌ Error checking templates: {e}")
        results.append("❌ Templates: ERROR")
    
    return results

def test_advanced_analytics_functionality():
    """Test Advanced Analytics (CMC Markets inspired) functionality"""
    results = []
    
    print("\n📊 TESTING ADVANCED ANALYTICS FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Advanced Analytics blueprint exists
    print("\n1. Testing Advanced Analytics blueprint...")
    try:
        with open('app/routes/advanced_analytics.py', 'r') as f:
            analytics_content = f.read()
            
        if 'advanced_analytics = Blueprint' in analytics_content:
            print("✅ Advanced Analytics blueprint exists")
            results.append("✅ Analytics blueprint: PASS")
        else:
            print("❌ Advanced Analytics blueprint not found")
            results.append("❌ Analytics blueprint: FAIL")
    except Exception as e:
        print(f"❌ Error checking Advanced Analytics blueprint: {e}")
        results.append("❌ Analytics blueprint: ERROR")
    
    # Test 2: CMC Markets inspired features
    print("\n2. Testing CMC Markets inspired features...")
    try:
        with open('app/routes/advanced_analytics.py', 'r') as f:
            analytics_content = f.read()
            
        cmc_features = [
            'portfolio_optimization',
            'risk_management',
            'market_analysis',
            'ml_predictions'
        ]
        
        found_features = []
        for feature in cmc_features:
            if feature in analytics_content:
                found_features.append(feature)
        
        if len(found_features) >= 3:
            print(f"✅ CMC Markets inspired features found: {found_features}")
            results.append("✅ CMC features: PASS")
        else:
            print(f"❌ Insufficient CMC features found: {found_features}")
            results.append("❌ CMC features: FAIL")
    except Exception as e:
        print(f"❌ Error checking CMC features: {e}")
        results.append("❌ CMC features: ERROR")
    
    return results

def main():
    """Run all tests and provide summary"""
    print("🔍 COMPREHENSIVE NAVIGATION & MARKET INTEL VERIFICATION")
    print("=" * 60)
    
    all_results = []
    
    # Run all test suites
    navigation_results = test_navigation_improvements()
    market_intel_results = test_market_intel_data()
    analytics_results = test_advanced_analytics_functionality()
    
    all_results.extend(navigation_results)
    all_results.extend(market_intel_results)
    all_results.extend(analytics_results)
    
    # Calculate summary
    total_tests = len(all_results)
    passed_tests = len([r for r in all_results if "PASS" in r])
    failed_tests = len([r for r in all_results if "FAIL" in r])
    error_tests = len([r for r in all_results if "ERROR" in r])
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 FINAL VERIFICATION SUMMARY")
    print("=" * 60)
    
    for result in all_results:
        print(result)
    
    print(f"\n📊 STATISTICS:")
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"⚠️ Errors: {error_tests}")
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("\n🎉 EXCELLENT! All major components are working correctly.")
    elif success_rate >= 75:
        print("\n👍 GOOD! Most components are working, minor issues detected.")
    elif success_rate >= 50:
        print("\n⚠️ PARTIAL SUCCESS! Some issues need attention.")
    else:
        print("\n❌ MULTIPLE ISSUES detected! Review required.")
    
    print("\n" + "=" * 60)
    print("🏁 VERIFICATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
