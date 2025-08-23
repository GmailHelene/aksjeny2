#!/usr/bin/env python3
"""
Test the specific problematic routes mentioned by the user
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_problematic_routes():
    """Test the three specific problematic routes"""
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            print("🧪 Testing problematic routes...")
            
            # Test 1: TradingView route
            print("\n1. Testing TradingView route (/analysis/tradingview)")
            try:
                response = client.get('/analysis/tradingview')
                print(f"   Status Code: {response.status_code}")
                if response.status_code == 200:
                    html_content = response.get_data(as_text=True)
                    if 'TradingView Charts' in html_content:
                        print("   ✅ TradingView route works - page loads correctly")
                    else:
                        print("   ⚠️ TradingView route loads but content may be missing")
                else:
                    print(f"   ❌ TradingView route failed with status {response.status_code}")
            except Exception as e:
                print(f"   ❌ TradingView route error: {e}")
            
            # Test 2: Warren Buffett with ticker
            print("\n2. Testing Warren Buffett with ticker (/analysis/warren-buffett?ticker=TEL.OL)")
            try:
                response = client.get('/analysis/warren-buffett?ticker=TEL.OL')
                print(f"   Status Code: {response.status_code}")
                if response.status_code == 200:
                    html_content = response.get_data(as_text=True)
                    if 'TEL.OL' in html_content and 'Warren Buffett' in html_content:
                        print("   ✅ Warren Buffett ticker route works correctly")
                    else:
                        print("   ⚠️ Warren Buffett route loads but ticker may not be processed")
                        print(f"   Contains TEL.OL: {'TEL.OL' in html_content}")
                        print(f"   Contains Warren Buffett: {'Warren Buffett' in html_content}")
                else:
                    print(f"   ❌ Warren Buffett ticker route failed with status {response.status_code}")
            except Exception as e:
                print(f"   ❌ Warren Buffett ticker route error: {e}")
            
            # Test 3: Sentiment with symbol
            print("\n3. Testing Sentiment with symbol (/analysis/sentiment?symbol=FLNG.OL)")
            try:
                response = client.get('/analysis/sentiment?symbol=FLNG.OL')
                print(f"   Status Code: {response.status_code}")
                if response.status_code == 200:
                    html_content = response.get_data(as_text=True)
                    if 'FLNG.OL' in html_content and 'sentiment' in html_content.lower():
                        print("   ✅ Sentiment symbol route works correctly")
                    else:
                        print("   ⚠️ Sentiment route loads but symbol may not be processed")
                        print(f"   Contains FLNG.OL: {'FLNG.OL' in html_content}")
                        print(f"   Contains sentiment: {'sentiment' in html_content.lower()}")
                else:
                    print(f"   ❌ Sentiment symbol route failed with status {response.status_code}")
            except Exception as e:
                print(f"   ❌ Sentiment symbol route error: {e}")
            
            # Test base routes without parameters
            print("\n4. Testing base routes...")
            base_routes = [
                '/analysis/tradingview',
                '/analysis/warren-buffett', 
                '/analysis/sentiment'
            ]
            
            for route in base_routes:
                try:
                    response = client.get(route)
                    status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                    print(f"   {route}: {status}")
                except Exception as e:
                    print(f"   {route}: ❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Critical error in route testing: {e}")
        return False

def check_route_implementations():
    """Check that route functions exist and are properly implemented"""
    print("\n🔍 Checking route implementations...")
    
    try:
        from app.routes.analysis import analysis
        
        # Get all routes in the analysis blueprint
        routes = []
        for rule in analysis.url_map.iter_rules():
            routes.append(str(rule))
        
        # Check specific routes
        required_routes = [
            '/analysis/tradingview',
            '/analysis/warren-buffett',
            '/analysis/sentiment'
        ]
        
        for route in required_routes:
            # Check if route exists in blueprint
            route_exists = any(route in r for r in routes)
            if route_exists:
                print(f"   ✅ {route} - route exists")
            else:
                print(f"   ❌ {route} - route missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking route implementations: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Analysis Routes")
    print("=" * 50)
    
    # Test route implementations
    check_route_implementations()
    
    # Test actual route responses
    test_problematic_routes()
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")

if __name__ == '__main__':
    main()
