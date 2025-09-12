import requests
import sys
import pytest

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

        # Assertion moved inside try
        assert response.status_code in (200,302), f"Unexpected status {response.status_code}"
    except requests.exceptions.ConnectionError as e:
        pytest.skip(f"Server not running for profile route test: {e}")
    except Exception as e:
        print(f"Error testing profile route: {e}")
        pytest.fail(f"Exception testing profile route: {e}")

if __name__ == "__main__":
    print("Testing profile route...")
    try:
        test_profile_route()
        print("Test succeeded")
        sys.exit(0)
    except AssertionError:
        print("Test failed")
        sys.exit(1)
