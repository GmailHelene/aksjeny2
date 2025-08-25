import urllib.request
import urllib.error
from datetime import datetime

def test_endpoints():
    """Simple test for problematic endpoints"""
    
    endpoints = [
        ('Profile Page', 'https://aksjeradar.trade/profile'),
        ('Oslo Stocks', 'https://aksjeradar.trade/stocks/list/oslo')
    ]
    
    print(f"Testing endpoints - {datetime.now()}")
    print("=" * 50)
    
    for name, url in endpoints:
        print(f"\nTesting: {name}")
        print(f"URL: {url}")
        
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                status = response.getcode()
                content = response.read().decode('utf-8', errors='ignore')
                
                print(f"Status: {status}")
                print(f"Response length: {len(content)} bytes")
                
                if status == 500:
                    print("❌ 500 INTERNAL SERVER ERROR")
                elif status == 200:
                    if 'det oppstod en teknisk feil' in content.lower():
                        print("⚠️ Page loads but shows error message")
                    elif name == 'Profile Page' and ('profile' in content.lower() or 'velkommen' in content.lower()):
                        print("✅ Profile page working")
                    elif name == 'Oslo Stocks' and ('eqnr' in content.lower() or 'oslo' in content.lower()):
                        print("✅ Oslo stocks page working")
                    else:
                        print("⚠️ Page loads but content unclear")
                elif status == 302:
                    print("🔄 Redirected (likely to login)")
                else:
                    print(f"⚠️ Status: {status}")
                    
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP Error: {e.code}")
            if e.code == 500:
                print("   500 Internal Server Error detected")
        except urllib.error.URLError as e:
            print(f"❌ URL Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Test complete")

if __name__ == '__main__':
    test_endpoints()
