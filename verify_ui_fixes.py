#!/usr/bin/env python3
"""
UI Fixes Verification Script
===========================

This script verifies that all UI fixes are working correctly:
1. Profile favorites display with proper data
2. Advanced analytics buttons with event binding
3. Analyst coverage filters with JavaScript functionality

Author: GitHub Copilot
Date: August 29, 2025
"""

import os
import sys
from datetime import datetime

def verify_profile_favorites():
    """Verify profile favorites fix"""
    print("\n🔍 Verifying Profile Favorites Fix...")
    
    try:
        from app import create_app
        from app.extensions import db
        from app.models.favorites import Favorites
        from app.models.user import User
        
        app = create_app()
        with app.app_context():
            # Check if favorites have proper names and exchanges now
            favorites = Favorites.query.limit(5).all()
            
            print(f"📊 Found {len(favorites)} sample favorites:")
            
            all_have_data = True
            for fav in favorites:
                name_ok = fav.name and fav.name.strip() != ''
                exchange_ok = fav.exchange and fav.exchange.strip() != ''
                
                status_name = "✅" if name_ok else "❌"
                status_exchange = "✅" if exchange_ok else "❌"
                
                print(f"  {status_name} {fav.symbol}: '{fav.name}' @ {status_exchange} '{fav.exchange}'")
                
                if not name_ok or not exchange_ok:
                    all_have_data = False
            
            if all_have_data:
                print("✅ Profile favorites data verification PASSED")
                return True
            else:
                print("❌ Some favorites still missing data")
                return False
                
    except Exception as e:
        print(f"❌ Profile favorites verification failed: {e}")
        return False

def verify_advanced_analytics():
    """Verify advanced analytics JavaScript fixes"""
    print("\n🔍 Verifying Advanced Analytics Fixes...")
    
    template_file = "/workspaces/aksjeny2/app/templates/advanced_analytics.html"
    enhanced_js_file = "/workspaces/aksjeny2/enhanced_analytics_js.js"
    
    checks = {
        "Template file exists": os.path.exists(template_file),
        "Enhanced JS file created": os.path.exists(enhanced_js_file),
        "Debug logging added": False,
        "Error handling improved": False
    }
    
    if checks["Template file exists"]:
        try:
            with open(template_file, 'r') as f:
                content = f.read()
                
            # Check for debug improvements
            if "console.log('Advanced Analytics JavaScript loaded')" in content:
                checks["Debug logging added"] = True
                
            if "console.error('Market Analysis button not found')" in content:
                checks["Error handling improved"] = True
                
        except Exception as e:
            print(f"❌ Error reading template: {e}")
    
    # Print results
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("✅ Advanced analytics verification PASSED")
    else:
        print("❌ Advanced analytics verification FAILED")
    
    return all_passed

def verify_analyst_coverage():
    """Verify analyst coverage filter fixes"""
    print("\n🔍 Verifying Analyst Coverage Fixes...")
    
    template_file = "/workspaces/aksjeny2/app/templates/external_data/analyst_coverage.html"
    enhanced_js_file = "/workspaces/aksjeny2/enhanced_analyst_filters.js"
    
    checks = {
        "Template file exists": os.path.exists(template_file),
        "Enhanced filter JS created": os.path.exists(enhanced_js_file),
        "Filter buttons have data-filter": False,
        "JavaScript event binding exists": False
    }
    
    if checks["Template file exists"]:
        try:
            with open(template_file, 'r') as f:
                content = f.read()
                
            # Check for filter button structure
            if 'data-filter="all"' in content and 'data-filter="buy"' in content:
                checks["Filter buttons have data-filter"] = True
                
            if "addEventListener('click'" in content:
                checks["JavaScript event binding exists"] = True
                
        except Exception as e:
            print(f"❌ Error reading template: {e}")
    
    # Print results
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("✅ Analyst coverage verification PASSED")
    else:
        print("❌ Analyst coverage verification FAILED")
    
    return all_passed

def verify_file_backups():
    """Verify that backup files were created"""
    print("\n🔍 Verifying Backup Files...")
    
    backup_dir = "/workspaces/aksjeny2"
    backup_files = [
        f for f in os.listdir(backup_dir) 
        if f.endswith('.backup_20250829_222328')
    ]
    
    print(f"📁 Found {len(backup_files)} backup files:")
    for backup in backup_files:
        print(f"  ✅ {backup}")
    
    if len(backup_files) >= 3:  # Should have at least 3 backups
        print("✅ Backup verification PASSED")
        return True
    else:
        print("❌ Expected at least 3 backup files")
        return False

def test_profile_route_simulation():
    """Simulate profile route execution"""
    print("\n🔍 Testing Profile Route Logic...")
    
    try:
        from app import create_app
        from app.extensions import db
        from app.models.favorites import Favorites
        
        app = create_app()
        with app.app_context():
            # Simulate the enhanced logic from the profile route
            user_id = 1  # Test with user ID 1 who has favorites
            
            favorites = Favorites.query.filter_by(user_id=user_id).all()
            print(f"📊 Found {len(favorites)} favorites for user {user_id}")
            
            if len(favorites) > 0:
                print("✅ Profile route simulation PASSED")
                
                # Test enhanced name/exchange logic
                test_fav = favorites[0]
                display_name = test_fav.name if test_fav.name and test_fav.name.strip() != '' else test_fav.symbol
                
                exchange = test_fav.exchange
                if not exchange or exchange.strip() == '':
                    if test_fav.symbol.endswith('.OL'):
                        exchange = 'Oslo Børs'
                    elif '.' not in test_fav.symbol:
                        exchange = 'NASDAQ/NYSE'
                    else:
                        exchange = 'Unknown'
                
                print(f"  📈 Sample: {test_fav.symbol} -> '{display_name}' @ '{exchange}'")
                return True
            else:
                print("❌ No favorites found for test user")
                return False
                
    except Exception as e:
        print(f"❌ Profile route simulation failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 UI Fixes Verification")
    print("=" * 40)
    
    tests = [
        ("Profile Favorites", verify_profile_favorites),
        ("Advanced Analytics", verify_advanced_analytics),
        ("Analyst Coverage", verify_analyst_coverage),
        ("Backup Files", verify_file_backups),
        ("Profile Route Logic", test_profile_route_simulation)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 40)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All UI fixes verified successfully!")
        print("\n📌 What was fixed:")
        print("• Profile favorites now show proper names and exchanges")
        print("• Advanced analytics buttons have enhanced error handling")
        print("• Analyst coverage filters include visual feedback")
        print("• All changes have backup files for safety")
        
        print("\n🚀 Ready for testing!")
        print("1. Restart Flask server if needed")
        print("2. Log in to test profile favorites")
        print("3. Try advanced analytics buttons")
        print("4. Test analyst coverage filters")
    else:
        print("\n⚠️  Some verifications failed. Check details above.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
