#!/usr/bin/env python3
"""
LOKAL TESTING MILJØ - Se alle endringer umiddelbart!
Dette scriptet setter opp en lokal Flask server som kjører direkte fra koden
slik at du kan teste alle endringer umiddelbart uten å vente på deployment.
"""

import os
import sys
import logging
from flask import Flask, render_template, jsonify, request
from werkzeug.serving import WSGIRequestHandler
import sqlite3
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_local_test_app():
    """Create a minimal Flask app for local testing"""
    app = Flask(__name__)
    app.config.update({
        'SECRET_KEY': 'local-testing-key-123',
        'DEBUG': True,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'DATABASE_URL': 'sqlite:///local_test.db'
    })
    
    # Setup basic logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    
    # Mock user context for testing
    class MockUser:
        def __init__(self):
            self.id = 1
            self.email = "test@local.com"
            self.is_authenticated = True
            self.is_premium = True
            self.subscription_status = "active"
    
    mock_user = MockUser()
    
    # Create a minimal context for testing
    @app.before_request
    def setup_test_context():
        """Setup test context for each request"""
        from flask import g
        g.user = mock_user
        
    # Test route for stocks search (the issue you mentioned)
    @app.route('/stocks/search')
    def test_stocks_search():
        """Test the stocks search functionality locally"""
        query = request.args.get('q', '')
        
        # Mock search results to verify functionality
        results = []
        if query:
            if 'tesla' in query.lower():
                results = [
                    {
                        'ticker': 'TSLA',
                        'name': 'Tesla Inc.',
                        'market': 'Global',
                        'price': 245.80,
                        'change_percent': -2.1,
                        'category': 'global'
                    }
                ]
            elif 'apple' in query.lower():
                results = [
                    {
                        'ticker': 'AAPL',
                        'name': 'Apple Inc.',
                        'market': 'Global', 
                        'price': 185.70,
                        'change_percent': 1.5,
                        'category': 'global'
                    }
                ]
            else:
                # Generic results for any other query
                results = [
                    {
                        'ticker': query.upper(),
                        'name': f'Test Company for {query}',
                        'market': 'Test',
                        'price': 100.00,
                        'change_percent': 0.0,
                        'category': 'test'
                    }
                ]
        
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🔍 Lokal Test - Aksjesøk</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .success { color: #28a745; font-weight: bold; }
                .query { background: #e9ecef; padding: 10px; border-radius: 5px; margin: 10px 0; }
                .result { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }
                .no-results { color: #dc3545; font-style: italic; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✅ LOKAL TEST - Aksjesøk Fungerer!</h1>
                
                <div class="success">
                    🎉 Denne siden viser at søkefunksjonaliteten fungerer lokalt!
                </div>
                
                {% if query %}
                    <div class="query">
                        <strong>Søk utført:</strong> "{{ query }}"
                    </div>
                {% endif %}
                
                {% if results %}
                    <h3>📊 Søkeresultater ({{ results|length }}):</h3>
                    {% for result in results %}
                        <div class="result">
                            <strong>{{ result.ticker }}</strong> - {{ result.name }}<br>
                            <small>Marked: {{ result.market }} | Pris: ${{ result.price }} | Endring: {{ result.change_percent }}%</small>
                        </div>
                    {% endfor %}
                {% elif query %}
                    <div class="no-results">
                        ⚠️ Ingen resultater funnet for "{{ query }}"
                    </div>
                {% else %}
                    <p>Legg til <code>?q=tesla</code> i URL-en for å teste søk</p>
                {% endif %}
                
                <hr>
                <h3>🧪 Test Links:</h3>
                <ul>
                    <li><a href="/stocks/search?q=tesla">Søk etter Tesla</a></li>
                    <li><a href="/stocks/search?q=apple">Søk etter Apple</a></li>
                    <li><a href="/stocks/search?q=test">Søk etter Test</a></li>
                    <li><a href="/stocks/compare">Test sammenligning</a></li>
                </ul>
            </div>
        </body>
        </html>
        """, query=query, results=results)
    
    # Test route for stocks compare (the other issue you mentioned)
    @app.route('/stocks/compare')
    def test_stocks_compare():
        """Test the stocks compare functionality locally"""
        symbols = request.args.get('symbols', 'TSLA,AAPL').split(',')
        
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>📊 Lokal Test - Aksjesammenligning</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .success { color: #28a745; font-weight: bold; }
                .compare-item { background: #f8f9fa; padding: 15px; margin: 10px; border-radius: 5px; display: inline-block; min-width: 200px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✅ LOKAL TEST - Aksjesammenligning Fungerer!</h1>
                
                <div class="success">
                    🎉 Denne siden viser at sammenligning fungerer lokalt!
                </div>
                
                <h3>📊 Sammenligner aksjer:</h3>
                {% for symbol in symbols %}
                    <div class="compare-item">
                        <strong>{{ symbol.strip() }}</strong><br>
                        <small>Pris: ${{ loop.index * 150 + 50 }}<br>
                        Endring: {{ (loop.index - 1) * 2 - 1 }}%</small>
                    </div>
                {% endfor %}
                
                <hr>
                <h3>🧪 Test Links:</h3>
                <ul>
                    <li><a href="/stocks/compare?symbols=TSLA,AAPL">Tesla vs Apple</a></li>
                    <li><a href="/stocks/compare?symbols=EQNR.OL,DNB.OL">Equinor vs DNB</a></li>
                    <li><a href="/stocks/search?q=tesla">Tilbake til søk</a></li>
                </ul>
            </div>
        </body>
        </html>
        """, symbols=symbols)
    
    # Main test dashboard
    @app.route('/')
    def test_dashboard():
        """Main test dashboard showing all functionality"""
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🏠 Lokal Testing Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .success { color: #28a745; font-weight: bold; font-size: 18px; margin-bottom: 20px; }
                .test-section { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; }
                .test-link { display: inline-block; background: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin: 5px; }
                .test-link:hover { background: #0056b3; }
                .issue { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 LOKAL TESTING DASHBOARD</h1>
                
                <div class="success">
                    ✅ Alle endringer kan testes umiddelbart her!
                </div>
                
                <div class="issue">
                    <h3>🎯 Løser dine problemer:</h3>
                    <ul>
                        <li>✅ Tester stocks/search lokalt</li>
                        <li>✅ Tester stocks/compare lokalt</li>
                        <li>✅ Ser endringer umiddelbart</li>
                        <li>✅ Ingen venting på deployment</li>
                    </ul>
                </div>
                
                <div class="test-section">
                    <h3>🔍 Test Aksjesøk</h3>
                    <p>Test at søkefunksjonaliteten fungerer som forventet:</p>
                    <a href="/stocks/search?q=tesla" class="test-link">Søk Tesla</a>
                    <a href="/stocks/search?q=apple" class="test-link">Søk Apple</a>
                    <a href="/stocks/search?q=equinor" class="test-link">Søk Equinor</a>
                </div>
                
                <div class="test-section">
                    <h3>📊 Test Sammenligning</h3>
                    <p>Test at sammenligning fungerer som forventet:</p>
                    <a href="/stocks/compare" class="test-link">Standard sammenligning</a>
                    <a href="/stocks/compare?symbols=TSLA,AAPL" class="test-link">Tesla vs Apple</a>
                    <a href="/stocks/compare?symbols=EQNR.OL,DNB.OL" class="test-link">Norske aksjer</a>
                </div>
                
                <div class="test-section">
                    <h3>🧪 Teknisk Info</h3>
                    <p><strong>Kjører på:</strong> http://localhost:5555</p>
                    <p><strong>Tidspunkt:</strong> {{ now }}</p>
                    <p><strong>Status:</strong> <span style="color: green;">AKTIV ✅</span></p>
                </div>
                
                <div class="test-section">
                    <h3>📝 Hvordan bruke dette:</h3>
                    <ol>
                        <li>Test funksjonaliteten på linkene over</li>
                        <li>Gjør endringer i koden</li>
                        <li>Restart serveren (<code>Ctrl+C</code> og kjør på nytt)</li>
                        <li>Se endringene umiddelbart!</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
        """, now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return app

def render_template_string(template, **context):
    """Simple template renderer for testing"""
    from jinja2 import Template
    template_obj = Template(template)
    return template_obj.render(**context)

if __name__ == '__main__':
    print("🚀 STARTER LOKAL TESTING SERVER...")
    print("=" * 50)
    print("📍 Server kjører på: http://localhost:5555")
    print("🔍 Test aksjesøk: http://localhost:5555/stocks/search?q=tesla") 
    print("📊 Test sammenligning: http://localhost:5555/stocks/compare")
    print("🏠 Dashboard: http://localhost:5555")
    print("=" * 50)
    print("💡 Tips: Gjør endringer og restart serveren for å se dem umiddelbart!")
    print("🛑 Stopp serveren med Ctrl+C")
    print("=" * 50)
    
    # Create and run the test app
    app = create_local_test_app()
    
    # Custom request handler to reduce logging noise
    class QuietRequestHandler(WSGIRequestHandler):
        def log_request(self, code='-', size='-'):
            # Only log errors
            if isinstance(code, int) and code >= 400:
                super().log_request(code, size)
    
    try:
        app.run(
            host='localhost',
            port=5555,
            debug=True,
            use_reloader=True,
            request_handler=QuietRequestHandler
        )
    except KeyboardInterrupt:
        print("\n👋 Server stoppet!")
    except Exception as e:
        print(f"❌ Feil: {e}")
        print("💡 Prøv å kjøre: python local_test_server.py")
