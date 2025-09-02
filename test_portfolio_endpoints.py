from flask import Flask, url_for
from app.routes.portfolio import portfolio_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.register_blueprint(portfolio_bp, url_prefix='/portfolio')

with app.app_context():
    try:
        url = url_for('portfolio.portfolio_overview')
        print(f'✅ SUCCESS: portfolio.portfolio_overview endpoint exists: {url}')
    except Exception as e:
        print(f'❌ ERROR: {e}')
        
    try:
        url = url_for('portfolio.index')
        print(f'❌ UNEXPECTED: portfolio.index still exists: {url}')
    except Exception as e:
        print(f'✅ SUCCESS: portfolio.index no longer exists (expected): {e}')
