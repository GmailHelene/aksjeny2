#!/usr/bin/env python3
"""
Comprehensive test to verify all major fixes are working correctly
"""

import requests
import time
import sys
import json
from urllib.parse import urljoin

class ComprehensiveFixVerification:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = {
            'portfolio_access': False,
            'chart_data_loading': False,
            'watchlist_api': False,
            'analysis_routes_access': False,
            'mobile_navigation': False,
            'csrf_protection': False
        }
        
    def test_portfolio_access(self):
        """Test portfolio route accessibility"""
        try:
            response = self.session.get(urljoin(self.base_url, "/portfolio"))
            if response.status_code == 200:
                self.results['portfolio_access'] = True
                print("✅ Portfolio route accessible")
            else:
                print(f"❌ Portfolio route returned {response.status_code}")
        except Exception as e:
            print(f"❌ Portfolio test failed: {e}")
    
    def test_chart_data_api(self):
        """Test chart data API endpoint"""
        try:
            # Test with a common stock symbol
            response = self.session.get(urljoin(self.base_url, "/stocks/api/demo/chart-data/AAPL"))
            if response.status_code == 200:
                data = response.json()
                if 'timestamps' in data or 'prices' in data:
                    self.results['chart_data_loading'] = True
                    print("✅ Chart data API working")
                else:
                    print("❌ Chart data API returned invalid format")
            else:
                print(f"❌ Chart data API returned {response.status_code}")
        except Exception as e:
            print(f"❌ Chart data test failed: {e}")
    
    def test_watchlist_api(self):
        """Test watchlist API endpoint"""
        try:
            # Test GET request first
            response = self.session.get(urljoin(self.base_url, "/api/watchlist/add"))
            if response.status_code in [200, 405]:  # 405 is OK for GET on POST endpoint
                self.results['watchlist_api'] = True
                print("✅ Watchlist API endpoint accessible")
            else:
                print(f"❌ Watchlist API returned {response.status_code}")
        except Exception as e:
            print(f"❌ Watchlist test failed: {e}")
    
    def test_analysis_routes(self):
        """Test key analysis routes accessibility"""
        routes_to_test = [
            "/analysis",
            "/analysis/market-overview",
            "/analysis/technical",
            "/analysis/recommendations",
            "/analysis/warren-buffett",
            "/analysis/benjamin-graham"
        ]
        
        accessible_routes = 0
        for route in routes_to_test:
            try:
                response = self.session.get(urljoin(self.base_url, route))
                if response.status_code == 200:
                    accessible_routes += 1
                    print(f"✅ {route} accessible")
                else:
                    print(f"❌ {route} returned {response.status_code}")
            except Exception as e:
                print(f"❌ {route} test failed: {e}")
        
        if accessible_routes == len(routes_to_test):
            self.results['analysis_routes_access'] = True
            print("✅ All analysis routes accessible")
        else:
            print(f"❌ Only {accessible_routes}/{len(routes_to_test)} analysis routes accessible")
    
    def test_mobile_navigation(self):
        """Test mobile navigation by checking base template"""
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                content = response.text
                # Check for mobile navigation elements
                if ('navbar-toggler' in content and 
                    'navbar-collapse' in content and
                    '@media' in content):
                    self.results['mobile_navigation'] = True
                    print("✅ Mobile navigation elements present")
                else:
                    print("❌ Mobile navigation elements missing")
            else:
                print(f"❌ Home page returned {response.status_code}")
        except Exception as e:
            print(f"❌ Mobile navigation test failed: {e}")
    
    def test_csrf_protection(self):
        """Test CSRF token availability"""
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                content = response.text
                if 'csrf-token' in content:
                    self.results['csrf_protection'] = True
                    print("✅ CSRF protection enabled")
                else:
                    print("❌ CSRF token not found")
            else:
                print(f"❌ Home page returned {response.status_code}")
        except Exception as e:
            print(f"❌ CSRF test failed: {e}")
    
    def run_all_tests(self):
        """Run all verification tests"""
        print("🔍 Starting comprehensive fix verification...")
        print("="*50)
        
        self.test_portfolio_access()
        self.test_chart_data_api()
        self.test_watchlist_api()
        self.test_analysis_routes()
        self.test_mobile_navigation()
        self.test_csrf_protection()
        
        print("\n" + "="*50)
        print("📊 Test Results Summary:")
        print("="*50)
        
        total_tests = len(self.results)
        passed_tests = sum(self.results.values())
        
        for test_name, result in self.results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All fixes verified successfully!")
            return True
        else:
            print("⚠️  Some issues still need attention")
            return False

if __name__ == "__main__":
    # Check if server is running
    import socket
    
    def is_server_running(host='localhost', port=5000):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex((host, port))
            return result == 0
        finally:
            sock.close()
    
    if not is_server_running():
        print("❌ Server is not running on localhost:5000")
        print("Please start the Flask server first: python3 main.py")
        sys.exit(1)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Run verification
    verifier = ComprehensiveFixVerification()
    success = verifier.run_all_tests()
    
    sys.exit(0 if success else 1)
