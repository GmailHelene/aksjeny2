#!/usr/bin/env python3
"""
Route verification script for specific user-requested endpoints
Tests: /analysis/sentiment, /analysis/warren-buffett, /watchlist, /advanced/crypto-dashboard, /advanced-features/crypto-dashboard
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_routes():
    """Test the specific routes requested by user"""
    try:
        from app import create_app
        from flask import url_for
        
        app = create_app()
        
        # Test routes
        routes_to_test = [
            '/analysis/sentiment',
            '/analysis/warren-buffett', 
            '/watchlist',
            '/advanced/crypto-dashboard',
            '/advanced-features/crypto-dashboard'
        ]
        
        print("🔍 Testing routes for logged-in users with real data...")
        print("=" * 60)
        
        with app.test_client() as client:
            # Create a mock session to simulate logged-in user
            with client.session_transaction() as sess:
                sess['_user_id'] = '1'  
                sess['_fresh'] = True
                sess['user_id'] = 1
            
            results = {}
            
            for route in routes_to_test:
                print(f"\n📍 Testing: {route}")
                try:
                    response = client.get(route, follow_redirects=True)
                    status = response.status_code
                    
                    if status == 200:
                        # Check if response contains real data indicators
                        response_text = response.get_data(as_text=True)
                        
                        # Look for signs of real data vs demo data
                        has_real_data_indicators = any([
                            'DataService' in response_text,
                            'real_time' in response_text.lower(),
                            'live_data' in response_text.lower(),
                            'api_data' in response_text.lower(),
                            'external_data' in response_text.lower()
                        ])
                        
                        # Look for error indicators
                        has_errors = any([
                            'Error 500' in response_text,
                            'Internal Server Error' in response_text,
                            'Exception' in response_text,
                            'Traceback' in response_text
                        ])
                        
                        # Look for demo/fallback indicators
                        has_demo_fallback = any([
                            'fallback' in response_text.lower(),
                            'demo_data' in response_text.lower(),
                            'mock_data' in response_text.lower(),
                            'utilgjengelig' in response_text.lower(),
                            'midlertidig' in response_text.lower()
                        ])
                        
                        print(f"  ✅ Status: {status} (SUCCESS)")
                        print(f"  📊 Real data indicators: {'Yes' if has_real_data_indicators else 'No'}")
                        print(f"  ⚠️  Demo/fallback indicators: {'Yes' if has_demo_fallback else 'No'}")
                        print(f"  ❌ Error indicators: {'Yes' if has_errors else 'No'}")
                        
                        results[route] = {
                            'status': status,
                            'success': True,
                            'has_real_data': has_real_data_indicators,
                            'has_fallback': has_demo_fallback,
                            'has_errors': has_errors
                        }
                        
                    elif status == 302:
                        print(f"  ↪️  Status: {status} (REDIRECT)")
                        print(f"  🔗 Redirect location: {response.location}")
                        results[route] = {
                            'status': status,
                            'success': True,
                            'redirect': True,
                            'location': response.location
                        }
                        
                    elif status == 500:
                        print(f"  ❌ Status: {status} (INTERNAL SERVER ERROR)")
                        error_text = response.get_data(as_text=True)[:500]
                        print(f"  💥 Error preview: {error_text}")
                        results[route] = {
                            'status': status,
                            'success': False,
                            'error': error_text
                        }
                        
                    else:
                        print(f"  ⚠️  Status: {status} (UNEXPECTED)")
                        results[route] = {
                            'status': status,
                            'success': False,
                            'unexpected': True
                        }
                        
                except Exception as e:
                    print(f"  💥 EXCEPTION: {str(e)}")
                    results[route] = {
                        'status': 'EXCEPTION',
                        'success': False,
                        'exception': str(e)
                    }
            
            # Summary
            print("\n" + "=" * 60)
            print("📋 SUMMARY REPORT")
            print("=" * 60)
            
            successful_routes = [r for r, result in results.items() if result.get('success', False)]
            failed_routes = [r for r, result in results.items() if not result.get('success', False)]
            
            print(f"✅ Successful routes: {len(successful_routes)}/{len(routes_to_test)}")
            print(f"❌ Failed routes: {len(failed_routes)}/{len(routes_to_test)}")
            
            if successful_routes:
                print("\n🎉 Working routes:")
                for route in successful_routes:
                    result = results[route]
                    if result.get('redirect'):
                        print(f"  • {route} → {result.get('location', 'Unknown')}")
                    else:
                        print(f"  • {route} (Status: {result['status']})")
            
            if failed_routes:
                print("\n🚨 Failed routes:")
                for route in failed_routes:
                    result = results[route]
                    if result.get('exception'):
                        print(f"  • {route} - Exception: {result['exception']}")
                    elif result['status'] == 500:
                        print(f"  • {route} - Internal Server Error")
                    else:
                        print(f"  • {route} - Status: {result['status']}")
            
            # Real data analysis
            real_data_routes = [r for r, result in results.items() if result.get('has_real_data', False)]
            fallback_routes = [r for r, result in results.items() if result.get('has_fallback', False)]
            
            print(f"\n📊 Real data detection: {len(real_data_routes)}/{len(successful_routes)} working routes")
            print(f"🔄 Fallback data detection: {len(fallback_routes)}/{len(successful_routes)} working routes")
            
            print("\n🎯 USER REQUIREMENTS CHECK:")
            print(f"  ✅ Routes work for logged-in users: {'YES' if len(failed_routes) == 0 else 'NO'}")
            print(f"  ✅ No 500 errors: {'YES' if not any(r.get('status') == 500 for r in results.values()) else 'NO'}")
            print(f"  ✅ Real data available: {'YES' if len(real_data_routes) > 0 else 'NEEDS VERIFICATION'}")
            
            return results
            
    except Exception as e:
        print(f"💥 Critical error during testing: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_routes()
