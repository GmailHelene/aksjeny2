import requests
import sys

def test_profile_route():
    """Test the profile route to check if it's working properly"""
    try:
        # Make a request to the profile route
        response = requests.get('http://localhost:5002/profile')
        
        # Print the results
        print(f"Status code: {response.status_code}")
        print(f"Location header: {response.headers.get('Location', 'None')}")
        
        if response.status_code == 200:
            print("Profile page loaded successfully!")
            print(f"Content preview: {response.text[:200]}...")
        elif response.status_code == 302:
            print(f"Redirected to: {response.headers.get('Location', 'unknown')}")
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(f"Response text: {response.text[:200]}...")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing profile route: {e}")
        return False

if __name__ == "__main__":
    print("Testing profile route...")
    success = test_profile_route()
    print(f"Test {'succeeded' if success else 'failed'}")
    sys.exit(0 if success else 1)
