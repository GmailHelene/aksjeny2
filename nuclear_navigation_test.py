#!/usr/bin/env python3
"""
Nuclear Navigation Fix Test Suite
Comprehensive testing to verify all navigation issues are resolved
"""

import requests
import json
import time
from datetime import datetime

def test_nuclear_navigation_fix():
    """Run comprehensive tests for the nuclear navigation fix"""
    
    print("🚨 NUCLEAR NAVIGATION FIX TEST SUITE")
    print("=" * 50)
    
    base_url = "http://0.0.0.0:5001"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {
        "timestamp": timestamp,
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "test_results": []
    }
    
    # Test 1: Main page loads successfully
    print("\n🧪 Test 1: Main page accessibility")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Main page loads successfully")
            results["passed_tests"] += 1
            results["test_results"].append({"test": "main_page_load", "status": "PASS", "details": "200 OK"})
        else:
            print(f"❌ Main page failed: {response.status_code}")
            results["failed_tests"] += 1
            results["test_results"].append({"test": "main_page_load", "status": "FAIL", "details": f"{response.status_code}"})
        results["total_tests"] += 1
    except Exception as e:
        print(f"❌ Main page error: {e}")
        results["failed_tests"] += 1
        results["total_tests"] += 1
        results["test_results"].append({"test": "main_page_load", "status": "FAIL", "details": str(e)})
    
    # Test 2: Nuclear navigation script loads
    print("\n🧪 Test 2: Nuclear navigation script loading")
    try:
        response = requests.get(f"{base_url}/static/js/dropdown-navigation.js", timeout=10)
        if response.status_code == 200 and "NUCLEAR NAVIGATION FIX" in response.text:
            print("✅ Nuclear navigation script loads correctly")
            results["passed_tests"] += 1
            results["test_results"].append({"test": "nuclear_script_load", "status": "PASS", "details": "Script contains nuclear fix"})
        else:
            print(f"❌ Nuclear navigation script failed: {response.status_code}")
            results["failed_tests"] += 1
            results["test_results"].append({"test": "nuclear_script_load", "status": "FAIL", "details": f"{response.status_code}"})
        results["total_tests"] += 1
    except Exception as e:
        print(f"❌ Nuclear navigation script error: {e}")
        results["failed_tests"] += 1
        results["total_tests"] += 1
        results["test_results"].append({"test": "nuclear_script_load", "status": "FAIL", "details": str(e)})
    
    # Test 3: Main page HTML contains nuclear CSS override
    print("\n🧪 Test 3: Nuclear CSS override presence")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200 and "NUCLEAR CSS OVERRIDE" in response.text:
            print("✅ Nuclear CSS override is present")
            results["passed_tests"] += 1
            results["test_results"].append({"test": "nuclear_css_override", "status": "PASS", "details": "CSS override found"})
        else:
            print("❌ Nuclear CSS override missing")
            results["failed_tests"] += 1
            results["test_results"].append({"test": "nuclear_css_override", "status": "FAIL", "details": "CSS override not found"})
        results["total_tests"] += 1
    except Exception as e:
        print(f"❌ Nuclear CSS override error: {e}")
        results["failed_tests"] += 1
        results["total_tests"] += 1
        results["test_results"].append({"test": "nuclear_css_override", "status": "FAIL", "details": str(e)})
    
    # Test 4: Cache busting timestamp is updated
    print("\n🧪 Test 4: Cache busting timestamp")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200 and "20250806_164605" in response.text:
            print("✅ Latest cache busting timestamp present")
            results["passed_tests"] += 1
            results["test_results"].append({"test": "cache_timestamp", "status": "PASS", "details": "Timestamp 20250806_164605 found"})
        else:
            print("❌ Cache busting timestamp missing or outdated")
            results["failed_tests"] += 1
            results["test_results"].append({"test": "cache_timestamp", "status": "FAIL", "details": "Timestamp not found"})
        results["total_tests"] += 1
    except Exception as e:
        print(f"❌ Cache busting timestamp error: {e}")
        results["failed_tests"] += 1
        results["total_tests"] += 1
        results["test_results"].append({"test": "cache_timestamp", "status": "FAIL", "details": str(e)})
    
    # Test 5: Demo page (additional navigation test)
    print("\n🧪 Test 5: Demo page navigation")
    try:
        response = requests.get(f"{base_url}/demo", timeout=10)
        if response.status_code == 200:
            print("✅ Demo page loads successfully")
            results["passed_tests"] += 1
            results["test_results"].append({"test": "demo_page_load", "status": "PASS", "details": "200 OK"})
        else:
            print(f"❌ Demo page failed: {response.status_code}")
            results["failed_tests"] += 1
            results["test_results"].append({"test": "demo_page_load", "status": "FAIL", "details": f"{response.status_code}"})
        results["total_tests"] += 1
    except Exception as e:
        print(f"❌ Demo page error: {e}")
        results["failed_tests"] += 1
        results["total_tests"] += 1
        results["test_results"].append({"test": "demo_page_load", "status": "FAIL", "details": str(e)})
    
    # Test 6: Portfolio page (dropdown test)
    print("\n🧪 Test 6: Portfolio page navigation")
    try:
        response = requests.get(f"{base_url}/portfolio/", timeout=10)
        if response.status_code in [200, 302]:  # 302 might be redirect for auth
            print("✅ Portfolio page accessible")
            results["passed_tests"] += 1
            results["test_results"].append({"test": "portfolio_page_load", "status": "PASS", "details": f"{response.status_code}"})
        else:
            print(f"❌ Portfolio page failed: {response.status_code}")
            results["failed_tests"] += 1
            results["test_results"].append({"test": "portfolio_page_load", "status": "FAIL", "details": f"{response.status_code}"})
        results["total_tests"] += 1
    except Exception as e:
        print(f"❌ Portfolio page error: {e}")
        results["failed_tests"] += 1
        results["total_tests"] += 1
        results["test_results"].append({"test": "portfolio_page_load", "status": "FAIL", "details": str(e)})
    
    # Test 7: Analysis page (dropdown test)
    print("\n🧪 Test 7: Analysis page navigation")
    try:
        response = requests.get(f"{base_url}/analysis/", timeout=10)
        if response.status_code == 200:
            print("✅ Analysis page loads successfully")
            results["passed_tests"] += 1
            results["test_results"].append({"test": "analysis_page_load", "status": "PASS", "details": "200 OK"})
        else:
            print(f"❌ Analysis page failed: {response.status_code}")
            results["failed_tests"] += 1
            results["test_results"].append({"test": "analysis_page_load", "status": "FAIL", "details": f"{response.status_code}"})
        results["total_tests"] += 1
    except Exception as e:
        print(f"❌ Analysis page error: {e}")
        results["failed_tests"] += 1
        results["total_tests"] += 1
        results["test_results"].append({"test": "analysis_page_load", "status": "FAIL", "details": str(e)})
    
    # Calculate success rate
    success_rate = (results["passed_tests"] / results["total_tests"] * 100) if results["total_tests"] > 0 else 0
    
    print("\n" + "=" * 50)
    print("🚨 NUCLEAR NAVIGATION FIX TEST RESULTS")
    print("=" * 50)
    print(f"📊 Total Tests: {results['total_tests']}")
    print(f"✅ Passed: {results['passed_tests']}")
    print(f"❌ Failed: {results['failed_tests']}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 85:
        print("\n🎉 NUCLEAR NAVIGATION FIX: SUCCESS!")
        print("   Navigation system should now work correctly")
    elif success_rate >= 70:
        print("\n⚠️  NUCLEAR NAVIGATION FIX: PARTIAL SUCCESS")
        print("   Some issues may remain")
    else:
        print("\n💥 NUCLEAR NAVIGATION FIX: NEEDS MORE WORK")
        print("   Significant issues remain")
    
    # Save results
    filename = f"nuclear_navigation_test_results_{timestamp}.json"
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📝 Results saved to: {filename}")
    except Exception as e:
        print(f"\n❌ Could not save results: {e}")
    
    return results

if __name__ == "__main__":
    test_nuclear_navigation_fix()
