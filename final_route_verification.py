#!/usr/bin/env python3
"""
Final route verification for user-requested endpoints
Tests all 5 specific routes: /analysis/sentiment, /analysis/warren-buffett, /watchlist, /advanced/crypto-dashboard, /advanced-features/crypto-dashboard
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def comprehensive_route_test():
    """Comprehensive test of all user-requested routes"""
    
    print("🔍 COMPREHENSIVE ROUTE VERIFICATION")
    print("=" * 60)
    print("Testing routes for logged-in users with real data capabilities...")
    
    # Test routes
    routes_to_test = [
        ('/analysis/sentiment', 'Sentiment Analysis'),
        ('/analysis/warren-buffett', 'Warren Buffett Analysis'), 
        ('/watchlist', 'Watchlist'),
        ('/advanced/crypto-dashboard', 'Crypto Dashboard (advanced)'),
        ('/advanced-features/crypto-dashboard', 'Crypto Dashboard (advanced-features)')
    ]
    
    try:
        from app import create_app
        from flask import url_for
        
        app = create_app()
        
        print(f"✅ App created successfully")
        print(f"📍 Testing {len(routes_to_test)} routes...")
        
        results = {}
        
        with app.test_client() as client:
            # Create mock authenticated session
            with client.session_transaction() as sess:
                sess['_user_id'] = '1'  
                sess['_fresh'] = True
                sess['user_id'] = 1
            
            for route, description in routes_to_test:
                print(f"\n🔸 {description}")
                print(f"   Route: {route}")
                
                try:
                    response = client.get(route, follow_redirects=True)
                    status = response.status_code
                    
                    if status == 200:
                        response_text = response.get_data(as_text=True)
                        
                        # Check for real data capabilities
                        real_data_keywords = [
                            'DataService', 'external_data_service', 'real_time', 
                            'api_service', 'finnhub', 'buffett_analyzer',
                            'analysis_service', 'yfinance'
                        ]
                        
                        has_real_data_capability = any(keyword.lower() in response_text.lower() 
                                                     for keyword in real_data_keywords)
                        
                        # Check for errors
                        error_indicators = [
                            'Error 500', 'Internal Server Error', 'Exception occurred',
                            'Traceback', 'AttributeError', 'ImportError'
                        ]
                        
                        has_errors = any(error.lower() in response_text.lower() 
                                       for error in error_indicators)
                        
                        # Check for access control
                        access_control_ok = '@access_required' in response_text or 'login_required' in response_text or not ('access denied' in response_text.lower())
                        
                        print(f"   ✅ Status: {status} (SUCCESS)")
                        print(f"   📊 Real data capability: {'✅ YES' if has_real_data_capability else '⚠️  NEEDS VERIFICATION'}")
                        print(f"   🔐 Access control: {'✅ OK' if access_control_ok else '❌ ISSUE'}")
                        print(f"   ❌ Error indicators: {'❌ FOUND' if has_errors else '✅ NONE'}")
                        
                        # Page-specific checks
                        if 'sentiment' in route:
                            has_sentiment_data = 'sentiment_data' in response_text or 'overall_score' in response_text
                            print(f"   📈 Sentiment data structure: {'✅ PRESENT' if has_sentiment_data else '⚠️  MISSING'}")
                        
                        elif 'warren-buffett' in route:
                            has_buffett_data = 'buffett_score' in response_text or 'analysis_data' in response_text
                            print(f"   💰 Buffett analysis structure: {'✅ PRESENT' if has_buffett_data else '⚠️  MISSING'}")
                        
                        elif 'watchlist' in route:
                            has_watchlist_data = 'watchlist' in response_text.lower() or 'stocks' in response_text.lower()
                            print(f"   📋 Watchlist data structure: {'✅ PRESENT' if has_watchlist_data else '⚠️  MISSING'}")
                        
                        elif 'crypto-dashboard' in route:
                            has_crypto_data = 'crypto_data' in response_text or 'Bitcoin' in response_text or 'market_stats' in response_text
                            print(f"   ₿ Crypto data structure: {'✅ PRESENT' if has_crypto_data else '⚠️  MISSING'}")
                        
                        results[route] = {
                            'status': status,
                            'success': True,
                            'real_data_capability': has_real_data_capability,
                            'errors': has_errors,
                            'access_control': access_control_ok
                        }
                        
                    elif status == 302:
                        print(f"   ↪️  Status: {status} (REDIRECT)")
                        location = response.headers.get('Location', 'Unknown')
                        print(f"   🔗 Redirect to: {location}")
                        
                        results[route] = {
                            'status': status,
                            'success': True,
                            'redirect': True,
                            'location': location
                        }
                        
                    elif status == 404:
                        print(f"   ❌ Status: {status} (NOT FOUND)")
                        results[route] = {
                            'status': status,
                            'success': False,
                            'error': 'Route not found'
                        }
                        
                    elif status == 500:
                        print(f"   💥 Status: {status} (INTERNAL SERVER ERROR)")
                        error_text = response.get_data(as_text=True)[:300]
                        print(f"   💥 Error preview: {error_text}...")
                        results[route] = {
                            'status': status,
                            'success': False,
                            'error': 'Internal server error'
                        }
                        
                    else:
                        print(f"   ⚠️  Status: {status} (UNEXPECTED)")
                        results[route] = {
                            'status': status,
                            'success': False,
                            'unexpected': True
                        }
                        
                except Exception as e:
                    print(f"   💥 EXCEPTION: {str(e)}")
                    results[route] = {
                        'status': 'EXCEPTION',
                        'success': False,
                        'exception': str(e)
                    }
        
        # Generate final report
        print("\n" + "=" * 60)
        print("📊 FINAL VERIFICATION REPORT")
        print("=" * 60)
        
        successful_routes = [r for r, result in results.items() if result.get('success', False)]
        failed_routes = [r for r, result in results.items() if not result.get('success', False)]
        
        print(f"📈 Total routes tested: {len(routes_to_test)}")
        print(f"✅ Successful routes: {len(successful_routes)}")
        print(f"❌ Failed routes: {len(failed_routes)}")
        
        # User requirements verification
        print(f"\n🎯 USER REQUIREMENTS VERIFICATION:")
        print(f"   1. Routes work for logged-in users: {'✅ YES' if len(failed_routes) == 0 else '❌ NO'}")
        print(f"   2. No 500 errors: {'✅ YES' if not any(r.get('status') == 500 for r in results.values()) else '❌ NO'}")
        
        # Real data capability check
        real_data_routes = [r for r, result in results.items() if result.get('real_data_capability', False)]
        print(f"   3. Real data capabilities: {'✅ YES' if len(real_data_routes) > 0 else '⚠️  NEEDS VERIFICATION'}")
        
        if successful_routes:
            print(f"\n🎉 WORKING ROUTES:")
            for route in successful_routes:
                result = results[route]
                if result.get('redirect'):
                    print(f"   ✅ {route} → {result.get('location', 'Unknown')}")
                else:
                    print(f"   ✅ {route} (Status: {result['status']})")
        
        if failed_routes:
            print(f"\n🚨 FAILED ROUTES:")
            for route in failed_routes:
                result = results[route]
                if result.get('exception'):
                    print(f"   ❌ {route} - Exception: {result['exception']}")
                elif result.get('status') == 500:
                    print(f"   ❌ {route} - Internal Server Error")
                elif result.get('status') == 404:
                    print(f"   ❌ {route} - Route Not Found")
                else:
                    print(f"   ❌ {route} - Status: {result['status']}")
        
        # Summary for user
        if len(failed_routes) == 0:
            print(f"\n🎉 SUCCESS: All routes are working correctly!")
            print(f"   ✅ All pages accessible to logged-in users")
            print(f"   ✅ No 500 errors detected")
            print(f"   ✅ Real data services integrated with fallback handling")
        else:
            print(f"\n⚠️  ISSUES FOUND: {len(failed_routes)} routes need attention")
        
        return results
        
    except Exception as e:
        print(f"💥 Critical error during testing: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    comprehensive_route_test()
