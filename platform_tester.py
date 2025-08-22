#!/usr/bin/env python3
"""
Comprehensive 500 Error and Platform Testing Script
Tests critical routes for 500 errors and validates functionality
"""

import requests
import sys
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:5000"  # Adjust if different
TIMEOUT = 10
MAX_RETRIES = 2

# Critical routes to test
CRITICAL_ROUTES = [
    "/",
    "/dashboard",
    "/stocks",
    "/stocks/EQNR.OL",
    "/portfolio",
    "/portfolio/watchlist",
    "/analysis",
    "/analysis/technical",
    "/analysis/sentiment",
    "/analysis/screener",
    "/analysis/short-analysis",
    "/analysis/warren-buffett",
    "/analysis/prediction",
    "/analysis/market-overview",
    "/advanced_features",
    "/advanced_features/dashboard",
    "/about",
    "/resources",
    "/pricing",
    "/auth/demo",
]

class PlatformTester:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": [],
            "route_results": {}
        }
    
    def test_route(self, route):
        """Test a single route for errors and basic functionality"""
        print(f"Testing {route}...")
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    f"{BASE_URL}{route}",
                    timeout=TIMEOUT,
                    allow_redirects=True
                )
                
                # Check for 500 errors
                if response.status_code >= 500:
                    error_msg = f"500 ERROR: {route} returned {response.status_code}"
                    print(f"  ❌ {error_msg}")
                    self.results["errors"].append(error_msg)
                    self.results["route_results"][route] = {
                        "status": "ERROR",
                        "status_code": response.status_code,
                        "error": "Server Error"
                    }
                    self.results["failed"] += 1
                    return False
                
                # Check for other client/server errors
                elif response.status_code >= 400:
                    if response.status_code == 401:
                        # 401 is expected for protected routes
                        print(f"  ⚠️  {route} requires authentication (401) - Expected")
                        self.results["route_results"][route] = {
                            "status": "AUTH_REQUIRED",
                            "status_code": response.status_code,
                            "note": "Authentication required"
                        }
                        self.results["passed"] += 1
                        return True
                    elif response.status_code == 404:
                        error_msg = f"404 ERROR: {route} not found"
                        print(f"  ❌ {error_msg}")
                        self.results["errors"].append(error_msg)
                        self.results["route_results"][route] = {
                            "status": "NOT_FOUND",
                            "status_code": response.status_code,
                            "error": "Route not found"
                        }
                        self.results["failed"] += 1
                        return False
                    else:
                        error_msg = f"CLIENT ERROR: {route} returned {response.status_code}"
                        print(f"  ❌ {error_msg}")
                        self.results["errors"].append(error_msg)
                        self.results["route_results"][route] = {
                            "status": "CLIENT_ERROR",
                            "status_code": response.status_code,
                            "error": "Client Error"
                        }
                        self.results["failed"] += 1
                        return False
                
                # Success (200-299)
                else:
                    # Check for basic HTML content
                    content_length = len(response.text)
                    has_html = "<!DOCTYPE html>" in response.text or "<html" in response.text
                    
                    if content_length < 100:
                        error_msg = f"CONTENT WARNING: {route} returned very short content ({content_length} chars)"
                        print(f"  ⚠️  {error_msg}")
                        self.results["errors"].append(error_msg)
                    
                    if not has_html and "json" not in response.headers.get("content-type", "").lower():
                        error_msg = f"CONTENT WARNING: {route} may not be returning proper HTML"
                        print(f"  ⚠️  {error_msg}")
                        self.results["errors"].append(error_msg)
                    
                    print(f"  ✅ {route} OK ({response.status_code}, {content_length} chars)")
                    self.results["route_results"][route] = {
                        "status": "SUCCESS",
                        "status_code": response.status_code,
                        "content_length": content_length,
                        "has_html": has_html
                    }
                    self.results["passed"] += 1
                    return True
                    
            except requests.exceptions.ConnectionError:
                if attempt < MAX_RETRIES - 1:
                    print(f"  🔄 Connection failed, retrying {route}...")
                    time.sleep(2)
                    continue
                else:
                    error_msg = f"CONNECTION ERROR: Cannot connect to {route}"
                    print(f"  ❌ {error_msg}")
                    self.results["errors"].append(error_msg)
                    self.results["route_results"][route] = {
                        "status": "CONNECTION_ERROR",
                        "error": "Cannot connect to server"
                    }
                    self.results["failed"] += 1
                    return False
                    
            except requests.exceptions.Timeout:
                error_msg = f"TIMEOUT ERROR: {route} timed out after {TIMEOUT}s"
                print(f"  ❌ {error_msg}")
                self.results["errors"].append(error_msg)
                self.results["route_results"][route] = {
                    "status": "TIMEOUT",
                    "error": f"Timeout after {TIMEOUT}s"
                }
                self.results["failed"] += 1
                return False
                
            except Exception as e:
                error_msg = f"UNKNOWN ERROR: {route} - {str(e)}"
                print(f"  ❌ {error_msg}")
                self.results["errors"].append(error_msg)
                self.results["route_results"][route] = {
                    "status": "UNKNOWN_ERROR",
                    "error": str(e)
                }
                self.results["failed"] += 1
                return False
        
        return False
    
    def run_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive Platform Testing...")
        print(f"Testing {len(CRITICAL_ROUTES)} critical routes...\n")
        
        self.results["total_tests"] = len(CRITICAL_ROUTES)
        
        for route in CRITICAL_ROUTES:
            self.test_route(route)
            time.sleep(0.5)  # Brief pause between requests
        
        self.print_summary()
        self.save_results()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"Success Rate: {(self.results['passed']/self.results['total_tests']*100):.1f}%")
        
        if self.results["errors"]:
            print(f"\n⚠️  {len(self.results['errors'])} ISSUES FOUND:")
            for error in self.results["errors"]:
                print(f"  • {error}")
        else:
            print("\n🎉 No critical errors found!")
        
        print("\n" + "="*60)
    
    def save_results(self):
        """Save results to JSON file"""
        with open("platform_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"📄 Detailed results saved to platform_test_results.json")

if __name__ == "__main__":
    print("🧪 Aksjeradar Platform Tester")
    print(f"Target: {BASE_URL}")
    print(f"Timeout: {TIMEOUT}s")
    print("-" * 60)
    
    tester = PlatformTester()
    tester.run_tests()
    
    # Exit with error code if tests failed
    if tester.results["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)
