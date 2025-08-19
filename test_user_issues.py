#!/usr/bin/env python3
"""
Test script to verify the fixes for user reported issues:
1. Market overview showing fake data instead of real data
2. TradingView invalid symbol error for EQNR.OL
"""

import requests
import json
import sys

def test_market_overview_real_data():
    """Test that market overview returns real data, not fake data"""
    print("🔍 Testing Market Overview - Real Data Check")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5002/api/market/overview", timeout=10)
        if response.status_code != 200:
            print(f"❌ Market Overview API failed: {response.status_code}")
            return False
            
        data = response.json()
        
        # Check Oslo stocks for real data indicators
        oslo_stocks = data.get('oslo_stocks', {})
        if not oslo_stocks:
            print("❌ No Oslo Børs stocks found in market overview")
            return False
            
        # Check for EQNR.OL specifically (user's example)
        eqnr_data = oslo_stocks.get('EQNR.OL', {})
        if not eqnr_data:
            print("❌ EQNR.OL not found in Oslo Børs data")
            return False
            
        # Check for real data indicators
        price = eqnr_data.get('last_price', 0)
        source = eqnr_data.get('source', '')
        change = eqnr_data.get('change', 0)
        volume = eqnr_data.get('volume', 0)
        
        print(f"✅ EQNR.OL found in market overview:")
        print(f"   📊 Price: {price} NOK")
        print(f"   📈 Change: {change}")
        print(f"   📦 Volume: {volume}")
        print(f"   🔗 Source: {source}")
        
        # Check if this looks like real data (not the old fake "1,234.56" pattern)
        if price > 0 and price != 1234.56 and "REAL DATA" in source:
            print("✅ Market overview is using REAL data from DataService")
            return True
        else:
            print("❌ Market overview appears to be using fake/demo data")
            return False
            
    except Exception as e:
        print(f"❌ Error testing market overview: {e}")
        return False

def test_eqnr_stock_api():
    """Test that EQNR.OL returns real data via direct API"""
    print("\n🔍 Testing EQNR.OL Direct API - Real Data Check")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5002/api/stock/EQNR.OL", timeout=10)
        if response.status_code != 200:
            print(f"❌ EQNR.OL API failed: {response.status_code}")
            return False
            
        data = response.json()
        
        price = data.get('last_price', 0)
        source = data.get('data_source', '')
        volume = data.get('volume', 0)
        timestamp = data.get('timestamp', '')
        
        print(f"✅ EQNR.OL API Response:")
        print(f"   📊 Price: {price} NOK")
        print(f"   📦 Volume: {volume}")
        print(f"   🔗 Source: {source}")
        print(f"   ⏰ Timestamp: {timestamp}")
        
        if price > 0 and "REAL DATA" in source and volume > 0:
            print("✅ EQNR.OL API is returning REAL data")
            return True
        else:
            print("❌ EQNR.OL API appears to be using fake/demo data")
            return False
            
    except Exception as e:
        print(f"❌ Error testing EQNR.OL API: {e}")
        return False

def test_tradingview_symbol_access():
    """Test that TradingView technical analysis page loads for EQNR.OL"""
    print("\n🔍 Testing TradingView Technical Analysis Page")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5002/analysis/technical/?symbol=EQNR.OL", timeout=10)
        if response.status_code != 200:
            print(f"❌ Technical analysis page failed: {response.status_code}")
            return False
            
        html_content = response.text
        
        # Check for TradingView widget presence
        if "TradingView.widget" in html_content:
            print("✅ TradingView widget found in technical analysis page")
            
            # Check for proper symbol mapping logic (not literal OSL:EQNR, but the mapping code)
            has_symbol_mapping = ".endsWith('.OL')" in html_content
            has_osl_mapping = "OSL:" in html_content
            has_symbol_variable = "const symbol = 'EQNR.OL'" in html_content
            
            print(f"   📋 Has .OL symbol detection: {has_symbol_mapping}")
            print(f"   📋 Has OSL: prefix mapping: {has_osl_mapping}")
            print(f"   📋 Has symbol variable set: {has_symbol_variable}")
            
            if has_symbol_mapping and has_osl_mapping and has_symbol_variable:
                print("✅ Symbol mapping logic found (EQNR.OL → OSL:EQNR)")
                
                # Check for enhanced debugging
                if "console.log" in html_content and "TradingView" in html_content:
                    print("✅ Enhanced debugging code found for TradingView troubleshooting")
                    return True
                else:
                    print("⚠️ TradingView widget present but missing enhanced debugging")
                    return True
            else:
                print("❌ Symbol mapping logic incomplete or missing")
                return False
        else:
            print("❌ TradingView widget not found in technical analysis page")
            return False
            
    except Exception as e:
        print(f"❌ Error testing TradingView page: {e}")
        return False

def main():
    """Run all tests and report results"""
    print("🚀 Testing User Reported Issues - Fix Verification")
    print("=" * 60)
    print("Issue 1: Market overview showing fake data instead of real data")
    print("Issue 2: TradingView 'invalid symbol' error for EQNR.OL")
    print("=" * 60)
    
    tests = [
        ("Market Overview Real Data", test_market_overview_real_data),
        ("EQNR.OL Direct API", test_eqnr_stock_api), 
        ("TradingView Technical Analysis", test_tradingview_symbol_access)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED - User issues have been resolved!")
        print("✅ Market overview now shows REAL data from DataService")
        print("✅ TradingView integration enhanced with proper symbol mapping")
        return 0
    else:
        print(f"\n⚠️ {failed} test(s) failed - issues may need additional work")
        return 1

if __name__ == "__main__":
    sys.exit(main())
