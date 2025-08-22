#!/usr/bin/env python3
"""
Quick test for sentiment and crypto dashboard routes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
import logging

def test_routes():
    """Test the problematic routes"""
    app = create_app()
    
    with app.test_client() as client:
        print("🧪 Testing fixed routes...")
        
        # Test sentiment analysis route
        print("\n1. Testing sentiment analysis route:")
        try:
            response = client.get('/analysis/sentiment?symbol=FLNG.OL')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Sentiment route working!")
            else:
                print(f"   ❌ Sentiment route failed: {response.status_code}")
                print(f"   Response: {response.data.decode()[:200]}...")
        except Exception as e:
            print(f"   ❌ Sentiment route error: {e}")
        
        # Test crypto dashboard route
        print("\n2. Testing crypto dashboard route:")
        try:
            response = client.get('/advanced/crypto-dashboard')
            print(f"   Status: {response.status_code}")
            if response.status_code in [200, 302]:  # 302 is redirect, which is OK
                print("   ✅ Crypto dashboard route working!")
                if response.status_code == 302:
                    print(f"   Redirects to: {response.location}")
            else:
                print(f"   ❌ Crypto dashboard route failed: {response.status_code}")
                print(f"   Response: {response.data.decode()[:200]}...")
        except Exception as e:
            print(f"   ❌ Crypto dashboard route error: {e}")
        
        # Test advanced features crypto route directly
        print("\n3. Testing advanced features crypto route:")
        try:
            response = client.get('/advanced-features/crypto-dashboard')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Advanced features crypto route working!")
            else:
                print(f"   ❌ Advanced features crypto route failed: {response.status_code}")
                print(f"   Response: {response.data.decode()[:200]}...")
        except Exception as e:
            print(f"   ❌ Advanced features crypto route error: {e}")

if __name__ == '__main__':
    test_routes()
