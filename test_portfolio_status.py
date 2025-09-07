#!/usr/bin/env python3
"""Test portfolio page for 500 errors"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app import create_app
    
    app = create_app()
    
    with app.test_client() as client:
        print("Testing portfolio page...")
        
        # Test portfolio root
        response = client.get('/portfolio/')
        print(f"Portfolio root status: {response.status_code}")
        
        if response.status_code == 500:
            print("❌ 500 ERROR DETECTED!")
            print("Response data:", response.data[:1000].decode('utf-8', errors='ignore'))
        elif response.status_code == 302:
            print("✅ Redirect (likely login required)")
            print("Location:", response.headers.get('Location', 'N/A'))
        elif response.status_code == 200:
            print("✅ Portfolio page loads successfully!")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            
        # Test with demo access
        response = client.get('/portfolio/', query_string={'demo': '1'})
        print(f"Portfolio with demo param status: {response.status_code}")
        
        print("\nTest completed!")
        
except Exception as e:
    print(f"❌ Test error: {e}")
    import traceback
    traceback.print_exc()
