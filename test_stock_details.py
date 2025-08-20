#!/usr/bin/env python3
"""
Test script to check stock details route
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import url_for

def test_stock_details():
    app = create_app()
    with app.test_client() as client:
        # Test stock details route
        response = client.get('/stocks/details/TSLA')
        print(f'Status Code: {response.status_code}')
        
        if response.status_code >= 400:
            print(f'Error Response: {response.data.decode()[:500]}')
            return False
        elif response.status_code == 302:
            print(f'Redirect Location: {response.location}')
            return False
        else:
            print('Request successful!')
            return True

if __name__ == '__main__':
    test_stock_details()
