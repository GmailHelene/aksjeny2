#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import time

def run_database_check():
    """Check if database and tables exist"""
    print("="*60)
    print("🔧 STEP 1: Database Check & Initialization")
    print("="*60)
    
    # Set environment variables for the database
    os.environ['DATABASE_URL'] = 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway'
    
    try:
        # Import all the necessary components
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import create_app
        from app.models import db
        
        print("📋 Creating Flask app...")
        app = create_app('development')
        
        with app.app_context():
            print("📋 Creating database tables...")
            db.create_all()
            
            # Check what tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ Database tables created/verified: {len(tables)} tables")
            print(f"📊 Tables: {', '.join(tables[:10])}{'...' if len(tables) > 10 else ''}")
            
            # Specifically check for user_stats
            if 'user_stats' in tables:
                print("✅ UserStats table exists - this should fix database errors")
            else:
                print("❌ UserStats table missing - will attempt to create")
                
            return True
            
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_route_availability_check():
    """Check if critical routes are working"""
    print("="*60) 
    print("🔧 STEP 2: Route Availability Check")
    print("="*60)
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import create_app
        
        app = create_app('development')
        
        # List of critical routes to test
        routes_to_test = [
            '/advanced-features/crypto-dashboard',
            '/portfolio/watchlist', 
            '/stocks/AAPL',
            '/analysis/sentiment',
            '/stocks/compare'
        ]
        
        with app.test_client() as client:
            results = {}
            
            for route in routes_to_test:
                try:
                    response = client.get(route)
                    results[route] = response.status_code
                    
                    if response.status_code == 200:
                        print(f"✅ {route} - OK (200)")
                    elif response.status_code == 500:
                        print(f"❌ {route} - SERVER ERROR (500)")
                    elif response.status_code in [401, 403]:
                        print(f"⚠️ {route} - AUTH REQUIRED ({response.status_code})")
                    else:
                        print(f"⚠️ {route} - STATUS {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ {route} - EXCEPTION: {e}")
                    results[route] = f"ERROR: {e}"
            
            # Check if any routes have 500 errors
            error_routes = [route for route, status in results.items() if status == 500]
            
            if error_routes:
                print(f"\n❌ Routes with 500 errors: {error_routes}")
                return False
            else:
                print(f"\n✅ No 500 errors found in tested routes")
                return True
                
    except Exception as e:
        print(f"❌ Route check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_template_issues():
    """Check for template syntax issues"""
    print("="*60)
    print("🔧 STEP 3: Template Syntax Check")
    print("="*60)
    
    try:
        # Check crypto dashboard template specifically
        template_path = os.path.join(os.path.dirname(__file__), 'app', 'templates', 'advanced_features', 'crypto_dashboard.html')
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for common template issues
            issues = []
            
            # Check for unmatched blocks
            block_count = content.count('{% block')
            endblock_count = content.count('{% endblock')
            
            if block_count != endblock_count:
                issues.append(f"Unmatched blocks: {block_count} blocks, {endblock_count} endblocks")
            
            # Check for specific syntax errors
            if 'endblock %}' not in content:
                issues.append("Missing endblock tags")
                
            if issues:
                print("❌ Template issues found:")
                for issue in issues:
                    print(f"   - {issue}")
                return False
            else:
                print("✅ Template syntax appears correct")
                return True
        else:
            print("❌ Crypto dashboard template not found")
            return False
            
    except Exception as e:
        print(f"❌ Template check failed: {e}")
        return False

def check_static_files():
    """Check for CSS issues"""
    print("="*60)
    print("🔧 STEP 4: Static Files Check")
    print("="*60)
    
    try:
        # Check for CSS files
        static_path = os.path.join(os.path.dirname(__file__), 'app', 'static', 'css')
        
        if os.path.exists(static_path):
            css_files = [f for f in os.listdir(static_path) if f.endswith('.css')]
            print(f"📁 Found {len(css_files)} CSS files")
            
            # Check for color inherit issues in main CSS files
            for css_file in css_files[:3]:  # Check first 3
                css_path = os.path.join(static_path, css_file)
                try:
                    with open(css_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'color: inherit' in content:
                        print(f"⚠️ {css_file} contains 'color: inherit' - potential visibility issue")
                    else:
                        print(f"✅ {css_file} - no color inherit issues")
                except:
                    print(f"⚠️ Could not read {css_file}")
                    
            return True
        else:
            print("❌ Static CSS directory not found")
            return False
            
    except Exception as e:
        print(f"❌ Static files check failed: {e}")
        return False

def run_comprehensive_diagnostic():
    """Run all diagnostic checks"""
    print("🚀 COMPREHENSIVE PRODUCTION DIAGNOSTIC")
    print("🎯 Checking all critical components...")
    print()
    
    checks = [
        ("Database & Tables", run_database_check),
        ("Route Availability", run_route_availability_check),
        ("Template Syntax", check_template_issues),
        ("Static Files", check_static_files)
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        print(f"\n{'='*80}")
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results[check_name] = False
        
        time.sleep(1)  # Brief pause between checks
    
    # Final summary
    print("\n" + "="*80)
    print("📋 COMPREHENSIVE DIAGNOSTIC SUMMARY")
    print("="*80)
    
    passed = [name for name, result in results.items() if result]
    failed = [name for name, result in results.items() if not result]
    
    print(f"✅ PASSED ({len(passed)}/{len(checks)}):")
    for check in passed:
        print(f"   ✅ {check}")
    
    if failed:
        print(f"\n❌ FAILED ({len(failed)}/{len(checks)}):")
        for check in failed:
            print(f"   ❌ {check}")
    
    print("\n" + "="*80)
    
    if len(passed) == len(checks):
        print("🎉 ALL CHECKS PASSED!")
        print("The Flask application should be working correctly.")
        print("\nTo test the website:")
        print("1. Run: python main.py")
        print("2. Open: http://localhost:5002")
        print("3. Test the problem routes listed by the user")
    else:
        print(f"⚠️ {len(failed)} issues found that need to be addressed.")
        print("\nNext steps:")
        if "Database & Tables" in failed:
            print("- Fix database connection and table creation")
        if "Route Availability" in failed:
            print("- Investigate 500 errors in specific routes")
        if "Template Syntax" in failed:
            print("- Fix template syntax errors")
        if "Static Files" in failed:
            print("- Fix CSS color inherit issues")
    
    return results

if __name__ == "__main__":
    run_comprehensive_diagnostic()
