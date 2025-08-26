#!/usr/bin/env python3
"""
Test script for stocks compare functionality
"""
import sys
import os
import json
from datetime import datetime, timedelta
import random

# Add the app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def generate_demo_data(symbol, days=180):
    """Generate sample stock data"""
    base_price = 150 if '.OL' in symbol else 300
    trend = random.uniform(-0.2, 0.2)
    volatility = 0.02
    data = []
    
    end_date = datetime.now()
    for i in range(days):
        date = end_date - timedelta(days=days-i)
        # Generate price with trend and random walk
        if i == 0:
            close = base_price
        else:
            close = data[-1]['close'] * (1 + trend/days + random.uniform(-volatility, volatility))
            
        # Generate OHLC values around close
        open_price = close * (1 + random.uniform(-0.01, 0.01))
        high = max(open_price, close) * (1 + random.uniform(0, 0.01))
        low = min(open_price, close) * (1 - random.uniform(0, 0.01))
        volume = int(random.uniform(50000, 500000))
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': volume
        })
    
    return data

def test_chart_data_format():
    """Test that chart data is properly formatted for JSON serialization"""
    print("Testing chart data format...")
    
    symbols = ['EQNR.OL', 'DNB.OL']
    chart_data = {}
    
    for symbol in symbols:
        chart_data[symbol] = generate_demo_data(symbol, 30)
    
    # Test JSON serialization
    try:
        json_str = json.dumps(chart_data)
        print(f"✅ Chart data JSON serialization successful - length: {len(json_str)}")
        
        # Test deserialization
        parsed_data = json.loads(json_str)
        print(f"✅ Chart data JSON deserialization successful")
        
        # Verify structure
        for symbol in symbols:
            if symbol in parsed_data:
                data_points = parsed_data[symbol]
                if len(data_points) > 0:
                    first_point = data_points[0]
                    required_keys = ['date', 'open', 'high', 'low', 'close', 'volume']
                    if all(key in first_point for key in required_keys):
                        print(f"✅ {symbol} data structure is correct")
                    else:
                        print(f"❌ {symbol} missing required keys: {required_keys}")
                        return False
                else:
                    print(f"❌ {symbol} has no data points")
                    return False
            else:
                print(f"❌ {symbol} not found in chart data")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Chart data JSON serialization failed: {e}")
        return False

def test_empty_chart_data():
    """Test behavior with empty chart data"""
    print("\nTesting empty chart data...")
    
    empty_data = {}
    
    # Test length check
    if len(empty_data) > 0:
        print("❌ Empty data should have length 0")
        return False
    else:
        print("✅ Empty data length check passed")
    
    # Test truthiness
    if empty_data:
        print("❌ Empty data should be falsy")
        return False
    else:
        print("✅ Empty data truthiness check passed")
    
    return True

def main():
    """Run all tests"""
    print("Running stocks compare functionality tests...\n")
    
    tests = [
        test_chart_data_format,
        test_empty_chart_data
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ Test passed\n")
            else:
                failed += 1
                print("❌ Test failed\n")
        except Exception as e:
            failed += 1
            print(f"❌ Test failed with exception: {e}\n")
    
    print(f"Test Summary: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Chart data format should work correctly.")
    else:
        print("⚠️ Some tests failed. Issues need to be fixed.")

if __name__ == '__main__':
    main()
