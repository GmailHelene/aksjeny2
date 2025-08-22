import sys
import os
sys.path.append('.')

from app import create_app
from flask import url_for

def test_analysis_routes():
    app = create_app()
    
    with app.app_context():
        # Test that all the new routes exist
        new_routes = [
            'analysis.portfolio_tips',
            'analysis.risk_analysis', 
            'analysis.peer_comparison',
            'analysis.options_screener',
            'analysis.dividend_calendar',
            'analysis.earnings_calendar'
        ]
        
        print("Testing analysis routes:")
        for route_name in new_routes:
            try:
                url = url_for(route_name)
                print(f"✓ {route_name} -> {url}")
            except Exception as e:
                print(f"✗ {route_name} -> ERROR: {e}")
        
        # List all analysis routes
        analysis_routes = []
        for rule in app.url_map.iter_rules():
            if 'analysis' in str(rule):
                analysis_routes.append(str(rule))
        
        print("\nAll analysis routes found:")
        for route in sorted(analysis_routes):
            print(f"  {route}")

if __name__ == '__main__':
    test_analysis_routes()
