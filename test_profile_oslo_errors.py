#!/usr/bin/env python3
"""
Test script to debug profile and Oslo stocks page errors
"""
import requests
import sys
import traceback
from datetime import datetime

def test_endpoints():
    """Test the problematic endpoints to identify specific errors"""
    
    base_url = 'https://aksjeradar.trade'
    
    endpoints = [
        {
            'name': 'Profile Page',
            'url': f'{base_url}/profile',
            'description': 'User profile page - should redirect to login or show profile'
        },
        {
            'name': 'Oslo Stocks Page', 
            'url': f'{base_url}/stocks/list/oslo',
            'description': 'Oslo Børs stocks listing page'
        }
    ]
    
    print(f"🔍 Testing problematic endpoints - {datetime.now()}")
    print("=" * 60)
    
    for endpoint in endpoints:
        print(f"\n📍 Testing: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        print(f"   Description: {endpoint['description']}")
        
        try:
            # Test with proper headers to mimic browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'nb-NO,nb;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(endpoint['url'], headers=headers, timeout=30, allow_redirects=True)
            
            print(f"   ✅ Status Code: {response.status_code}")
            print(f"   📊 Response Length: {len(response.content)} bytes")
            print(f"   🔄 Final URL: {response.url}")
            
            # Check for specific error messages in response
            content = response.text.lower()
            
            if response.status_code == 500:
                print(f"   ❌ 500 INTERNAL SERVER ERROR detected!")
                if 'det oppstod en teknisk feil' in content:
                    print(f"   📝 Found Norwegian error message in response")
                if 'error' in content:
                    print(f"   📝 Generic error message found in response")
                    
            elif response.status_code == 200:
                if 'det oppstod en teknisk feil' in content:
                    print(f"   ⚠️  200 OK but contains error message!")
                    print(f"   📝 Error message: 'Det oppstod en teknisk feil under lasting av profilen'")
                elif 'profile' in endpoint['name'].lower() and 'velkommen' in content:
                    print(f"   ✅ Profile page appears to be working")
                elif 'oslo' in endpoint['name'].lower() and ('eqnr' in content or 'dnb' in content):
                    print(f"   ✅ Oslo stocks page appears to be working")
                else:
                    print(f"   ⚠️  Page loaded but content unclear")
                    
            elif response.status_code == 302:
                print(f"   🔄 Redirect detected - likely to login page")
                
            else:
                print(f"   ⚠️  Unexpected status code: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Request timed out (30s)")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection error - server may be down")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print(f"   📋 Traceback: {traceback.format_exc()}")
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print("- If you see 500 errors, there are backend Python exceptions")
    print("- If you see 200 OK with error messages, the error handling is working but underlying issue remains")
    print("- If you see 302 redirects for /profile, that's normal for non-authenticated users")
    print("- The Oslo stocks page should return 200 OK with stock data")

if __name__ == '__main__':
    test_endpoints()
