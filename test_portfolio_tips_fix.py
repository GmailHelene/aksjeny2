import sys
import os

# Add current directory to path
sys.path.insert(0, '.')

try:
    from app import create_app
    from flask import url_for
    
    app = create_app()
    
    with app.app_context():
        with app.test_request_context():
            # Test if the portfolio.stock_tips endpoint exists
            try:
                url = url_for('portfolio.stock_tips')
                print(f'✅ portfolio.stock_tips works: {url}')
            except Exception as e:
                print(f'❌ portfolio.stock_tips failed: {e}')
            
            # Test if the old portfolio.tips endpoint fails as expected
            try:
                url = url_for('portfolio.tips')
                print(f'⚠️ portfolio.tips unexpectedly works: {url}')
            except Exception as e:
                print(f'✅ portfolio.tips correctly fails: {e}')
                
except Exception as e:
    print(f'❌ App startup failed: {e}')
