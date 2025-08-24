import requests
import json

base_url = 'https://aksjeradar.app'

# Test the different watchlist endpoints
endpoints_to_test = [
    '/api/watchlist/add',
    '/watchlist/add', 
    '/watchlist/api/watchlist/add'
]

print("Testing watchlist endpoints...")

for endpoint in endpoints_to_test:
    try:
        url = base_url + endpoint
        # Test with a simple GET first to see if endpoint exists
        response = requests.get(url, timeout=10)
        print(f'{endpoint}: GET Status {response.status_code}')
        
        # If GET works or returns 405 (method not allowed), try POST
        if response.status_code in [200, 405, 401, 403]:
            try:
                post_data = {'symbol': 'TSLA'}
                post_response = requests.post(url, 
                    json=post_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                print(f'{endpoint}: POST Status {post_response.status_code}')
                if post_response.status_code < 500:
                    try:
                        data = post_response.json()
                        print(f'{endpoint}: Response: {data}')
                    except:
                        print(f'{endpoint}: Response: {post_response.text[:200]}')
            except Exception as e:
                print(f'{endpoint}: POST Error - {e}')
                
    except Exception as e:
        print(f'{endpoint}: GET Error - {e}')

print("\nDone testing endpoints.")
