#!/usr/bin/env python3
"""
Quick test of critical routes after access control fixes
"""

import sys
import os
sys.path.append('.')

try:
    from app import create_app
    print("✅ App import successful")
    
    app = create_app()
    print("✅ App creation successful")

    with app.test_client() as client:
        print('\n🔧 Testing critical routes after access control fixes...\n')
        
        routes = [
            ('/profile', 'Profile page'),
            ('/forum/search', 'Forum search'),  
            ('/analysis/sentiment', 'Sentiment analysis'),
            ('/watchlist', 'Watchlist redirect'),
            ('/advanced/crypto-dashboard', 'Crypto dashboard'),
            ('/stocks/compare', 'Stock comparison'),
            ('/analysis/warren-buffett?ticker=AAPL', 'Warren Buffett analysis'),
            ('/advanced-features/crypto-dashboard', 'Advanced crypto dashboard')
        ]
        
        results = []
        
        for route, name in routes:
            try:
                response = client.get(route)
                status = response.status_code
                
                if status == 200:
                    print(f'✅ {name}: OK ({status})')
                    results.append(f'✅ {route} - OK')
                elif status == 302:
                    print(f'🔄 {name}: Redirect ({status})')
                    results.append(f'🔄 {route} - Redirect')
                elif status == 401:
                    print(f'🔐 {name}: Unauthorized ({status})')
                    results.append(f'🔐 {route} - Needs login')
                elif status == 404:
                    print(f'❓ {name}: Not found ({status})')
                    results.append(f'❓ {route} - Not found')
                elif status == 500:
                    print(f'❌ {name}: Internal error ({status})')
                    results.append(f'❌ {route} - 500 ERROR')
                else:
                    print(f'⚠️ {name}: Other error ({status})')
                    results.append(f'⚠️ {route} - Error {status}')
                    
            except Exception as e:
                print(f'💥 {name}: Exception - {e}')
                results.append(f'💥 {route} - Exception')
        
        print('\n📊 SUMMARY:')
        print('=' * 50)
        for result in results:
            print(result)
        
        # Count results
        ok_count = len([r for r in results if '✅' in r])
        redirect_count = len([r for r in results if '🔄' in r])
        error_count = len([r for r in results if '❌' in r or '💥' in r])
        
        print(f'\n✅ OK: {ok_count}')
        print(f'🔄 Redirects: {redirect_count}')
        print(f'❌ Errors: {error_count}')
        
        if error_count == 0:
            print('\n🎉 ALL ROUTES WORKING!')
        else:
            print(f'\n⚠️ {error_count} routes still have issues')

except Exception as e:
    print(f"❌ Failed to run test: {e}")
    import traceback
    traceback.print_exc()
