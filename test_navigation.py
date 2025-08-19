#!/usr/bin/env python3
"""
Navigation Test Suite - Verify PC and Mobile Navigation Functionality
"""

import requests
import json
from datetime import datetime

def test_navigation_endpoints():
    """Test that all navigation endpoints are accessible"""
    base_url = "http://localhost:5001"
    
    # Main navigation endpoints
    endpoints_to_test = [
        "/stocks/",      # Aksjer main page
        "/analysis/",    # Analyse main page  
        "/portfolio/",   # Portefølje main page
        "/news",         # Nyheter
        "/financial-dashboard",  # Dashboard
    ]
    
    results = {
        "test_time": datetime.now().isoformat(),
        "navigation_endpoints": {},
        "summary": {"passed": 0, "failed": 0, "total": 0}
    }
    
    print("🧪 Testing Navigation Endpoints...")
    print("=" * 50)
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            
            results["navigation_endpoints"][endpoint] = {
                "status_code": response.status_code,
                "passed": response.status_code == 200,
                "content_length": len(response.content)
            }
            
            if response.status_code == 200:
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1
                
            print(f"{status:<15} {endpoint:<25} ({response.status_code}, {len(response.content):,} bytes)")
            
        except Exception as e:
            print(f"❌ ERROR      {endpoint:<25} ({str(e)})")
            results["navigation_endpoints"][endpoint] = {
                "status_code": 0,
                "passed": False,
                "error": str(e)
            }
            results["summary"]["failed"] += 1
        
        results["summary"]["total"] += 1
    
    print("=" * 50)
    print(f"📊 Summary: {results['summary']['passed']}/{results['summary']['total']} endpoints passed")
    
    # Save results
    filename = f"navigation_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Results saved to: {filename}")
    return results

def check_navigation_javascript():
    """Check if the navigation JavaScript is properly loaded"""
    try:
        response = requests.get("http://localhost:5001/static/js/dropdown-navigation.js")
        if response.status_code == 200:
            content = response.text
            
            # Check for key functions
            has_desktop_setup = "setupDesktopNavigation" in content
            has_mobile_setup = "setupMobileNavigation" in content
            has_toggle_function = "toggleMobileDropdown" in content
            
            print("\n🔧 Navigation JavaScript Analysis:")
            print("=" * 50)
            print(f"✅ File loaded: {response.status_code == 200}")
            print(f"✅ Desktop setup function: {has_desktop_setup}")
            print(f"✅ Mobile setup function: {has_mobile_setup}")
            print(f"✅ Mobile toggle function: {has_toggle_function}")
            print(f"📏 File size: {len(content):,} characters")
            
            return {
                "loaded": True,
                "has_desktop_setup": has_desktop_setup,
                "has_mobile_setup": has_mobile_setup,
                "has_toggle_function": has_toggle_function,
                "file_size": len(content)
            }
        else:
            print(f"❌ Navigation JavaScript failed to load: {response.status_code}")
            return {"loaded": False, "status_code": response.status_code}
            
    except Exception as e:
        print(f"❌ Error checking navigation JavaScript: {e}")
        return {"loaded": False, "error": str(e)}

if __name__ == "__main__":
    print("🚀 AKSJERADAR NAVIGATION TEST SUITE")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test navigation endpoints
    endpoint_results = test_navigation_endpoints()
    
    # Test navigation JavaScript
    js_results = check_navigation_javascript()
    
    print("\n🎯 NAVIGATION TEST COMPLETE")
    print("=" * 50)
    
    if endpoint_results["summary"]["passed"] == endpoint_results["summary"]["total"] and js_results.get("loaded", False):
        print("✅ ALL TESTS PASSED - Navigation system ready!")
    else:
        print("⚠️  Some tests failed - Check results above")
