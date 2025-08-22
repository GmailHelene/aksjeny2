#!/usr/bin/env python3
"""
Quick test script to verify Warren Buffett analysis route works
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app

def test_analysis_route():
    """Test the Warren Buffett analysis route"""
    app = create_app('testing')
    
    with app.test_client() as client:
        try:
            # Test Warren Buffett analysis route with XRP-USD ticker
            response = client.get('/analysis/warren-buffett?ticker=XRP-USD')
            print(f"Warren Buffett analysis route status: {response.status_code}")
            
            if response.status_code == 500:
                print("❌ Still getting 500 error")
                print(f"Response data: {response.data.decode()}")
                return False
            elif response.status_code in [200, 302]:  # 302 if redirected
                print("✅ Warren Buffett analysis route is working!")
                return True
            else:
                print(f"Unexpected status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error testing route: {e}")
            return False

if __name__ == "__main__":
    test_analysis_route()
