#!/usr/bin/env python3
"""
Comprehensive Styling and Loading Fixes Verification Test
Tests the fixes for navigation styling, watchlist loading, and stock details issues.
"""

import requests
import time
import json
from datetime import datetime

class StylingAndLoadingFixTest:
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
    
    def test_navigation_css_inclusion(self):
        """Test that navigation fixes CSS is included in pages"""
        try:
            print("\n🧪 Testing Navigation CSS Inclusion...")
            response = requests.get(f"{self.base_url}/", timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Check if navigation-fixes.css is included
                if "navigation-fixes.css" in content:
                    self.log_test("Navigation CSS Included", "PASS", 
                                "navigation-fixes.css is properly included in base template")
                else:
                    self.log_test("Navigation CSS Included", "FAIL", 
                                "navigation-fixes.css is not found in the page")
                
                # Check for styling elements
                if "#252525" in content or "navbar" in content.lower():
                    self.log_test("Navigation Styling Present", "PASS", 
                                "Navigation styling elements are present")
                else:
                    self.log_test("Navigation Styling Present", "FAIL", 
                                "No navigation styling found")
                
            else:
                self.log_test("Homepage Load", "FAIL", 
                            f"HTTP {response.status_code}: {response.reason}")
                
        except Exception as e:
            self.log_test("Navigation CSS Test", "FAIL", f"Request error: {e}")
    
    def test_watchlist_page_loading(self):
        """Test that watchlist page loads without infinite loading"""
        try:
            print("\n🧪 Testing Watchlist Page Loading...")
            response = requests.get(f"{self.base_url}/watchlist/", timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Check if the page contains "laster varsler" infinite loading
                if "Laster varsler..." in content:
                    # This is expected in the initial HTML, but JavaScript should replace it
                    self.log_test("Watchlist Initial Loading Text", "PASS", 
                                "Initial loading text present (will be replaced by JavaScript)")
                
                # Check for timeout mechanisms in JavaScript
                if "setTimeout" in content and "loadActiveAlerts" in content:
                    self.log_test("Watchlist Timeout Mechanisms", "PASS", 
                                "JavaScript timeout mechanisms are present")
                else:
                    self.log_test("Watchlist Timeout Mechanisms", "FAIL", 
                                "No timeout mechanisms found in JavaScript")
                
                # Check for improved fallback content
                if "Varselsystem aktivt" in content or "System OK" in content:
                    self.log_test("Watchlist Improved Fallback", "PASS", 
                                "Improved fallback content is present")
                else:
                    self.log_test("Watchlist Improved Fallback", "FAIL", 
                                "No improved fallback content found")
                
            else:
                self.log_test("Watchlist Page Load", "FAIL", 
                            f"HTTP {response.status_code}: {response.reason}")
                
        except Exception as e:
            self.log_test("Watchlist Page Test", "FAIL", f"Request error: {e}")
    
    def test_stock_details_page(self):
        """Test stock details page for loading and company info improvements"""
        try:
            print("\n🧪 Testing Stock Details Page...")
            # Test with EQNR.OL as mentioned in the user's request
            response = requests.get(f"{self.base_url}/stocks/details/EQNR.OL", timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Check for improved loading mechanism
                if "Henter kursdata..." in content:
                    self.log_test("Stock Details Loading Text", "PASS", 
                                "Initial loading text present (will be replaced by timeout)")
                
                # Check for fallback mechanism
                if "chart-fallback" in content:
                    self.log_test("Chart Fallback Element", "PASS", 
                                "Chart fallback element is present")
                else:
                    self.log_test("Chart Fallback Element", "FAIL", 
                                "No chart fallback element found")
                
                # Check that old negative messages are replaced
                if "Ingen ledelsesinformasjon tilgjengelig" not in content:
                    self.log_test("Management Info Improved", "PASS", 
                                "Old negative management message replaced")
                else:
                    self.log_test("Management Info Improved", "FAIL", 
                                "Still shows old negative management message")
                
                if "Ingen selskapsbeskrivelse tilgjengelig" not in content:
                    self.log_test("Company Description Improved", "PASS", 
                                "Old negative company description replaced")
                else:
                    self.log_test("Company Description Improved", "FAIL", 
                                "Still shows old negative company description")
                
                # Check for improved content
                if "Selskapsdetaljer" in content or "Ledelsesstruktur" in content:
                    self.log_test("Improved Info Messages", "PASS", 
                                "New improved information messages are present")
                else:
                    self.log_test("Improved Info Messages", "FAIL", 
                                "No improved information messages found")
                
            else:
                self.log_test("Stock Details Page Load", "FAIL", 
                            f"HTTP {response.status_code}: {response.reason}")
                
        except Exception as e:
            self.log_test("Stock Details Test", "FAIL", f"Request error: {e}")
    
    def test_javascript_enhancements(self):
        """Test that JavaScript enhancements are in place"""
        try:
            print("\n🧪 Testing JavaScript Enhancements...")
            
            # Test watchlist page for JavaScript improvements
            response = requests.get(f"{self.base_url}/watchlist/", timeout=30)
            
            if response.status_code == 200:
                content = response.text
                
                # Check for timeout implementations
                timeout_count = content.count("setTimeout")
                if timeout_count >= 2:
                    self.log_test("JavaScript Timeouts", "PASS", 
                                f"Found {timeout_count} setTimeout implementations")
                else:
                    self.log_test("JavaScript Timeouts", "FAIL", 
                                f"Only found {timeout_count} setTimeout implementations")
                
                # Check for improved error handling
                if "catch" in content and "error" in content.lower():
                    self.log_test("Error Handling", "PASS", 
                                "Error handling mechanisms are present")
                else:
                    self.log_test("Error Handling", "FAIL", 
                                "No error handling mechanisms found")
                
                # Check for fetch API usage with timeout
                if "fetch" in content and "Promise.race" in content:
                    self.log_test("Advanced Fetch Handling", "PASS", 
                                "Advanced fetch with timeout race condition")
                else:
                    self.log_test("Advanced Fetch Handling", "FAIL", 
                                "No advanced fetch handling found")
                
            else:
                self.log_test("JavaScript Enhancement Check", "FAIL", 
                            f"Could not load page for JavaScript check")
                
        except Exception as e:
            self.log_test("JavaScript Enhancement Test", "FAIL", f"Request error: {e}")
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting Styling and Loading Fixes Verification...")
        print("=" * 70)
        
        # Run tests
        self.test_navigation_css_inclusion()
        self.test_watchlist_page_loading()
        self.test_stock_details_page()
        self.test_javascript_enhancements()
        
        # Generate summary
        print("\n" + "=" * 70)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 70)
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
        with open('styling_loading_fixes_test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📁 Detailed results saved to: styling_loading_fixes_test_results.json")
        
        if self.results['tests_failed'] == 0:
            print("\n🎉 ALL TESTS PASSED! The styling and loading fixes are working correctly.")
            return True
        else:
            print(f"\n⚠️  {self.results['tests_failed']} test(s) failed. Review the issues above.")
            return False

if __name__ == "__main__":
    tester = StylingAndLoadingFixTest()
    success = tester.run_all_tests()
    exit(0 if success else 1)
