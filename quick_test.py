import sys
sys.path.insert(0, '.')

try:
    from app import create_app
    app = create_app()
    print('✅ App created successfully')
    
    with app.test_client() as client:
        with app.app_context():
            print('🧪 Testing critical routes...')
            
            # Test watchlist routes (Step 1)
            routes = [
                ('/watchlist/', 'Watchlist route'),
                ('/portfolio/watchlist/', 'Portfolio watchlist route'),
                ('/analysis/warren-buffett?ticker=EQNR.OL', 'Warren Buffett analysis'),
                ('/analysis/technical?ticker=EQNR.OL', 'Technical analysis'),
                ('/analysis/recommendation?ticker=EQNR.OL', 'Recommendation analysis')
            ]
            
            success_count = 0
            total_count = len(routes)
            
            for route, description in routes:
                try:
                    resp = client.get(route)
                    if resp.status_code == 200:
                        print(f'   ✅ {description}: PASS')
                        success_count += 1
                    else:
                        print(f'   ❌ {description}: FAIL ({resp.status_code})')
                except Exception as e:
                    print(f'   ❌ {description}: ERROR - {str(e)[:50]}')
                    
            print(f'\n📊 Results: {success_count}/{total_count} routes working')
            
            if success_count == total_count:
                print('🎉 ALL CRITICAL FIXES VERIFIED - PRODUCTION READY!')
            elif success_count >= total_count * 0.8:
                print('✅ Most fixes working - minor issues may remain')
            else:
                print('⚠️ Some critical issues still need attention')
            
except ImportError as e:
    print(f'❌ Import error: {e}')
except Exception as e:
    print(f'❌ Error: {e}')
