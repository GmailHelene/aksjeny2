#!/usr/bin/env python3
"""Test script to verify portfolio navigation fix"""
import requests
from urllib.parse import urljoin

def test_navigation_fix():
    """Test that portfolio navigation no longer causes BuildError"""
    base_url = "http://localhost:5000"
    
    print("Testing portfolio navigation fix...")
    
    try:
        # Test homepage load
        response = requests.get(base_url, timeout=5)
        print(f"Homepage status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check if CSS code is appearing as text (look for style tags in body)
            if '<style>' in content and not content.count('<style>') == content.count('</style>'):
                print("⚠️  WARNING: Possible unclosed style tag detected")
            else:
                print("✅ CSS structure looks good")
            
            # Check if portfolio link exists
            if 'url_for("portfolio.index")' in content or 'portfolio.index' in content:
                print("✅ Portfolio navigation appears to use correct endpoint")
            else:
                print("❓ Could not verify portfolio navigation endpoint in HTML")
                
        # Test if we can access the portfolio index directly (will redirect to login for non-auth users)
        portfolio_response = requests.get(f"{base_url}/portfolio/", timeout=5, allow_redirects=False)
        print(f"Portfolio index status: {portfolio_response.status_code} (should be 302 redirect to login)")
        
        if portfolio_response.status_code in [200, 302]:
            print("✅ Portfolio index endpoint exists and responds correctly")
        else:
            print(f"❌ Portfolio index endpoint issue: {portfolio_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Please ensure Flask app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_navigation_fix()
