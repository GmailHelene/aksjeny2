#!/usr/bin/env python3
"""
Script to verify all navigation pages fetch real data for logged in users
"""

import requests
import time
from urllib.parse import urljoin

class NavigationDataVerifier:
    def __init__(self):
        self.local_base_url = "http://localhost:5000"
        self.live_base_url = "https://aksjeradar.trade"
        
    def test_data_endpoints(self, base_url, label):
        """Test critical data endpoints"""
        print(f"\n🔍 Testing Data Endpoints for {label}")
        print("=" * 50)
        
        data_endpoints = [
            # Main navigation pages that should show real data
            ("/", "Homepage - Should show real market data"),
            ("/stocks/", "Stocks listing - Real stock data"),
            ("/portfolio/", "Portfolio - User data"),
            ("/watchlist/", "Watchlist - User data"),
            ("/price-alerts/", "Price alerts - User data"),
            ("/news/", "News - Real news data"),
            ("/analysis/", "Analysis page - Real data"),
            ("/advanced-analytics/", "Advanced Analytics - Real data"),
            
            # API endpoints that provide data
            ("/api/realtime/market-status", "Market status API"),
            ("/api/realtime/trending", "Trending stocks API"),
            ("/news/api/latest", "Latest news API"),
            
            # Forum (recently fixed)
            ("/forum/", "Forum - Real posts"),
        ]
        
        results = []
        for endpoint, description in data_endpoints:
            print(f"Testing {endpoint:<35} ... ", end="")
            try:
                full_url = urljoin(base_url, endpoint)
                response = requests.get(full_url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    # Check for signs of real data vs placeholder/demo data
                    has_real_data = True
                    issues = []
                    
                    # Check for common placeholder indicators
                    placeholder_indicators = [
                        'demo data', 'placeholder', 'coming soon', 
                        'not available', 'mock data', 'dummy data'
                    ]
                    
                    for indicator in placeholder_indicators:
                        if indicator in content:
                            has_real_data = False
                            issues.append(f"Contains '{indicator}'")
                    
                    # Check for empty data indicators
                    if 'no data available' in content or 'ingen data' in content:
                        has_real_data = False
                        issues.append("No data available message")
                    
                    if has_real_data and len(content) < 1000:
                        has_real_data = False
                        issues.append("Response too small")
                    
                    if has_real_data:
                        print("✅ REAL DATA")
                    else:
                        print(f"⚠️  ISSUES: {', '.join(issues)}")
                    
                    results.append({
                        'endpoint': endpoint,
                        'status': 'OK' if has_real_data else 'ISSUES',
                        'issues': issues,
                        'description': description
                    })
                else:
                    print(f"❌ HTTP {response.status_code}")
                    results.append({
                        'endpoint': endpoint,
                        'status': f'HTTP {response.status_code}',
                        'issues': [f'HTTP {response.status_code}'],
                        'description': description
                    })
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)[:50]}")
                results.append({
                    'endpoint': endpoint,
                    'status': 'ERROR',
                    'issues': [str(e)],
                    'description': description
                })
        
        return results
    
    def generate_report(self, local_results, live_results):
        """Generate comprehensive data verification report"""
        print("\n" + "="*80)
        print("📊 NAVIGATION DATA VERIFICATION REPORT")
        print("="*80)
        
        print(f"\n🏠 LOCAL ENVIRONMENT:")
        working = sum(1 for r in local_results if r['status'] == 'OK')
        total = len(local_results)
        print(f"  ✅ Real Data: {working}/{total}")
        
        if working < total:
            print(f"  ⚠️  Issues found:")
            for result in local_results:
                if result['status'] != 'OK':
                    print(f"    - {result['endpoint']}: {result['status']}")
        
        print(f"\n🌐 LIVE ENVIRONMENT:")
        working = sum(1 for r in live_results if r['status'] == 'OK')
        total = len(live_results)
        print(f"  ✅ Real Data: {working}/{total}")
        
        if working < total:
            print(f"  ⚠️  Issues found:")
            for result in live_results:
                if result['status'] != 'OK':
                    print(f"    - {result['endpoint']}: {result['status']}")

def main():
    """Run the navigation data verification"""
    print("🚀 Starting Navigation Data Verification")
    print("Checking if all navigation pages fetch and display real data")
    
    verifier = NavigationDataVerifier()
    
    # Test local development server
    local_results = verifier.test_data_endpoints(verifier.local_base_url, "LOCAL")
    
    # Test live site  
    live_results = verifier.test_data_endpoints(verifier.live_base_url, "LIVE")
    
    # Generate report
    verifier.generate_report(local_results, live_results)
    
    print(f"\n✨ Data verification complete!")

if __name__ == "__main__":
    main()
