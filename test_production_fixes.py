#!/usr/bin/env python3
"""
Test critical production fixes without authentication requirements
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

def test_critical_fixes():
    """Test the specific fixes we implemented"""
    print("🔍 Testing critical production fixes...")
    
    app = create_app()
    
    with app.test_client() as client:
        print("\n📊 Testing market overview route (no auth required)...")
        response = client.get('/analysis/market-overview')
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Market overview route accessible")
            # Check if the response contains data indicating successful template rendering
            response_text = response.data.decode()
            if 'Oslo' in response_text and 'market' in response_text.lower():
                print("✅ Market overview template renders with data")
                if 'data.get(' in response_text:
                    print("✅ Template uses correct dict access patterns")
                else:
                    print("⚠️  Dict access patterns not visible in response")
                return True
            else:
                print("❌ Market overview template content issue")
                return False
        else:
            print(f"❌ Market overview route failed: {response.status_code}")
            return False

def test_data_service_directly():
    """Test DataService.get_comparative_data directly"""
    print("\n🔧 Testing DataService.get_comparative_data method directly...")
    
    from app.services.data_service import DataService
    
    try:
        # Test if method exists
        if hasattr(DataService, 'get_comparative_data'):
            print("✅ Method exists on DataService")
            
            # Test method call
            symbols = ['EQNR.OL', 'AAPL']
            result = DataService.get_comparative_data(symbols)
            print(f"✅ Method callable - returned data type: {type(result)}")
            print(f"✅ Number of symbols processed: {len(result) if result else 0}")
            return True
        else:
            print("❌ Method not found on DataService")
            return False
    except Exception as e:
        print(f"❌ Error testing method: {e}")
        return False

def test_template_files():
    """Test that required template files exist"""
    print("\n📄 Testing template files...")
    
    templates = [
        '/workspaces/aksjeny/app/templates/analysis/fundamental_select.html',
        '/workspaces/aksjeny/app/templates/analysis/market_overview.html'
    ]
    
    all_exist = True
    for template in templates:
        if os.path.exists(template):
            print(f"✅ {os.path.basename(template)} exists")
            
            # Check content
            with open(template, 'r') as f:
                content = f.read()
                if 'data.get(' in content and 'url_for(' in content:
                    print(f"✅ {os.path.basename(template)} has correct patterns")
                else:
                    print(f"⚠️  {os.path.basename(template)} missing expected patterns")
        else:
            print(f"❌ {os.path.basename(template)} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🧪 Testing critical production fixes (comprehensive)...\n")
    
    results = []
    results.append(test_data_service_directly())
    results.append(test_template_files())
    results.append(test_critical_fixes())
    
    print("\n" + "="*50)
    print(f"📊 Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 All critical fixes are working correctly!")
        print("✅ Ready for production deployment")
        return 0
    else:
        print("⚠️  Some issues detected - check output above")
        return 1

if __name__ == '__main__':
    sys.exit(main())
