import requests
import time

def test_search():
    """Test search functionality"""
    print("Testing search functionality...")
    
    try:
        # Test the search endpoint
        url = "http://localhost:5000/stocks/search?q=tesla"
        print(f"Testing URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            if "Tesla" in content or "TSLA" in content:
                print("✅ Search is working - found Tesla results")
            elif "No results" in content:
                print("❌ Search returned no results")
            else:
                print("⚠️ Search returned HTML but unclear if results found")
                print(f"Content length: {len(content)} characters")
                # Print first 500 chars to see what we got
                print("First 500 chars:")
                print(content[:500])
        else:
            print(f"❌ Search failed with status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except requests.ConnectionError:
        print("❌ Could not connect to Flask server (http://localhost:5000)")
        print("Make sure the Flask server is running")
    except Exception as e:
        print(f"❌ Error testing search: {e}")

if __name__ == "__main__":
    test_search()
