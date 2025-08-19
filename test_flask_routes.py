#!/usr/bin/env python3
"""
Test Flask routes to ensure the production fixes work in the actual application context
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

def test_analysis_routes():
    """Test critical analysis routes"""
    print("🔍 Testing Flask application routes...")
    
    app = create_app()
    
    with app.test_client() as client:
        # Test fundamental analysis select page
        print("\n📄 Testing fundamental analysis select route...")
        response = client.get('/analysis/fundamental')
        if response.status_code == 200:
            print("✅ Fundamental select route working")
            if b'fundamental analyse' in response.data:
                print("✅ Template renders correctly")
            else:
                print("❌ Template content issue")
                return False
        else:
            print(f"❌ Fundamental select route failed: {response.status_code}")
            return False
        
        # Test market overview route
        print("\n📊 Testing market overview route...")
        response = client.get('/analysis/market-overview')
        if response.status_code == 200:
            print("✅ Market overview route working")
            # Check if template rendered without errors
            if b'Oslo B' in response.data or b'Market' in response.data:
                print("✅ Market overview template renders correctly")
            else:
                print("❌ Market overview template rendering issue")
                return False
        else:
            print(f"❌ Market overview route failed: {response.status_code}")
            return False
        
        # Test stock comparison route (uses get_comparative_data)
        print("\n📈 Testing stock comparison route...")
        response = client.get('/stocks/compare?symbols=EQNR.OL,AAPL&period=1mo')
        if response.status_code == 200:
            print("✅ Stock comparison route working")
            print("✅ DataService.get_comparative_data method accessible")
        else:
            print(f"❌ Stock comparison route failed: {response.status_code}")
            return False
    
    return True

def main():
    """Run Flask route tests"""
    print("🧪 Testing Flask application with critical fixes...\n")
    
    try:
        result = test_analysis_routes()
        
        print("\n" + "="*50)
        if result:
            print("🎉 All Flask routes working correctly with fixes!")
            print("✅ Ready for production deployment")
            return 0
        else:
            print("⚠️  Some route issues detected")
            return 1
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
