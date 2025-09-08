import requests
import sys
import os
import logging
from pprint import pprint

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base URL for the local Flask server
BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, expected_status=200, headers=None):
    """Test an endpoint and return the result"""
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"Testing endpoint: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        
        if status_code == expected_status:
            logger.info(f"✅ Success: {endpoint} returned status {status_code}")
            return True, response
        else:
            logger.error(f"❌ Failed: {endpoint} returned status {status_code}, expected {expected_status}")
            return False, response
    except Exception as e:
        logger.error(f"❌ Error testing {endpoint}: {str(e)}")
        return False, None

def run_diagnostic_tests():
    """Run tests on the diagnostic endpoints"""
    logger.info("Running diagnostic tests...")
    
    # Test auth status endpoint
    success, response = test_endpoint("/diagnostic/auth-status")
    if success:
        try:
            # Try to parse as JSON
            data = response.json()
            logger.info("Auth status response:")
            pprint(data)
        except:
            # If not JSON, print the text content
            logger.info(f"Auth status response (text): {response.text[:500]}...")
    
    # Test access control endpoint
    success, response = test_endpoint("/test/access-control")
    if success:
        try:
            # Try to parse as JSON
            data = response.json()
            logger.info("Access control test response:")
            pprint(data)
        except:
            # If not JSON, print the text content
            logger.info(f"Access control test response (text): {response.text[:500]}...")

def test_with_simulated_auth():
    """Test endpoints with simulated auth headers"""
    logger.info("Testing with simulated auth headers...")
    
    # Create headers to simulate an authenticated user
    auth_headers = {
        'X-Test-Auth': 'true',
        'X-Test-User-Id': '123',
        'X-Test-User-Role': 'premium'
    }
    
    # Test portfolio endpoint with auth headers
    success, response = test_endpoint("/portfolio/", headers=auth_headers)
    if success:
        logger.info(f"Portfolio response with auth (text): {response.text[:500]}...")
    
    # Test profile endpoint with auth headers
    success, response = test_endpoint("/profile/", headers=auth_headers)
    if success:
        logger.info(f"Profile response with auth (text): {response.text[:500]}...")

def test_main_routes():
    """Test main routes to ensure they're accessible"""
    logger.info("Testing main routes...")
    
    routes = [
        "/",                    # Main index
        "/stocks/list/oslo",    # Oslo stocks
        "/stocks/list/global",  # Global stocks
        "/news/",               # News page
        "/analysis/"            # Analysis page
    ]
    
    for route in routes:
        success, response = test_endpoint(route)
        if success:
            logger.info(f"{route} accessible")

if __name__ == "__main__":
    logger.info("Starting comprehensive access control test...")
    
    # Run the tests
    test_main_routes()
    run_diagnostic_tests()
    test_with_simulated_auth()
    
    logger.info("Testing complete.")
