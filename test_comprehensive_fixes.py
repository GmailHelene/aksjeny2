#!/usr/bin/env python3
"""
Comprehensive testing script to verify all fixes are working correctly
Tests both local development server and live aksjeradar.trade site
"""

import requests
import time
from urllib.parse import urljoin
import json

class ComprehensiveTestSuite:
    def __init__(self):
        self.local_base_url = "http://localhost:5000"
        self.live_base_url = "https://aksjeradar.trade"
        self.test_results = {
            'local': {},
            'live': {}
        }
        
    def test_endpoint(self, endpoint, base_url, description=""):
        """Test if an endpoint is accessible and returns 200"""
        full_url = urljoin(base_url, endpoint)
        try:
            response = requests.get(full_url, timeout=10)
            success = response.status_code == 200
            result = {
                'url': full_url,
                'status_code': response.status_code,
                'success': success,
                'description': description
            }
            
            # Check if response contains error indicators
            if success and response.text:
                content = response.text.lower()
                if any(error in content for error in ['error', '500', '404', 'not found']):
                    result['success'] = False
                    result['warning'] = 'Response contains error indicators'
            
            return result
        except Exception as e:
            return {
                'url': full_url,
                'status_code': 'ERROR',
                'success': False,
                'error': str(e),
                'description': description
            }
    
    def run_tests(self, base_url, label):
        """Run all tests for a given base URL"""
        print(f"\n🧪 Testing {label} ({base_url})")
        print("=" * 60)
        
        test_cases = [
            # Critical endpoints from user's reported issues
            ("/advanced-analytics/", "Advanced Analytics main page"),
            ("/advanced-analytics/dashboard", "Advanced Analytics dashboard"),
            ("/profile/", "Profile page with favorites"),
            ("/external-data/analyst-coverage", "External Data Analyst Coverage"),
            ("/stocks/details/EQNR.OL", "Stock details page (styling check)"),
            ("/price-alerts/", "Price alerts page"),
            ("/portfolio/", "Portfolio page"),
            
            # Additional important endpoints
            ("/", "Homepage"),
            ("/health/", "Health check"),
            ("/api/realtime/market-status", "Market status API"),
            ("/watchlist/", "Watchlist page"),
            ("/news/", "News page"),
        ]
        
        results = {}
        for endpoint, description in test_cases:
            print(f"Testing {endpoint:<35} ... ", end="")
            result = self.test_endpoint(endpoint, base_url, description)
            results[endpoint] = result
            
            if result['success']:
                print("✅ PASS")
            else:
                status = result.get('status_code', 'ERROR')
                error = result.get('error', result.get('warning', ''))
                print(f"❌ FAIL ({status}) {error}")
        
        self.test_results[label.lower()] = results
        return results
    
    def test_api_endpoints(self, base_url, label):
        """Test specific API endpoints that were fixed"""
        print(f"\n🔧 Testing API Endpoints for {label}")
        print("-" * 40)
        
        api_tests = [
            ("/advanced-analytics/api/ml/predict/EQNR.OL", "ML Prediction API"),
            ("/price-alerts/api/alerts", "Price Alerts API"),
            ("/api/realtime/quote/EQNR.OL", "Real-time Quote API"),
        ]
        
        for endpoint, description in api_tests:
            print(f"Testing {endpoint:<45} ... ", end="")
            result = self.test_endpoint(endpoint, base_url, description)
            
            if result['success']:
                print("✅ PASS")
            else:
                print(f"❌ FAIL ({result.get('status_code', 'ERROR')})")
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        for environment in ['local', 'live']:
            if environment in self.test_results:
                results = self.test_results[environment]
                total_tests = len(results)
                passed_tests = sum(1 for r in results.values() if r['success'])
                failed_tests = total_tests - passed_tests
                
                print(f"\n{environment.upper()} ENVIRONMENT:")
                print(f"  Total Tests: {total_tests}")
                print(f"  Passed: {passed_tests} ✅")
                print(f"  Failed: {failed_tests} ❌")
                print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
                
                if failed_tests > 0:
                    print(f"\n  FAILED TESTS:")
                    for endpoint, result in results.items():
                        if not result['success']:
                            status = result.get('status_code', 'ERROR')
                            error = result.get('error', result.get('warning', ''))
                            print(f"    - {endpoint} ({status}) {error}")
        
        # Summary of user's specific issues
        print(f"\n📋 USER'S REPORTED ISSUES STATUS:")
        print("-" * 40)
        
        issue_endpoints = {
            "Advanced Analytics buttons": "/advanced-analytics/",
            "External Data Analyst Coverage": "/external-data/analyst-coverage", 
            "Profile favorites": "/profile/",
            "Stock details styling": "/stocks/details/EQNR.OL",
            "Price alert creation": "/price-alerts/",
            "Portfolio functionality": "/portfolio/"
        }
        
        for issue, endpoint in issue_endpoints.items():
            local_status = "✅" if self.test_results.get('local', {}).get(endpoint, {}).get('success') else "❌"
            live_status = "✅" if self.test_results.get('live', {}).get(endpoint, {}).get('success') else "❌"
            print(f"  {issue:<35} Local: {local_status}  Live: {live_status}")

def main():
    """Run the comprehensive test suite"""
    print("🚀 Starting Comprehensive Fix Verification")
    print("Testing aksjeradar.trade functionality locally and live")
    
    suite = ComprehensiveTestSuite()
    
    # Test local development server
    suite.run_tests(suite.local_base_url, "LOCAL")
    suite.test_api_endpoints(suite.local_base_url, "LOCAL")
    
    # Test live site
    suite.run_tests(suite.live_base_url, "LIVE") 
    suite.test_api_endpoints(suite.live_base_url, "LIVE")
    
    # Generate comprehensive report
    suite.generate_report()
    
    print(f"\n✨ Testing complete!")
    print(f"📈 Local server: {suite.local_base_url}")
    print(f"🌐 Live site: {suite.live_base_url}")

if __name__ == "__main__":
    main()
