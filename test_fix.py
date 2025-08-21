#!/usr/bin/env python3
"""
Quick test for BuildError fix
"""

import sys
import os
sys.path.insert(0, '.')

def test_builderror_fix():
    """Test that BuildError is fixed"""
    try:
        print("=== TESTING BUILDERROR FIX ===")
        
        # Test 1: Import Flask app
        try:
            from app import create_app
            app = create_app('development')
            print("✅ 1. App created successfully")
        except Exception as e:
            print(f"❌ 1. App creation failed: {e}")
            return False
        
        # Test 2: Test URL generation within app context
        with app.app_context():
            try:
                from flask import url_for
                crypto_url = url_for('advanced_features.crypto_dashboard')
                print(f"✅ 2. URL generated successfully: {crypto_url}")
            except Exception as e:
                print(f"❌ 2. URL generation failed: {e}")
                return False
            
            # Test 3: Check blueprint registration
            try:
                rules = [rule for rule in app.url_map.iter_rules() if 'advanced_features' in rule.endpoint]
                print(f"✅ 3. Found {len(rules)} advanced_features routes:")
                for rule in rules:
                    print(f"   - {rule.endpoint}: {rule.rule}")
            except Exception as e:
                print(f"❌ 3. Blueprint check failed: {e}")
                return False
        
        print("\n🎉 BUILDERROR FIX SUCCESSFUL!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_builderror_fix()
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
