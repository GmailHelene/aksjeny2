#!/usr/bin/env python3
"""Test script to identify actual remaining issues"""

import sys
import os
import json
import requests
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_actual_issues():
    """Test actual issues that still exist"""
    
    print("=== TESTING ACTUAL REMAINING ISSUES ===")
    print(f"Test started at: {datetime.now()}")
    
    issues_found = []
    
    # Check if Flask app can start without errors
    print("\n🔍 Testing Flask App Import")
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app imports successfully")
        
        with app.app_context():
            # Test 1: Check for blueprint registration errors
            print("\n🔍 Testing Blueprint Registration")
            try:
                blueprints = list(app.blueprints.keys())
                print(f"✅ {len(blueprints)} blueprints registered: {blueprints}")
                
                if 'pro_tools' not in blueprints:
                    issues_found.append("❌ pro_tools blueprint NOT registered")
                else:
                    print("✅ pro_tools blueprint is registered")
                    
            except Exception as e:
                issues_found.append(f"❌ Blueprint registration error: {e}")
            
            # Test 2: Check for route errors
            print("\n🔍 Testing Route Registration")
            try:
                routes = [str(rule) for rule in app.url_map.iter_rules()]
                pro_routes = [r for r in routes if 'pro-tools' in r]
                print(f"✅ Pro-tools routes found: {pro_routes}")
                
                compare_routes = [r for r in routes if 'compare' in r]
                print(f"✅ Compare routes found: {compare_routes}")
                
            except Exception as e:
                issues_found.append(f"❌ Route registration error: {e}")
            
            # Test 3: Check database tables
            print("\n🔍 Testing Database Tables")
            try:
                from app.extensions import db
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"✅ Database tables: {tables}")
                
                required_tables = ['users', 'portfolios', 'portfolio_stocks', 'favorites']
                missing_tables = [t for t in required_tables if t not in tables]
                if missing_tables:
                    issues_found.append(f"❌ Missing database tables: {missing_tables}")
                else:
                    print("✅ All required tables exist")
                    
            except Exception as e:
                issues_found.append(f"❌ Database error: {e}")
                
            # Test 4: Check template files exist
            print("\n🔍 Testing Template Files")
            template_paths = [
                'stocks/details.html',
                'stocks/compare.html', 
                'pro/screener.html',
                'notifications/index.html',
                'portfolio/index.html',
                'portfolio/watchlist.html',
                'advanced_features/crypto_dashboard.html'
            ]
            
            for template in template_paths:
                try:
                    app.jinja_env.get_template(template)
                    print(f"✅ Template exists: {template}")
                except Exception as e:
                    issues_found.append(f"❌ Missing template: {template} - {e}")
            
            # Test 5: Test actual route responses (simulation)
            print("\n🔍 Testing Route Response Simulation")
            with app.test_client() as client:
                test_routes = [
                    ('/', 'Homepage'),
                    ('/stocks', 'Stocks list'),
                    ('/stocks/compare', 'Stock comparison'),
                ]
                
                for route, name in test_routes:
                    try:
                        response = client.get(route)
                        if response.status_code == 500:
                            issues_found.append(f"❌ 500 error on {route} ({name})")
                        elif response.status_code in [200, 302, 404]:
                            print(f"✅ {route} responds with {response.status_code}")
                        else:
                            issues_found.append(f"⚠️ Unexpected status {response.status_code} on {route}")
                    except Exception as e:
                        issues_found.append(f"❌ Route test error {route}: {e}")
                        
    except Exception as e:
        issues_found.append(f"❌ Critical Flask app error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
    
    # Summary
    print(f"\n=== ACTUAL ISSUES FOUND ===")
    if issues_found:
        print(f"❌ Found {len(issues_found)} actual issues:")
        for i, issue in enumerate(issues_found, 1):
            print(f"  {i}. {issue}")
    else:
        print("✅ No major issues found in testing")
    
    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'issues_found': issues_found,
        'test_status': 'ISSUES_FOUND' if issues_found else 'PASSING'
    }
    
    with open('actual_issues_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to actual_issues_test_results.json")
    
    return issues_found

if __name__ == "__main__":
    issues = test_actual_issues()
    if issues:
        print(f"\n❌ FOUND {len(issues)} ACTUAL ISSUES THAT NEED FIXING!")
    else:
        print(f"\n✅ No major issues found in basic testing")
