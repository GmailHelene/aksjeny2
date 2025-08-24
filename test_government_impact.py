#!/usr/bin/env python3

from app import create_app

def test_government_impact():
    """Test government impact route"""
    app = create_app()
    
    with app.test_client() as client:
        # Test government impact route
        response = client.get('/norwegian-intel/government-impact')
        print(f'Government Impact Status: {response.status_code}')
        if response.status_code != 200:
            print(f'Error: {response.data.decode()}')
        else:
            print('Government Impact route working ✅')
            
        # Test redirect route
        response2 = client.get('/norwegian-intel/government-impact', follow_redirects=True)
        print(f'Redirect Status: {response2.status_code}')

if __name__ == '__main__':
    test_government_impact()
