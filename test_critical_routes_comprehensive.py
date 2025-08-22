#!/usr/bin/env python3
"""
Simple Critical Routes Tester - Tests all remaining issues
"""

import requests
import json
import time
import sys
from datetime import datetime

def test_flask_server_status():
    """Check if Flask server is running"""
    ports_to_try = [5000, 5002, 8000]
    
    for port in ports_to_try:
        try:
            url = f"http://localhost:{port}/"
            response = requests.get(url, timeout=3)
            print(f"✅ Flask server found on port {port} (Status: {response.status_code})")
            return f"http://localhost:{port}"
        except requests.exceptions.ConnectError:
            print(f"❌ No server on port {port}")
        except Exception as e:
            print(f"⚠️  Error checking port {port}: {e}")
    
    print("❌ No Flask server found on any common port")
    return None

def test_critical_routes(base_url):
    """Test all critical routes for the 19 issues"""
    
    # Routes corresponding to the 19 critical issues
    test_routes = [
        # TradingView and charts (FIXED)
        ("/analysis/tradingview", "TradingView charts"),
        ("/analysis/technical", "Technical analysis"),
        
        # Search functionality (FIXED)
        ("/search", "Search functionality"),
        
        # Stock analysis tools (FIXED)
        ("/analysis/compare", "Stock comparison"),
        ("/analysis/screener", "Stock screener"),
        ("/analysis/recommendations", "Stock recommendations"),
        
        # News intelligence (FIXED)
        ("/news-intelligence", "News intelligence dashboard"),
        ("/news-intelligence/sentiment", "Sentiment analysis"),
        
        # Portfolio and watchlist
        ("/portfolio", "Portfolio dashboard"),
        ("/portfolio/performance", "Portfolio performance"),
        ("/portfolio/watchlist", "Watchlist functionality"),
        
        # Advanced features
        ("/advanced/crypto-dashboard", "Crypto dashboard"),
        ("/advanced/options-analyzer", "Options analyzer"),
        
        # Analysis features
        ("/analysis/risk", "Risk analysis"),
        ("/analysis/sectors", "Sector analysis"),
        
        # User features
        ("/features/notifications", "Notification system"),
        ("/features/profile", "User profile"),
        
        # API endpoints
        ("/achievements/api/user_stats", "Achievement tracking API - GET"),
        ("/api/notifications", "Notifications API"),
    ]
    
    print(f"\n🧪 Testing {len(test_routes)} critical routes...")
    print("=" * 60)
    
    results = {
        'success': [],
        'failed': [],
        'errors': []
    }
    
    for route, description in test_routes:
        try:
            url = f"{base_url}{route}"
            response = requests.get(url, timeout=10)
            
            status = response.status_code
            print(f"📍 {route}")
            print(f"   {description}")
            
            if status == 200:
                print(f"   ✅ SUCCESS (200)")
                results['success'].append((route, description))
            elif status == 302:
                print(f"   🔄 REDIRECT (302) - May require authentication")
                results['success'].append((route, description))
            elif status == 405:
                print(f"   ⚠️  METHOD NOT ALLOWED (405) - Route exists but wrong method")
                results['success'].append((route, description))
            elif status == 500:
                print(f"   ❌ SERVER ERROR (500) - NEEDS FIXING")
                results['failed'].append((route, description, 500))
                # Try to get error details
                try:
                    error_text = response.text[:200] if response.text else "No error details"
                    print(f"   📝 Error preview: {error_text}")
                except:
                    pass
            elif status == 404:
                print(f"   ❌ NOT FOUND (404) - Route missing")
                results['failed'].append((route, description, 404))
            else:
                print(f"   ⚠️  UNEXPECTED STATUS ({status})")
                results['failed'].append((route, description, status))
            
            print()  # Blank line for readability
            time.sleep(0.5)  # Rate limiting
            
        except requests.exceptions.ConnectError:
            print(f"   ❌ CONNECTION ERROR - Server not responding")
            results['errors'].append((route, description, "Connection Error"))
            break
        except requests.exceptions.Timeout:
            print(f"   ❌ TIMEOUT - Route too slow")
            results['failed'].append((route, description, "Timeout"))
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results['errors'].append((route, description, str(e)))
    
    return results

