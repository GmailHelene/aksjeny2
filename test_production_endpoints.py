#!/usr/bin/env python3

import requests
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    
    # Retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        backoff_factor=1
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def test_production_endpoints():
    """Test the production endpoints that were having 500 errors"""
    
    # Production URLs to test
    base_url = "https://aksjeradar.trade"
    endpoints = [
        "/",  # Index page
        "/stocks/list/crypto",  # Crypto list
        "/stocks/list/currency",  # Currency list
        "/analysis/sentiment?symbol=DNB.OL",  # Sentiment analysis
        "/stocks/list/global",  # Global stocks list
    ]
    
    session = create_session()
    
    # Set headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    print("🔍 Testing Production Endpoints")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            print(f"\n📋 Testing: {base_url}{endpoint}")
            
            response = session.get(
                base_url + endpoint, 
                headers=headers, 
                timeout=30,
                allow_redirects=True
            )
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"   Content-Length: {len(response.content)} bytes")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS - Endpoint working correctly")
                
                # Check for specific content indicators
                content = response.text.lower()
                
                if endpoint == "/":
                    if "aksjeradar" in content and "aksjer" in content:
                        print(f"   ✅ Content verified - Contains expected homepage elements")
                    else:
                        print(f"   ⚠️  Content warning - May not be fully loaded")
                
                elif endpoint == "/stocks/list/crypto":
                    if "bitcoin" in content or "btc" in content or "krypto" in content:
                        print(f"   ✅ Content verified - Contains crypto data")
                    else:
                        print(f"   ⚠️  Content warning - May not contain crypto data")
                
                elif endpoint == "/stocks/list/currency":
                    if "usd" in content or "eur" in content or "valuta" in content:
                        print(f"   ✅ Content verified - Contains currency data")
                    else:
                        print(f"   ⚠️  Content warning - May not contain currency data")
                
                elif "sentiment" in endpoint:
                    if "sentiment" in content or "dnb" in content:
                        print(f"   ✅ Content verified - Contains sentiment analysis")
                    else:
                        print(f"   ⚠️  Content warning - May not contain sentiment data")
                
                elif endpoint == "/stocks/list/global":
                    if "aapl" in content or "global" in content or "apple" in content:
                        print(f"   ✅ Content verified - Contains global stocks data")
                    else:
                        print(f"   ⚠️  Content warning - May not contain global stocks data")
                        
            elif response.status_code == 302:
                redirect_url = response.headers.get('Location', 'Unknown')
                print(f"   🔄 REDIRECT to: {redirect_url}")
                
                # Check if redirect is to login page (which would indicate auth required)
                if "login" in redirect_url.lower():
                    print(f"   ℹ️  Endpoint requires authentication")
                else:
                    print(f"   ℹ️  Normal redirect")
                    
            elif response.status_code == 403:
                print(f"   🔒 ACCESS DENIED - May require authentication")
                
            elif response.status_code == 404:
                print(f"   ❌ NOT FOUND - Endpoint may not exist")
                
            elif response.status_code == 500:
                print(f"   ❌ SERVER ERROR - The reported issue still exists!")
                # Try to get error details
                if "text/html" in response.headers.get('Content-Type', ''):
                    if "error" in response.text.lower():
                        print(f"   💥 Error content detected in response")
                
            else:
                print(f"   ⚠️  UNEXPECTED STATUS: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ CONNECTION ERROR: {e}")
            
        except Exception as e:
            print(f"   ❌ UNEXPECTED ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Production Testing Complete")
    
    # Summary
    print("\n📊 Summary:")
    print("If you see ✅ SUCCESS for all endpoints, the issues have been resolved.")
    print("If you see ❌ SERVER ERROR (500), the issues still exist.")
    print("If you see 🔄 REDIRECT to login, authentication may be required.")

if __name__ == "__main__":
    test_production_endpoints()
