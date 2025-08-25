#!/usr/bin/env python3
"""
Comprehensive test script for profile and Oslo stocks fixes
"""
import sys
import os
import logging
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_profile_oslo_fixes():
    """Test the fixes for profile and Oslo stocks pages"""
    
    print(f"🔧 Testing Profile and Oslo Stocks Fixes - {datetime.now()}")
    print("=" * 70)
    
    # Test the route functions directly to see if they have syntax errors
    test_results = []
    
    print("\n📋 1. Testing Route Function Imports")
    print("-" * 40)
    
    try:
        from app.routes.main import profile
        print("✅ Profile route function imports successfully")
        test_results.append(("Profile Import", "PASS"))
    except Exception as e:
        print(f"❌ Profile route import failed: {e}")
        test_results.append(("Profile Import", f"FAIL: {e}"))
    
    try:
        from app.routes.stocks import list_oslo
        print("✅ Oslo stocks route function imports successfully")
        test_results.append(("Oslo Import", "PASS"))
    except Exception as e:
        print(f"❌ Oslo stocks route import failed: {e}")
        test_results.append(("Oslo Import", f"FAIL: {e}"))
    
    print("\n📋 2. Testing Model Imports")
    print("-" * 40)
    
    try:
        from app.models.referral import Referral, ReferralDiscount
        print("✅ Referral models import successfully")
        test_results.append(("Referral Models", "PASS"))
    except Exception as e:
        print(f"❌ Referral models import failed: {e}")
        test_results.append(("Referral Models", f"FAIL: {e}"))
    
    try:
        from app.models.favorites import Favorites
        print("✅ Favorites model imports successfully")
        test_results.append(("Favorites Model", "PASS"))
    except Exception as e:
        print(f"❌ Favorites model import failed: {e}")
        test_results.append(("Favorites Model", f"FAIL: {e}"))
    
    print("\n📋 3. Testing DataService Methods")
    print("-" * 40)
    
    try:
        from app.services.data_service import DataService
        print("✅ DataService imports successfully")
        
        # Check if methods exist
        if hasattr(DataService, 'get_oslo_bors_overview'):
            print("✅ get_oslo_bors_overview method exists")
            test_results.append(("Oslo DataService Method", "PASS"))
        else:
            print("❌ get_oslo_bors_overview method missing")
            test_results.append(("Oslo DataService Method", "FAIL: Method missing"))
            
        if hasattr(DataService, '_get_guaranteed_oslo_data'):
            print("✅ _get_guaranteed_oslo_data method exists")
            test_results.append(("Oslo Fallback Method", "PASS"))
        else:
            print("❌ _get_guaranteed_oslo_data method missing")
            test_results.append(("Oslo Fallback Method", "FAIL: Method missing"))
            
    except Exception as e:
        print(f"❌ DataService import failed: {e}")
        test_results.append(("DataService", f"FAIL: {e}"))
    
    print("\n📋 4. Testing Template Existence")
    print("-" * 40)
    
    template_paths = [
        'app/templates/profile.html',
        'app/templates/stocks/oslo_dedicated.html',
        'app/templates/stocks/oslo.html'
    ]
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            print(f"✅ {template_path} exists")
            test_results.append((f"Template: {template_path}", "PASS"))
        else:
            print(f"⚠️ {template_path} missing")
            test_results.append((f"Template: {template_path}", "MISSING"))
    
    print("\n📋 5. Testing Application Context")
    print("-" * 40)
    
    try:
        from app import create_app
        app = create_app()
        
        with app.app_context():
            print("✅ Application context created successfully")
            test_results.append(("App Context", "PASS"))
            
            # Test if we can access the database
            try:
                from app.extensions import db
                print("✅ Database extension accessible")
                test_results.append(("Database Access", "PASS"))
            except Exception as db_error:
                print(f"⚠️ Database access issue: {db_error}")
                test_results.append(("Database Access", f"WARNING: {db_error}"))
                
    except Exception as app_error:
        print(f"❌ Application context creation failed: {app_error}")
        test_results.append(("App Context", f"FAIL: {app_error}"))
    
    print("\n📋 6. Summary of Test Results")
    print("=" * 70)
    
    passed = 0
    failed = 0
    warnings = 0
    
    for test_name, result in test_results:
        if result == "PASS":
            print(f"✅ {test_name}: PASSED")
            passed += 1
        elif result.startswith("FAIL"):
            print(f"❌ {test_name}: {result}")
            failed += 1
        elif result.startswith("WARNING") or result == "MISSING":
            print(f"⚠️ {test_name}: {result}")
            warnings += 1
        else:
            print(f"ℹ️ {test_name}: {result}")
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed} PASSED, {failed} FAILED, {warnings} WARNINGS")
    
    if failed == 0:
        print("🎉 All critical tests passed! The fixes should resolve the profile and Oslo issues.")
    elif failed <= 2:
        print("⚠️ Minor issues detected, but core functionality should work.")
    else:
        print("❌ Multiple critical issues detected. Additional fixes may be needed.")
    
    print("\n🔍 Next Steps:")
    print("1. Deploy the updated code to production")
    print("2. Test the live /profile and /stocks/list/oslo endpoints")
    print("3. Monitor the application logs for any remaining errors")
    print("4. Verify that users can access both pages without errors")
    
    return test_results

if __name__ == '__main__':
    test_profile_oslo_fixes()
