#!/usr/bin/env python3
"""
Quick inline test for critical Flask routes
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_routes():
    """Test critical routes"""
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.test_client() as client:
            # Test sentiment analysis
            print('Testing sentiment analysis...')
            response = client.get('/analysis/sentiment?symbol=DNB.OL')
            print(f'Sentiment: {response.status_code}')
            
            # Test stocks compare  
            print('Testing stocks compare...')
            response = client.get('/stocks/compare?symbols=DNB.OL,EQNR.OL')
            print(f'Compare: {response.status_code}')
            
            # Test stock details
            print('Testing stock details...')
            response = client.get('/stocks/DNB.OL')
            print(f'Details: {response.status_code}')
            
            # Test chart API
            print('Testing chart API...')
            response = client.get('/stocks/api/demo/chart-data/DNB.OL')
            print(f'Chart API: {response.status_code}')
            
            print('All tests completed')
            
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_routes()
