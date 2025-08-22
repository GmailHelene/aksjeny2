#!/usr/bin/env python3
import requests
import json

def test_portfolio_add_endpoint():
    """Test the portfolio add endpoint to see what's causing the hang"""
    
    url = 'https://aksjeradar.trade/portfolio/add'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    data = {
        'ticker': 'AAPL', 
        'quantity': 1,
        'purchase_price': 100
    }

    try:
        print("Testing portfolio add endpoint...")
        response = requests.post(url, headers=headers, data=data, allow_redirects=False, timeout=10)
        print(f'Status Code: {response.status_code}')
        print(f'Headers: {dict(response.headers)}')
        print(f'Content: {response.text[:1000]}')
        
        # Check if it's a redirect
        if response.status_code in [301, 302, 303, 307, 308]:
            print(f'Redirect to: {response.headers.get("Location", "Unknown")}')
            
    except requests.exceptions.Timeout:
        print("REQUEST TIMED OUT - This explains the infinite loading!")
    except Exception as e:
        print(f'Error: {e}')

def test_portfolio_add_authenticated():
    """Test with authentication simulation"""
    
    # First try to get a session
    session = requests.Session()
    
    # Try to visit the site first
    try:
        homepage = session.get('https://aksjeradar.trade/', timeout=10)
        print(f"Homepage status: {homepage.status_code}")
        
        # Extract CSRF token if available
        csrf_token = None
        if 'csrf-token' in homepage.text:
            import re
            match = re.search(r'name="csrf-token"\s+content="([^"]+)"', homepage.text)
            if match:
                csrf_token = match.group(1)
                print(f"Found CSRF token: {csrf_token[:20]}...")
        
        # Now test portfolio add with session
        url = 'https://aksjeradar.trade/portfolio/add'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://aksjeradar.trade/'
        }
        
        data = {
            'ticker': 'AAPL', 
            'quantity': 1,
            'purchase_price': 100
        }
        
        if csrf_token:
            data['csrf_token'] = csrf_token
            headers['X-CSRFToken'] = csrf_token
        
        print("\nTesting with session and CSRF...")
        response = session.post(url, headers=headers, data=data, allow_redirects=False, timeout=10)
        print(f'Status Code: {response.status_code}')
        print(f'Headers: {dict(response.headers)}')
        print(f'Content: {response.text[:1000]}')
        
        if response.status_code in [301, 302, 303, 307, 308]:
            print(f'Redirect to: {response.headers.get("Location", "Unknown")}')
            
    except requests.exceptions.Timeout:
        print("REQUEST TIMED OUT WITH SESSION - Confirms infinite loading issue!")
    except Exception as e:
        print(f'Session test error: {e}')

if __name__ == "__main__":
    test_portfolio_add_endpoint()
    print("\n" + "="*50 + "\n")
    test_portfolio_add_authenticated()
