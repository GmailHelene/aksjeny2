#!/usr/bin/env python3
"""
Test sentiment route to identify the 500 error
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app import create_app
    
    # Create Flask app
    app = create_app()
    
    # Test the sentiment route directly
    with app.test_client() as client:
        print("Testing sentiment route...")
        
        # Test without parameters
        response = client.get('/analysis/sentiment')
        print(f"Response status (no params): {response.status_code}")
        if response.status_code != 200:
            print(f"Response data: {response.get_data(as_text=True)[:500]}")
        
        # Test with DNB parameter
        response = client.get('/analysis/sentiment?symbol=DNB.OL')
        print(f"Response status (DNB.OL): {response.status_code}")
        if response.status_code != 200:
            print(f"Response data: {response.get_data(as_text=True)[:500]}")
        else:
            print("✓ Sentiment route working correctly!")
            
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error testing sentiment route: {e}")
    import traceback
    traceback.print_exc()