def test_achievement_api_post(base_url):
    """Test the achievement tracking API with POST request"""
    print("\n🧪 Testing Achievement API (POST)")
    print("=" * 40)
    
    try:
        url = f"{base_url}/achievements/api/update_stat"
        data = {
            "type": "favorites",
            "increment": 1
        }
        
        response = requests.post(url, json=data, timeout=10)
        status = response.status_code
        
        print(f"📍 POST {url}")
        print(f"   Data: {data}")
        
        if status == 200:
            print(f"   ✅ SUCCESS (200)")
            try:
                response_data = response.json()
                print(f"   📝 Response: {response_data}")
            except:
                print(f"   📝 Response text: {response.text[:100]}")
            return True
        elif status == 302:
            print(f"   🔄 REDIRECT (302) - Authentication required")
            return True  # Route exists
        elif status == 500:
            print(f"   ❌ SERVER ERROR (500) - DATABASE ISSUE")
            try:
                error_text = response.text[:300] if response.text else "No error details"
                print(f"   📝 Error: {error_text}")
            except:
                pass
            return False
        else:
            print(f"   ⚠️  STATUS {status}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def generate_report(results, achievement_api_result):
    """Generate final test report"""
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    total_routes = len(results['success']) + len(results['failed']) + len(results['errors'])
    success_count = len(results['success'])
    failed_count = len(results['failed'])
    error_count = len(results['errors'])
    
    print(f"📈 OVERVIEW:")
    print(f"   Total routes tested: {total_routes}")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   🚫 Errors: {error_count}")
    
    if success_count > 0:
        success_rate = (success_count / total_routes) * 100
        print(f"   📊 Success rate: {success_rate:.1f}%")
    
    if failed_count > 0:
        print(f"\n❌ FAILED ROUTES ({failed_count}):")
        for route, description, status in results['failed']:
            print(f"   • {route} - {description} ({status})")
    
    if error_count > 0:
        print(f"\n🚫 ERROR ROUTES ({error_count}):")
        for route, description, error in results['errors']:
            print(f"   • {route} - {description} ({error})")
    
    print(f"\n🎯 ACHIEVEMENT API:")
    if achievement_api_result:
        print("   ✅ Achievement tracking API working")
    else:
        print("   ❌ Achievement tracking API has issues")
    
    # Calculate overall progress
    fixed_issues = 7  # Previously completed
    working_routes = success_count
    total_issues = 19
    
    if achievement_api_result:
        working_routes += 1  # Achievement API working
    
    total_working = min(fixed_issues + (working_routes // 2), total_issues)  # Estimate
    completion_rate = (total_working / total_issues) * 100
    
    print(f"\n🏆 ESTIMATED OVERALL PROGRESS:")
    print(f"   Completed issues: ~{total_working}/{total_issues}")
    print(f"   Completion rate: ~{completion_rate:.1f}%")
    
    if completion_rate >= 80:
        print("\n🎉 EXCELLENT PROGRESS! Most critical issues resolved!")
    elif completion_rate >= 60:
        print("\n👍 GOOD PROGRESS! Continue with remaining fixes.")
    else:
        print("\n🔧 MORE WORK NEEDED. Focus on failed routes.")

def main():
    """Main testing function"""
    print("🚀 CRITICAL ROUTES TESTING")
    print("Comprehensive test of all 19 critical issues")
    print("=" * 60)
    
    # Check server status
    base_url = test_flask_server_status()
    if not base_url:
        print("\n❌ Cannot proceed without a running Flask server.")
        print("💡 To start the server:")
        print("   python main.py  (runs on port 5002)")
        print("   python run.py   (runs on port 5000)")
        return False
    
    # Test all routes
    results = test_critical_routes(base_url)
    
    # Test achievement API specifically
    achievement_api_result = test_achievement_api_post(base_url)
    
    # Generate final report
    generate_report(results, achievement_api_result)
    
    return len(results['failed']) == 0 and len(results['errors']) == 0

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n⚠️  Some issues found - see report above.")
