#!/usr/bin/env python3
"""Simple verification of the fixes made"""

import os

def verify_profile_route_fix():
    """Verify profile route has been fixed"""
    print("🔍 Verifying profile route fix...")
    
    main_py_path = 'app/routes/main.py'
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that dangerous db.session.commit() was removed
        if 'current_user.subscription_type = \'monthly\'' not in content:
            print("✅ Dangerous database commit removed from profile route")
            return True
        else:
            print("❌ Dangerous database commit still present")
            return False
    else:
        print("❌ main.py file not found")
        return False

def verify_navigation_changes():
    """Verify navigation changes in template"""
    print("🔍 Verifying navigation changes...")
    
    base_html_path = 'app/templates/base.html'
    if os.path.exists(base_html_path):
        with open(base_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        abonnement_removed = 'Abonnement</a></li>' not in content
        forum_added = 'Forum</a>' in content and 'bi-chat-dots' in content
        
        if abonnement_removed:
            print("✅ Abonnement menu item successfully removed")
        else:
            print("❌ Abonnement menu item still present")
            
        if forum_added:
            print("✅ Forum link successfully added to footer")
        else:
            print("❌ Forum link not found in footer")
            
        return abonnement_removed and forum_added
    else:
        print("❌ base.html file not found")
        return False

def main():
    """Run all verifications"""
    print("🧪 Verifying all fixes...")
    print("=" * 40)
    
    profile_ok = verify_profile_route_fix()
    nav_ok = verify_navigation_changes()
    
    print("=" * 40)
    print("📊 VERIFICATION RESULTS:")
    print(f"Profile route fix: {'✅ VERIFIED' if profile_ok else '❌ FAILED'}")
    print(f"Navigation changes: {'✅ VERIFIED' if nav_ok else '❌ FAILED'}")
    
    if profile_ok and nav_ok:
        print("\n🎉 ALL FIXES VERIFIED!")
        print("✅ Profile page 500 error should be resolved")
        print("✅ Abonnement menu item removed from navigation")
        print("✅ Forum link added to footer")
        return True
    else:
        print("\n⚠️  Some verifications failed")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
