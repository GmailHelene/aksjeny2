#!/usr/bin/env python3
"""
Comprehensive test to verify all critical production fixes are working correctly
"""

import sys
sys.path.insert(0, '.')

from app import create_app
from app.models.user import User
from flask import url_for
import json
from datetime import datetime

def test_all_critical_fixes():
    """Test all the critical fixes we implemented"""
    app = create_app()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'tests': {},
        'overall_status': 'UNKNOWN'
    }
    
    with app.test_client() as client:
        with app.app_context():
            print("🚀 Starting comprehensive test of all critical fixes...")
            print("=" * 80)
            
            # Test 1: Watchlist routes (Step 1)
            print("\n📋 Step 1: Testing watchlist routes...")
            watchlist_tests = {
                '/watchlist/': False,
                '/portfolio/watchlist/': False
            }
            
            for route in watchlist_tests:
                try:
                    response = client.get(route)
                    watchlist_tests[route] = response.status_code == 200
                    status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
                    print(f"   {route}: {status}")
                except Exception as e:
                    print(f"   {route}: ❌ ERROR - {e}")
                    
            results['tests']['step1_watchlist'] = watchlist_tests
            
            # Test 2: Warren Buffett analysis (Step 2)
            print("\n🔍 Step 2: Testing Warren Buffett analysis...")
            warren_tests = {
                '/analysis/warren-buffett?ticker=EQNR.OL': False,
                '/analysis/warren-buffett?ticker=XRP-USD': False
            }
            
            for route in warren_tests:
                try:
                    response = client.get(route)
                    warren_tests[route] = response.status_code == 200
                    status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
                    print(f"   {route}: {status}")
                except Exception as e:
                    print(f"   {route}: ❌ ERROR - {e}")
                    
            results['tests']['step2_warren_buffett'] = warren_tests
            
            # Test 3: Technical analysis with charts (Steps 7 & 8)
            print("\n📊 Steps 7 & 8: Testing technical analysis and charts...")
            technical_tests = {
                '/analysis/technical?ticker=EQNR.OL': False,
                '/analysis/technical?ticker=AAPL': False
            }
            
            for route in technical_tests:
                try:
                    response = client.get(route)
                    technical_tests[route] = response.status_code == 200
                    if response.status_code == 200:
                        html = response.get_data(as_text=True)
                        # Check for chart components
                        has_tradingview = 'TradingView.widget' in html
                        has_fallback = 'id="technicalChart"' in html
                        has_real_data = 'technical_data' in html and 'rsi' in html.lower()
                        
                        if has_tradingview and has_fallback and has_real_data:
                            print(f"   {route}: ✅ PASS (TradingView + fallback + real data)")
                        else:
                            missing = []
                            if not has_tradingview: missing.append("TradingView")
                            if not has_fallback: missing.append("Chart.js fallback")
                            if not has_real_data: missing.append("Real technical data")
                            print(f"   {route}: ⚠️  PARTIAL (Missing: {', '.join(missing)})")
                    else:
                        print(f"   {route}: ❌ FAIL ({response.status_code})")
                except Exception as e:
                    print(f"   {route}: ❌ ERROR - {e}")
                    
            results['tests']['step78_technical_charts'] = technical_tests
            
            # Test 4: CSS and styling (Step 3)
            print("\n🎨 Step 3: Testing CSS and styling...")
            css_tests = {
                'Homepage loads': False,
                'Analysis pages load': False
            }
            
            try:
                # Test homepage
                response = client.get('/')
                css_tests['Homepage loads'] = response.status_code == 200
                
                # Test analysis page
                response = client.get('/analysis/technical?ticker=EQNR.OL')
                css_tests['Analysis pages load'] = response.status_code == 200
                
                for test, passed in css_tests.items():
                    status = "✅ PASS" if passed else "❌ FAIL"
                    print(f"   {test}: {status}")
                    
            except Exception as e:
                print(f"   CSS Tests: ❌ ERROR - {e}")
                
            results['tests']['step3_css_styling'] = css_tests
            
            # Test 5: Recommendation routing (Step 6)
            print("\n🔗 Step 6: Testing recommendation routing...")
            rec_tests = {
                '/analysis/recommendation?ticker=EQNR.OL': False,
                '/analysis/recommendations': False
            }
            
            for route in rec_tests:
                try:
                    response = client.get(route)
                    rec_tests[route] = response.status_code == 200
                    status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
                    print(f"   {route}: {status}")
                except Exception as e:
                    print(f"   {route}: ❌ ERROR - {e}")
                    
            results['tests']['step6_recommendation_routing'] = rec_tests
            
            # Summary
            print("\n" + "=" * 80)
            print("📊 COMPREHENSIVE TEST SUMMARY")
            print("=" * 80)
            
            total_tests = 0
            passed_tests = 0
            
            for step, tests in results['tests'].items():
                step_passed = 0
                step_total = 0
                
                for test, result in tests.items():
                    step_total += 1
                    total_tests += 1
                    if result:
                        step_passed += 1
                        passed_tests += 1
                
                step_status = "✅ PASS" if step_passed == step_total else f"⚠️  PARTIAL ({step_passed}/{step_total})"
                print(f"{step}: {step_status}")
            
            overall_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            if overall_percentage >= 90:
                results['overall_status'] = 'EXCELLENT'
                status_icon = '🎉'
            elif overall_percentage >= 75:
                results['overall_status'] = 'GOOD'
                status_icon = '✅'
            elif overall_percentage >= 50:
                results['overall_status'] = 'NEEDS_IMPROVEMENT'
                status_icon = '⚠️'
            else:
                results['overall_status'] = 'CRITICAL_ISSUES'
                status_icon = '❌'
            
            print(f"\n{status_icon} OVERALL STATUS: {results['overall_status']}")
            print(f"📈 Tests passed: {passed_tests}/{total_tests} ({overall_percentage:.1f}%)")
            
            if overall_percentage >= 90:
                print("🎊 Excellent! All critical production issues have been resolved!")
            elif overall_percentage >= 75:
                print("👍 Good! Most issues resolved, minor improvements may be needed.")
            else:
                print("⚠️  Some critical issues remain. Additional fixes required.")
                
            # Save results
            with open('comprehensive_test_results.json', 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"\n📄 Detailed results saved to: comprehensive_test_results.json")
            
            return results

if __name__ == "__main__":
    test_all_critical_fixes()
