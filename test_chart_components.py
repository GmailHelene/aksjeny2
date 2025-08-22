#!/usr/bin/env python3
"""
Test chart components in technical analysis page
"""

import sys
sys.path.insert(0, '.')

from app import create_app

def test_chart_components():
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            print('🔍 Testing technical analysis page chart components...')
            response = client.get('/analysis/technical?ticker=EQNR.OL')
            print(f'Status: {response.status_code}')
            
            if response.status_code == 200:
                html = response.get_data(as_text=True)
                
                # Check for chart elements
                chart_checks = {
                    'TradingView widget container': 'tradingview_widget' in html,
                    'Chart.js fallback canvas': 'id="technicalChart"' in html,
                    'Fallback container div': 'id="chartjs-fallback"' in html,
                    'TradingView script': 'TradingView.widget' in html,
                    'Chart fallback function': 'showTradingViewFallback' in html,
                    'generateFallbackChartData function': 'generateFallbackChartData' in html,
                    'Technical indicators section': 'Tekniske indikatorer' in html,
                    'RSI indicator': 'RSI' in html,
                    'MACD indicator': 'MACD' in html,
                    'Chart.js initialization': 'new Chart(canvas' in html,
                    'Canvas display styling': 'style="display: none"' in html,
                    'Bootstrap classes': 'class="container' in html
                }
                
                print('\n📊 Chart component verification:')
                print('=' * 60)
                
                all_passed = True
                for check, passed in chart_checks.items():
                    status = '✅' if passed else '❌'
                    print(f'{status} {check}')
                    if not passed:
                        all_passed = False
                
                print('=' * 60)
                
                if all_passed:
                    print('🎉 All chart components are present and properly configured!')
                else:
                    print('⚠️ Some chart components may be missing or misconfigured')
                
                # Check for potential missing components
                missing_components = []
                if 'Chart.js' not in html and 'chart.js' not in html:
                    missing_components.append('Chart.js library script')
                if 'TradingView' not in html:
                    missing_components.append('TradingView widget script')
                if 'canvas' not in html.lower():
                    missing_components.append('Canvas elements')
                
                if missing_components:
                    print('\n🔍 Potentially missing components:')
                    for component in missing_components:
                        print(f'   - {component}')
                else:
                    print('\n✨ No obviously missing components detected')
                
                print(f'\n✅ Technical analysis page loaded successfully')
                return True
            else:
                print(f'❌ Error loading technical analysis page: {response.status_code}')
                return False

if __name__ == "__main__":
    test_chart_components()
