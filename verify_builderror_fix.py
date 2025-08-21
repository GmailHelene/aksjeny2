#!/usr/bin/env python3
"""
Final BuildError verification script
Tests that all fixed endpoints are now working correctly
"""

def test_portfolio_endpoints():
    """Test if portfolio endpoints are working"""
    print("🔍 Testing Portfolio Endpoints...")
    print("="*40)
    
    # Test cases based on our fixes
    test_cases = [
        {
            'endpoint': 'portfolio.stock_tips',
            'description': 'Stock tips page (FIXED)',
            'expected': '/portfolio/tips'
        },
        {
            'endpoint': 'portfolio.index', 
            'description': 'Portfolio index page (FIXED)',
            'expected': '/portfolio/'
        },
        {
            'endpoint': 'portfolio.view_portfolio',
            'description': 'View portfolio page (CORRECT)',
            'expected': '/portfolio/view/',
            'requires_id': True
        }
    ]
    
    try:
        import sys
        import os
        sys.path.insert(0, '.')
        
        from app import create_app
        from flask import url_for
        
        app = create_app()
        
        with app.app_context():
            with app.test_request_context():
                
                for test in test_cases:
                    endpoint = test['endpoint']
                    description = test['description']
                    
                    try:
                        if test.get('requires_id'):
                            url = url_for(endpoint, id=1)
                        else:
                            url = url_for(endpoint)
                        
                        print(f"✅ {endpoint}: {url} - {description}")
                        
                    except Exception as e:
                        print(f"❌ {endpoint}: FAILED - {e}")
                
                print("\n" + "="*40)
                print("🎯 TESTING PREVIOUSLY BROKEN ENDPOINTS")
                print("="*40)
                
                # Test endpoints that should now fail (as expected)
                broken_endpoints = [
                    'portfolio.tips',
                    'portfolio.portfolio_index', 
                    'auth.profile'
                ]
                
                for endpoint in broken_endpoints:
                    try:
                        url = url_for(endpoint)
                        print(f"⚠️  {endpoint}: UNEXPECTEDLY WORKS - {url}")
                    except Exception as e:
                        print(f"✅ {endpoint}: Correctly fails - {str(e)[:50]}...")
                        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting BuildError Fix Verification")
    print("="*50)
    success = test_portfolio_endpoints()
    print("\n" + "="*50)
    if success:
        print("🎉 All endpoint tests completed!")
    else:
        print("❌ Some tests failed - check output above")
