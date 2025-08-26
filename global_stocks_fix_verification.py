#!/usr/bin/env python3
"""
Global Stocks Fix Verification Test
Tests the fixes for both notifications settings and global stocks pages.
"""

import requests
import time
import json
from datetime import datetime

class GlobalStocksFixTest:
    def __init__(self):
        self.base_url = "https://aksjeradar.trade"
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'issues_found': [],
            'successes': []
        }
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        self.results['tests_run'] += 1
        if status == 'PASS':
            self.results['tests_passed'] += 1
            self.results['successes'].append(f"✅ {test_name}: {details}")
            print(f"✅ {test_name}: {details}")
        else:
            self.results['tests_failed'] += 1
            self.results['issues_found'].append(f"❌ {test_name}: {details}")
            print(f"❌ {test_name}: {details}")
    
    def test_global_stocks_page_loads(self):
        """Test that global stocks page loads without showing 'Ingen data tilgjengelig'"""
        try:
            print("\n🧪 Testing Global Stocks Page Loading...")
            response = requests.get(f"{self.base_url}/stocks/global", timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Check if we're showing "Ingen data tilgjengelig"
                if "Ingen data tilgjengelig" in content:
                    self.log_test("Global Stocks Data Available", "FAIL", 
                                "Page still shows 'Ingen data tilgjengelig' message")
                else:
                    self.log_test("Global Stocks Data Available", "PASS", 
                                "Page loads without 'Ingen data tilgjengelig' message")
                
                # Check if we have stock symbols in the table
                stock_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
                found_symbols = []
                for symbol in stock_symbols:
                    if symbol in content:
                        found_symbols.append(symbol)
                
                if len(found_symbols) >= 3:
                    self.log_test("Stock Symbols Present", "PASS", 
                                f"Found {len(found_symbols)} stock symbols: {', '.join(found_symbols)}")
                else:
                    self.log_test("Stock Symbols Present", "FAIL", 
                                f"Only found {len(found_symbols)} stock symbols: {', '.join(found_symbols)}")
                
                # Check for stock prices ($ signs indicating price data)
                price_indicators = content.count('$')
                if price_indicators >= 5:
                    self.log_test("Stock Prices Present", "PASS", 
                                f"Found {price_indicators} price indicators ($)")
                else:
                    self.log_test("Stock Prices Present", "FAIL", 
                                f"Only found {price_indicators} price indicators")
                
                # Check for table structure
                if '<table class="table table-hover' in content:
                    self.log_test("Table Structure Present", "PASS", 
                                "Stock table structure is present")
                else:
                    self.log_test("Table Structure Present", "FAIL", 
                                "Stock table structure is missing")
                
            else:
                self.log_test("Global Stocks Page Load", "FAIL", 
                            f"HTTP {response.status_code}: {response.reason}")
                
        except Exception as e:
            self.log_test("Global Stocks Page Load", "FAIL", f"Request error: {e}")
    
    def test_notifications_api_endpoints(self):
        """Test that notifications API endpoints exist"""
        try:
            print("\n🧪 Testing Notifications API Endpoints...")
            
            # Test price alerts endpoint that was missing
            response = requests.get(f"{self.base_url}/notifications/api/price_alerts", timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.log_test("Price Alerts API", "PASS", 
                                f"Endpoint returns JSON: {type(data)}")
                except:
                    self.log_test("Price Alerts API", "PASS", 
                                "Endpoint exists and returns response")
            elif response.status_code == 404:
                self.log_test("Price Alerts API", "FAIL", 
                            "Endpoint still returns 404 - not fixed")
            else:
                self.log_test("Price Alerts API", "PASS", 
                            f"Endpoint exists (HTTP {response.status_code})")
                
        except Exception as e:
            self.log_test("Price Alerts API", "FAIL", f"Request error: {e}")
    
    def test_notifications_settings_page(self):
        """Test notifications settings page for timeout fixes"""
        try:
            print("\n🧪 Testing Notifications Settings Page...")
            response = requests.get(f"{self.base_url}/notifications/settings", timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Check for timeout mechanisms in JavaScript
                if "setTimeout" in content:
                    self.log_test("Timeout Mechanisms", "PASS", 
                                "JavaScript timeout mechanisms are present")
                else:
                    self.log_test("Timeout Mechanisms", "FAIL", 
                                "No setTimeout found in JavaScript")
                
                # Check for showInfo function
                if "showInfo" in content or "showSuccess" in content:
                    self.log_test("Toast Notifications", "PASS", 
                                "Toast notification functions are present")
                else:
                    self.log_test("Toast Notifications", "FAIL", 
                                "Toast notification functions missing")
                
                # Check for proper error handling
                if "catch" in content and "error" in content.lower():
                    self.log_test("Error Handling", "PASS", 
                                "Error handling mechanisms are present")
                else:
                    self.log_test("Error Handling", "FAIL", 
                                "Error handling mechanisms missing")
                
            else:
                self.log_test("Notifications Settings Page", "FAIL", 
                            f"HTTP {response.status_code}: {response.reason}")
                
        except Exception as e:
            self.log_test("Notifications Settings Page", "FAIL", f"Request error: {e}")
    
    def test_authenticated_user_experience(self):
        """Test that authenticated users get better data"""
        try:
            print("\n🧪 Testing Authenticated User Data Priority...")
            
            # Test the global stocks page for authenticated users
            # Note: This is a basic test since we can't actually authenticate
            response = requests.get(f"{self.base_url}/stocks/global", timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Check for user authentication indicators
                if "user_authenticated" in content or "authenticated" in content.lower():
                    self.log_test("Authentication Context", "PASS", 
                                "Authentication context is being passed to template")
                else:
                    self.log_test("Authentication Context", "FAIL", 
                                "No authentication context found")
                
                # Check for data source indicators
                if "real data" in content.lower() or "enhanced" in content.lower():
                    self.log_test("Data Source Indicators", "PASS", 
                                "Data source information is present")
                else:
                    self.log_test("Data Source Indicators", "FAIL", 
                                "No data source indicators found")
                
            else:
                self.log_test("Authenticated User Context", "FAIL", 
                            f"HTTP {response.status_code}: {response.reason}")
                
        except Exception as e:
            self.log_test("Authenticated User Context", "FAIL", f"Request error: {e}")
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting Global Stocks & Notifications Fix Verification...")
        print("=" * 60)
        
        # Run tests
        self.test_global_stocks_page_loads()
        self.test_notifications_api_endpoints()
        self.test_notifications_settings_page()
        self.test_authenticated_user_experience()
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Tests Run: {self.results['tests_run']}")
        print(f"Tests Passed: {self.results['tests_passed']}")
        print(f"Tests Failed: {self.results['tests_failed']}")
        print(f"Success Rate: {(self.results['tests_passed']/self.results['tests_run']*100):.1f}%")
        
        if self.results['issues_found']:
            print(f"\n❌ ISSUES FOUND ({len(self.results['issues_found'])}):")
            for issue in self.results['issues_found']:
                print(f"   {issue}")
        
        if self.results['successes']:
            print(f"\n✅ SUCCESSES ({len(self.results['successes'])}):")
            for success in self.results['successes']:
                print(f"   {success}")
        
        # Save results
        with open('global_stocks_fix_test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📁 Detailed results saved to: global_stocks_fix_test_results.json")
        
        if self.results['tests_failed'] == 0:
            print("\n🎉 ALL TESTS PASSED! The fixes appear to be working correctly.")
            return True
        else:
            print(f"\n⚠️  {self.results['tests_failed']} test(s) failed. Review the issues above.")
            return False

if __name__ == "__main__":
    tester = GlobalStocksFixTest()
    success = tester.run_all_tests()
    exit(0 if success else 1)
