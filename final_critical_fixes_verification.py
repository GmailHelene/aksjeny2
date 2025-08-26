#!/usr/bin/env python3
"""
Final Critical Fixes Verification Test
Tests all the fixes we've implemented for the critical 500 errors
"""

import os
import sys
import requests
import json
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_yfinance_fallback():
    """Test the yfinance fallback system"""
    print("🧪 Testing yfinance fallback system...")
    
    try:
        from app.services.enhanced_yfinance_service import EnhancedYFinanceService
        
        service = EnhancedYFinanceService()
        
        # Test with AAPL (most common error)
        print("  Testing AAPL data retrieval...")
        ticker_info = service.get_ticker_info('AAPL')
        
        if ticker_info and 'currentPrice' in ticker_info:
            print(f"  ✅ AAPL info: ${ticker_info['currentPrice']}")
        else:
            print("  ❌ AAPL info failed")
            return False
            
        # Test history
        history = service.get_ticker_history('AAPL', '1y')
        if history is not None and not history.empty:
            print(f"  ✅ AAPL history: {len(history)} data points")
        else:
            print("  ❌ AAPL history failed")
            return False
            
        # Test Norwegian stock
        print("  Testing Norwegian stock (EQNR.OL)...")
        eqnr_info = service.get_ticker_info('EQNR.OL')
        if eqnr_info and 'currentPrice' in eqnr_info:
            print(f"  ✅ EQNR.OL info: {eqnr_info['currentPrice']} NOK")
        else:
            print("  ❌ EQNR.OL info failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ yfinance test failed: {e}")
        return False

def test_price_alert_creation():
    """Test PriceAlert creation (without condition parameter)"""
    print("🧪 Testing PriceAlert creation...")
    
    try:
        # Import the model directly
        sys.path.append('/workspace')
        from app.models import PriceAlert
        
        # Try to create a PriceAlert object manually
        alert = PriceAlert(
            user_id=1,
            symbol='AAPL',
            target_price=180.0,
            alert_type='above',
            is_active=True
        )
        
        print("  ✅ PriceAlert object created successfully")
        print(f"  Alert details: {alert.symbol} @ ${alert.target_price} ({alert.alert_type})")
        return True
        
    except Exception as e:
        print(f"  ❌ PriceAlert creation failed: {e}")
        return False

def test_css_file():
    """Test that CSS file has correct background color"""
    print("🧪 Testing CSS background color fix...")
    
    try:
        css_file = 'app/static/css/text-contrast.css'
        
        if not os.path.exists(css_file):
            print(f"  ❌ CSS file not found: {css_file}")
            return False
            
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for the fixed color
        if '#252525' in content and '.navbar-nav .dropdown-menu' in content:
            print("  ✅ CSS background color is correct (#252525)")
            
            # Check that old color is not present
            if '#333333' in content:
                print("  ⚠️  Warning: Still contains #333333 somewhere")
            
            return True
        else:
            print("  ❌ CSS background color not found or incorrect")
            return False
            
    except Exception as e:
        print(f"  ❌ CSS test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 CRITICAL FIXES VERIFICATION TEST")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        'yfinance_fallback': test_yfinance_fallback(),
        'price_alert_creation': test_price_alert_creation(),
        'css_background_fix': test_css_file()
    }
    
    print()
    print("📊 FINAL RESULTS:")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nSUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL CRITICAL FIXES VERIFIED!")
        print("The main 500 errors should now be resolved.")
    else:
        print("⚠️  Some fixes may need additional work.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
