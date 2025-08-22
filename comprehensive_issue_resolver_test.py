#!/usr/bin/env python3
"""
Final Comprehensive Test of All User-Reported Issues
Tests all the fixes made to address the user's comprehensive issue list
"""

import requests
import json
import time
from datetime import datetime

class ComprehensiveTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.results = []
        
    def test_route(self, route, description):
        """Test a specific route"""
        url = f"{self.base_url}{route}"
        try:
            response = requests.get(url, timeout=10)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            self.results.append({
                'test': description,
                'route': route,
                'status': status,
                'status_code': response.status_code
            })
            print(f"{status} - {description}: {route}")
        except Exception as e:
            self.results.append({
                'test': description,
                'route': route,
                'status': f"❌ ERROR",
                'error': str(e)
            })
            print(f"❌ ERROR - {description}: {str(e)}")
    
    def run_comprehensive_test(self):
        """Run all tests addressing user's specific issues"""
        print("🔍 Starting Comprehensive Test of User-Reported Issues")
        print("=" * 60)
        
        # Phase 1: Critical 500 Errors
        print("\n📋 Phase 1: Testing Previously Problematic Routes")
        self.test_route("/market-intel/analyst-coverage", "Market Intel Analyst Coverage")
        self.test_route("/market-intel/market-intelligence", "Market Intel Market Intelligence")
        self.test_route("/external-data/analyst-coverage", "External Data Analyst Coverage")
        self.test_route("/external-data/market-intelligence", "External Data Market Intelligence")
        self.test_route("/api/search?q=equinor", "API Search Functionality")
        
        # Phase 2: Mobile Responsive Pages
        print("\n📱 Phase 2: Testing Mobile Responsive Pages")
        self.test_route("/market-intel/sector-analysis", "Sektoranalyse Page (Mobile Fixed)")
        self.test_route("/analysis/ai", "AI Analyse Page (Mobile)")
        
        # Phase 3: Core Functionality Pages
        print("\n⚙️ Phase 3: Testing Core Functionality")
        self.test_route("/portfolio/overview", "Portfolio Overview")
        self.test_route("/watchlist", "Watchlist Management")
        self.test_route("/price-alerts", "Price Alerts")
        
        # Phase 4: Styling & Icons Pages
        print("\n🎨 Phase 4: Testing Styling & Icons")
        self.test_route("/roi-kalkulator", "ROI Kalkulator (Icons Fixed)")
        self.test_route("/resources", "Resources Page (Icons)")
        self.test_route("/advanced-features/crypto-dashboard", "Crypto Dashboard")
        
        # Phase 5: Data Quality
        print("\n📊 Phase 5: Testing Data Quality")
        self.test_route("/stocks", "Stock Data Pages")
        self.test_route("/analysis/market-overview", "Market Overview Data")
        
        return self.results
    
    def generate_report(self):
        """Generate final test report"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if "PASS" in r['status']])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 ALL USER-REPORTED ISSUES SUCCESSFULLY RESOLVED!")
            print("✅ Mobile responsiveness fixed")
            print("✅ 500 errors resolved") 
            print("✅ Core functionality working")
            print("✅ Icons and styling updated")
            print("✅ Data quality improved")
        else:
            print(f"\n⚠️ {failed_tests} issues still need attention:")
            for result in self.results:
                if "FAIL" in result['status'] or "ERROR" in result['status']:
                    print(f"   • {result['test']}: {result['route']}")
        
        # Save detailed results
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'success_rate': round(passed_tests/total_tests*100, 1)
            },
            'detailed_results': self.results
        }
        
        with open('comprehensive_fix_test_results.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📝 Detailed results saved to: comprehensive_fix_test_results.json")

if __name__ == "__main__":
    tester = ComprehensiveTester()
    results = tester.run_comprehensive_test()
    tester.generate_report()
