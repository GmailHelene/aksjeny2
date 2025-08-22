#!/usr/bin/env python3
"""
Test and fix critical production issues for aksjeradar.trade
"""

import sys
import os

# Set up path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set required environment variables
os.environ.setdefault('EMAIL_USERNAME', 'support@luxushair.com')
os.environ.setdefault('EMAIL_PASSWORD', 'suetozoydejwntii')
os.environ.setdefault('EMAIL_PORT', '587')
os.environ.setdefault('EMAIL_SERVER', 'imap.gmail.com')
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway')

def test_database_initialization():
    """Test and initialize database tables"""
    print("=" * 60)
    print("🔧 STEP 1: Database Initialization")
    print("=" * 60)
    
    try:
        from app import create_app
        from app.models import db
        from app.models.achievements import UserStats
        
        app = create_app('development')
        with app.app_context():
            print("📋 Creating database tables...")
            db.create_all()
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ Available tables: {', '.join(tables)}")
            
            if 'user_stats' in tables:
                print("✅ UserStats table exists - database issue should be resolved")
                return True
            else:
                print("❌ UserStats table still missing")
                return False
                
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_crypto_dashboard_route():
    """Test crypto dashboard route for 500 errors"""
    print("=" * 60)
    print("🔧 STEP 2: Testing Crypto Dashboard Route")
    print("=" * 60)
    
    try:
        from app import create_app
        
        app = create_app('development')
        with app.test_client() as client:
            # Test crypto dashboard route
            response = client.get('/advanced-features/crypto-dashboard')
            print(f"📊 Crypto dashboard status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Crypto dashboard route working correctly")
                return True
            elif response.status_code == 500:
                print("❌ Crypto dashboard 500 error still exists")
                print(f"Response data: {response.data[:500]}")
                return False
            else:
                print(f"⚠️ Unexpected status code: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Crypto dashboard test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_watchlist_routes():
    """Test watchlist routes for 500 errors"""
    print("=" * 60)
    print("🔧 STEP 3: Testing Watchlist Routes")
    print("=" * 60)
    
    try:
        from app import create_app
        
        app = create_app('development')
        with app.test_client() as client:
            # Test main watchlist route
            response = client.get('/watchlist')
            print(f"📊 Watchlist page status: {response.status_code}")
            
            # Test watchlist API endpoint (needs auth)
            response = client.post('/api/watchlist/add', 
                                 json={'symbol': 'AAPL'},
                                 content_type='application/json')
            print(f"📊 Watchlist API status: {response.status_code}")
            
            if response.status_code in [200, 401, 403]:  # 401/403 expected without auth
                print("✅ Watchlist routes responding correctly")
                return True
            else:
                print(f"❌ Watchlist routes have issues")
                return False
                
    except Exception as e:
        print(f"❌ Watchlist test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_routes():
    """Test stock routes for financial data issues"""
    print("=" * 60)
    print("🔧 STEP 4: Testing Stock Routes")
    print("=" * 60)
    
    try:
        from app import create_app
        
        app = create_app('development')
        with app.test_client() as client:
            # Test stock details page
            response = client.get('/stocks/AAPL')
            print(f"📊 Stock details status: {response.status_code}")
            
            if response.status_code == 200:
                # Check if financial data is present
                content = response.data.decode('utf-8')
                
                # Check for common issues
                issues = []
                if 'volume": "-"' in content or 'Volume: -' in content:
                    issues.append("Volume showing '-'")
                if 'market_cap": "-"' in content or 'Market Cap: -' in content:
                    issues.append("Market cap showing '-'")
                if 'Henter kursdata' in content:
                    issues.append("Chart loading message still present")
                if 'Ikke tilgjengelig' in content:
                    issues.append("Company info showing 'Ikke tilgjengelig'")
                
                if issues:
                    print("❌ Stock data issues found:")
                    for issue in issues:
                        print(f"   - {issue}")
                    return False
                else:
                    print("✅ Stock routes working with proper data")
                    return True
            else:
                print(f"❌ Stock details route failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Stock routes test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sentiment_and_compare():
    """Test sentiment analysis and stock compare routes"""
    print("=" * 60)
    print("🔧 STEP 5: Testing Sentiment Analysis & Stock Compare")
    print("=" * 60)
    
    try:
        from app import create_app
        
        app = create_app('development')
        with app.test_client() as client:
            # Test sentiment analysis
            response = client.get('/analysis/sentiment')
            print(f"📊 Sentiment analysis status: {response.status_code}")
            
            # Test stock compare
            response = client.get('/stocks/compare?symbols=AAPL,MSFT')
            print(f"📊 Stock compare status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Analysis routes working correctly")
                return True
            else:
                print(f"❌ Analysis routes have 500 errors")
                return False
                
    except Exception as e:
        print(f"❌ Analysis routes test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_comprehensive_test():
    """Run all tests and report results"""
    print("🚀 COMPREHENSIVE PRODUCTION ISSUE TESTING")
    print("🎯 Testing all critical routes and functionality...")
    
    tests = [
        ("Database Initialization", test_database_initialization),
        ("Crypto Dashboard", test_crypto_dashboard_route),
        ("Watchlist Routes", test_watchlist_routes),
        ("Stock Routes & Data", test_stock_routes),
        ("Sentiment & Compare", test_sentiment_and_compare)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*80}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*80)
    print("📋 COMPREHENSIVE TEST RESULTS SUMMARY")
    print("="*80)
    
    passed = [name for name, result in results.items() if result]
    failed = [name for name, result in results.items() if not result]
    
    print(f"✅ PASSED ({len(passed)}/{len(tests)}):")
    for test in passed:
        print(f"   ✅ {test}")
    
    if failed:
        print(f"\n❌ FAILED ({len(failed)}/{len(tests)}):")
        for test in failed:
            print(f"   ❌ {test}")
    
    if len(passed) == len(tests):
        print("\n🎉 ALL TESTS PASSED! Production issues should be resolved.")
    else:
        print(f"\n⚠️ {len(failed)} issues remain to be fixed.")
    
    return results

if __name__ == "__main__":
    run_comprehensive_test()
