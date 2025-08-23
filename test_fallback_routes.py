#!/usr/bin/env python3
"""
Quick test script for fallback routes to verify they don't cause 500 errors.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_route_status():
    """Test that critical routes return non-500 status codes."""
    app = create_app()
    
    # Routes to test - all the problematic ones mentioned by user
    test_routes = [
        '/profile',
        '/watchlist', 
        '/analysis',
        '/forum',
        '/sentiment-analysis',
        '/crypto-dashboard',
        '/norsk-intel',
        '/advanced',
        '/comparison'
    ]
    
    successful_routes = []
    failed_routes = []
    
    with app.test_client() as client:
        logger.info("Testing fallback routes...")
        
        for route in test_routes:
            try:
                response = client.get(route)
                status_code = response.status_code
                
                if status_code < 500:
                    successful_routes.append((route, status_code))
                    logger.info(f"✅ {route}: {status_code}")
                else:
                    failed_routes.append((route, status_code))
                    logger.error(f"❌ {route}: {status_code}")
                    
            except Exception as e:
                failed_routes.append((route, f"Exception: {e}"))
                logger.error(f"❌ {route}: Exception - {e}")
    
    # Test the API route too
    try:
        with app.test_client() as client:
            response = client.post('/api/watchlist/add', 
                                 json={'symbol': 'AAPL'},
                                 headers={'Content-Type': 'application/json'})
            status_code = response.status_code
            
            if status_code < 500:
                successful_routes.append(('/api/watchlist/add', status_code))
                logger.info(f"✅ /api/watchlist/add: {status_code}")
            else:
                failed_routes.append(('/api/watchlist/add', status_code))
                logger.error(f"❌ /api/watchlist/add: {status_code}")
                
    except Exception as e:
        failed_routes.append(('/api/watchlist/add', f"Exception: {e}"))
        logger.error(f"❌ /api/watchlist/add: Exception - {e}")
    
    print("\n" + "="*50)
    print("FALLBACK ROUTES TEST SUMMARY")
    print("="*50)
    
    print(f"\n✅ SUCCESSFUL ROUTES ({len(successful_routes)}):")
    for route, status in successful_routes:
        print(f"   {route}: {status}")
    
    if failed_routes:
        print(f"\n❌ FAILED ROUTES ({len(failed_routes)}):")
        for route, status in failed_routes:
            print(f"   {route}: {status}")
    else:
        print(f"\n🎉 ALL ROUTES WORKING! No 500 errors detected.")
    
    print(f"\nTotal routes tested: {len(test_routes) + 1}")
    print(f"Success rate: {len(successful_routes)}/{len(test_routes) + 1} ({100*len(successful_routes)/(len(test_routes) + 1):.1f}%)")
    
    return len(failed_routes) == 0

if __name__ == "__main__":
    success = test_route_status()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
