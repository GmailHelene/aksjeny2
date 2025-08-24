#!/usr/bin/env python3
"""
Simple test to verify the BuildError is fixed
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_stocks_index_route():
    """Test that stocks.index route exists"""
    try:
        from app.routes.stocks import stocks
        
        # Check if the index route is registered
        rules = []
        for rule in stocks.url_map.iter_rules():
            if rule.endpoint == 'stocks.index':
                rules.append(rule)
                
        if rules:
            print(f"✅ SUCCESS: stocks.index route found: {rules}")
            return True
        else:
            print("❌ FAILED: stocks.index route not found")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Error testing route: {e}")
        return False

def test_url_for_stocks_index():
    """Test that url_for('stocks.index') works"""
    try:
        from flask import Flask
        from app.routes.stocks import stocks
        
        app = Flask(__name__)
        app.register_blueprint(stocks)
        
        with app.app_context():
            from flask import url_for
            url = url_for('stocks.index')
            print(f"✅ SUCCESS: url_for('stocks.index') = {url}")
            return True
            
    except Exception as e:
        print(f"❌ FAILED: url_for test failed: {e}")
        return False

if __name__ == '__main__':
    print("Testing BuildError fix...")
    print("=" * 50)
    
    success1 = test_stocks_index_route()
    success2 = test_url_for_stocks_index()
    
    print("=" * 50)
    if success1 and success2:
        print("🎉 BuildError is FIXED! stocks.index route is working!")
        sys.exit(0)
    else:
        print("💥 BuildError still exists!")
        sys.exit(1)
