#!/usr/bin/env python3
"""
Final comprehensive test for the three specific problematic routes
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_routes_completely():
    """Test all the routes and their functionality"""
    try:
        from app import create_app
        
        app = create_app()
        
        with app.test_client() as client:
            print("🧪 COMPREHENSIVE ROUTE TESTING")
            print("=" * 60)
            
            test_cases = [
                {
                    'name': 'TradingView Base Route',
                    'url': '/analysis/tradingview',
                    'expected_content': ['TradingView', 'Charts', 'tradingview_main_widget'],
                    'should_contain_symbol': False
                },
                {
                    'name': 'TradingView with Symbol',
                    'url': '/analysis/tradingview?symbol=AAPL',
                    'expected_content': ['TradingView', 'Charts', 'AAPL'],
                    'should_contain_symbol': True,
                    'symbol': 'AAPL'
                },
                {
                    'name': 'Warren Buffett Base Route',
                    'url': '/analysis/warren-buffett',
                    'expected_content': ['Warren Buffett', 'oslo_stocks', 'global_stocks'],
                    'should_contain_symbol': False
                },
                {
                    'name': 'Warren Buffett with Ticker TEL.OL',
                    'url': '/analysis/warren-buffett?ticker=TEL.OL',
                    'expected_content': ['Warren Buffett', 'TEL.OL', 'analysis'],
                    'should_contain_symbol': True,
                    'symbol': 'TEL.OL'
                },
                {
                    'name': 'Warren Buffett with Ticker AAPL',
                    'url': '/analysis/warren-buffett?ticker=AAPL',
                    'expected_content': ['Warren Buffett', 'AAPL', 'analysis'],
                    'should_contain_symbol': True,
                    'symbol': 'AAPL'
                },
                {
                    'name': 'Sentiment Base Route',
                    'url': '/analysis/sentiment',
                    'expected_content': ['sentiment', 'popular_stocks'],
                    'should_contain_symbol': False
                },
                {
                    'name': 'Sentiment with Symbol FLNG.OL',
                    'url': '/analysis/sentiment?symbol=FLNG.OL',
                    'expected_content': ['sentiment', 'FLNG.OL'],
                    'should_contain_symbol': True,
                    'symbol': 'FLNG.OL'
                },
                {
                    'name': 'Sentiment with Symbol EQNR.OL',
                    'url': '/analysis/sentiment?symbol=EQNR.OL',
                    'expected_content': ['sentiment', 'EQNR.OL'],
                    'should_contain_symbol': True,
                    'symbol': 'EQNR.OL'
                },
                # Additional routes
                {
                    'name': 'Options Screener',
                    'url': '/analysis/options-screener',
                    'expected_content': ['Options', 'options_data'],
                    'should_contain_symbol': False
                },
                {
                    'name': 'Dividend Calendar',
                    'url': '/analysis/dividend-calendar',
                    'expected_content': ['Utbyttekalender', 'dividend_events'],
                    'should_contain_symbol': False
                },
                {
                    'name': 'Earnings Calendar',
                    'url': '/analysis/earnings-calendar',
                    'expected_content': ['Resultatkalender', 'earnings_events'],
                    'should_contain_symbol': False
                }
            ]
            
            passed_tests = 0
            total_tests = len(test_cases)
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n{i}. Testing: {test_case['name']}")
                print(f"   URL: {test_case['url']}")
                
                try:
                    response = client.get(test_case['url'])
                    print(f"   Status Code: {response.status_code}")
                    
                    if response.status_code == 200:
                        html_content = response.get_data(as_text=True)
                        
                        # Check for expected content
                        content_checks = []
                        for expected in test_case['expected_content']:
                            found = expected.lower() in html_content.lower()
                            content_checks.append(found)
                            print(f"   ✅ Contains '{expected}': {'Yes' if found else 'No'}")
                        
                        # Check for symbol if expected
                        if test_case['should_contain_symbol']:
                            symbol = test_case['symbol']
                            symbol_found = symbol in html_content
                            content_checks.append(symbol_found)
                            print(f"   ✅ Contains symbol '{symbol}': {'Yes' if symbol_found else 'No'}")
                        
                        # Check for 500 error indicators
                        error_indicators = ['500', 'Internal Server Error', 'Exception', 'Traceback']
                        has_errors = any(indicator in html_content for indicator in error_indicators)
                        
                        if has_errors:
                            print(f"   ❌ Contains error indicators")
                        else:
                            print(f"   ✅ No error indicators found")
                        
                        # Overall test result
                        test_passed = all(content_checks) and not has_errors and response.status_code == 200
                        
                        if test_passed:
                            print(f"   🎉 TEST PASSED")
                            passed_tests += 1
                        else:
                            print(f"   ❌ TEST FAILED")
                            
                    elif response.status_code == 500:
                        print(f"   ❌ 500 ERROR - Route crashed")
                        html_content = response.get_data(as_text=True)
                        if 'Exception' in html_content:
                            lines = html_content.split('\n')
                            for line in lines:
                                if 'Exception' in line or 'Error' in line:
                                    print(f"   Error: {line.strip()}")
                                    break
                    else:
                        print(f"   ❌ HTTP ERROR - Status {response.status_code}")
                        
                except Exception as e:
                    print(f"   ❌ EXCEPTION: {str(e)}")
                
                print("-" * 50)
            
            # Final results
            print(f"\n🏆 FINAL RESULTS")
            print("=" * 60)
            print(f"Passed: {passed_tests}/{total_tests}")
            print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
            
            if passed_tests == total_tests:
                print("🎉 ALL TESTS PASSED! All routes are working correctly.")
            else:
                failed_tests = total_tests - passed_tests
                print(f"⚠️ {failed_tests} tests failed. Please review the issues above.")
            
            return passed_tests == total_tests
            
    except Exception as e:
        print(f"❌ Critical error in testing: {e}")
        return False

def main():
    """Run comprehensive testing"""
    print("🚀 FINAL ROUTE VERIFICATION")
    print("Testing all problematic routes reported by user")
    print()
    
    success = test_routes_completely()
    
    if success:
        print("\n✅ SUCCESS: All reported issues have been resolved!")
    else:
        print("\n⚠️ Some issues remain. Please check the test output above.")

if __name__ == '__main__':
    main()
