#!/usr/bin/env python3
"""
Test script for Warren Buffett analysis route
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_warren_buffett_route():
    """Test Warren Buffett analysis route"""
    base_url = "http://localhost:5002"
    
    # Test cases
    test_cases = [
        # Just the base page
        f"{base_url}/analysis/warren-buffett",
        # With Oslo ticker
        f"{base_url}/analysis/warren-buffett?ticker=EQNR.OL",
        # With US ticker  
        f"{base_url}/analysis/warren-buffett?ticker=AAPL",
    ]
    
    for url in test_cases:
        logger.info(f"Testing: {url}")
        try:
            response = requests.get(url)
            logger.info(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                logger.info("✅ SUCCESS - Page loads correctly")
                
                # Check for expected content
                content = response.text.lower()
                if 'warren buffett' in content:
                    logger.info("✅ Page contains expected content")
                else:
                    logger.warning("⚠️ Page might be missing expected content")
                    
            elif response.status_code == 500:
                logger.error("❌ INTERNAL SERVER ERROR - Check server logs")
            elif response.status_code == 404:
                logger.error("❌ PAGE NOT FOUND")
            else:
                logger.warning(f"⚠️ Unexpected status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            logger.error("❌ CONNECTION ERROR - Is the server running?")
        except Exception as e:
            logger.error(f"❌ ERROR: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_warren_buffett_route()
