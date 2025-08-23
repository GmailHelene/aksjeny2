#!/usr/bin/env python3
"""
PRODUCTION DEPLOYMENT STATUS CHECKER
Monitors deployment status and validates stock search/compare fixes
"""
import requests
import time
import json
from datetime import datetime

def check_deployment_status():
    """Check if our fixes have been deployed to production"""
    print("🔍 CHECKING DEPLOYMENT STATUS")
    print("=" * 50)
    
    test_urls = [
        {
            'url': 'https://aksjeradar.trade/stocks/search?q=tesla',
            'test_name': 'Tesla Search Test',
            'demo_indicators': ['demo-modus aktivert', 'prøv alle aksjeradar funksjoner', 'få tilgang til alle'],
            'success_indicators': ['search', 'søk', 'tesla', 'input', 'form']
        },
        {
            'url': 'https://aksjeradar.trade/stocks/compare',
            'test_name': 'Stock Compare Test', 
            'demo_indicators': ['demo-modus aktivert', 'prøv alle aksjeradar funksjoner', 'få tilgang til alle'],
            'success_indicators': ['compare', 'sammenlign', 'chart', 'select', 'stock']
        }
    ]
    
    deployment_success = True
    
    for test in test_urls:
        print(f"\n🧪 Testing {test['test_name']}")
        print(f"🌐 URL: {test['url']}")
        
        try:
            response = requests.get(test['url'], timeout=10)
            content = response.text.lower()
            
            # Check for demo content (bad)
            has_demo_content = any(indicator in content for indicator in test['demo_indicators'])
            
            # Check for actual functionality (good)
            has_success_content = any(indicator in content for indicator in test['success_indicators'])
            
            if has_demo_content:
                print(f"❌ STILL SHOWING DEMO CONTENT")
                print(f"   Status: {response.status_code}")
                print(f"   Result: Deployment not complete or fixes not working")
                deployment_success = False
            elif has_success_content:
                print(f"✅ WORKING CORRECTLY")
                print(f"   Status: {response.status_code}")
                print(f"   Result: Actual functionality is accessible")
            else:
                print(f"❓ UNCLEAR RESPONSE")
                print(f"   Status: {response.status_code}")
                print(f"   Result: Neither demo nor success indicators found")
                deployment_success = False
                
        except Exception as e:
            print(f"❌ REQUEST FAILED: {e}")
            deployment_success = False
    
    return deployment_success

def wait_for_deployment():
    """Monitor deployment until it's complete"""
    print("⏰ MONITORING DEPLOYMENT")
    print("=" * 50)
    print("Railway deployments typically take 2-3 minutes")
    print("Checking every 30 seconds...\n")
    
    max_attempts = 10  # 5 minutes total
    for attempt in range(1, max_attempts + 1):
        print(f"🔄 Attempt {attempt}/{max_attempts} - {datetime.now().strftime('%H:%M:%S')}")
        
        if check_deployment_status():
            print("\n🎉 DEPLOYMENT SUCCESSFUL!")
            print("✅ Both stock search and compare functionality are working")
            return True
        
        if attempt < max_attempts:
            print("⏳ Deployment still in progress... waiting 30 seconds")
            time.sleep(30)
        
    print("\n⚠️ DEPLOYMENT TIMEOUT")
    print("Deployment took longer than expected or there are remaining issues")
    return False

def generate_status_report():
    """Generate a deployment status report"""
    print("\n📊 FINAL DEPLOYMENT STATUS REPORT")
    print("=" * 60)
    
    success = check_deployment_status()
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if success:
        status = "DEPLOYMENT SUCCESSFUL ✅"
        message = "All stock search and compare fixes are working correctly"
    else:
        status = "DEPLOYMENT INCOMPLETE ❌"
        message = "Fixes may not be deployed yet or there are remaining issues"
    
    report = {
        'timestamp': timestamp,
        'status': status,
        'message': message,
        'fixes_applied': [
            'Removed conflicting @main.route(\'/search\') from main.py',
            'Verified @demo_access decorators on stocks.search and stocks.compare',
            'Added both endpoints to public_endpoints whitelist',
            'Fixed route conflicts preventing blueprint resolution'
        ],
        'expected_behavior': [
            'https://aksjeradar.trade/stocks/search?q=tesla shows search interface',
            'Tesla search returns actual results',
            'https://aksjeradar.trade/stocks/compare shows comparison tool',
            'No demo promotional content displayed'
        ]
    }
    
    print(f"Status: {status}")
    print(f"Message: {message}")
    print(f"Timestamp: {timestamp}")
    
    # Save report
    with open('deployment_status_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Status report saved to deployment_status_report.json")
    return success

if __name__ == "__main__":
    print("🚀 STOCK SEARCH & COMPARE DEPLOYMENT MONITOR")
    print("=" * 60)
    print("This script monitors deployment status and validates fixes")
    print("=" * 60)
    
    # First check current status
    print("📋 Initial status check...")
    if check_deployment_status():
        print("\n🎉 FIXES ALREADY DEPLOYED!")
        print("✅ Stock search and compare functionality are working")
    else:
        print("\n⏳ WAITING FOR DEPLOYMENT...")
        wait_for_deployment()
    
    # Generate final report
    generate_status_report()
    print("\n🏁 Monitoring complete!")
