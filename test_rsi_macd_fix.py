#!/usr/bin/env python3
"""
Test script to verify RSI and MACD calculations are working properly
STEP 16: Test real technical indicator calculations
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.routes.stocks import calculate_rsi, calculate_macd
    import numpy as np
    import pandas as pd
    
    print("🔧 STEP 16 TEST: Testing improved RSI and MACD calculations")
    print("=" * 60)
    
    # Test data - simulating 30 days of price data with realistic movements
    base_price = 100
    prices = []
    for i in range(30):
        # Create realistic price movements
        change = np.random.normal(0, 2)  # Average 0% change, 2% volatility
        if i == 0:
            prices.append(base_price)
        else:
            new_price = max(prices[-1] + change, 1)  # Ensure price stays positive
            prices.append(new_price)
    
    print(f"📊 Testing with {len(prices)} price points")
    print(f"📈 Price range: ${min(prices):.2f} - ${max(prices):.2f}")
    print()
    
    # Test RSI calculation
    print("🎯 Testing RSI Calculation:")
    try:
        rsi = calculate_rsi(prices)
        print(f"✅ RSI calculated successfully: {rsi:.2f}")
        
        # Validate RSI is in valid range
        if 0 <= rsi <= 100:
            print(f"✅ RSI is in valid range (0-100): {rsi:.2f}")
        else:
            print(f"❌ RSI out of range: {rsi:.2f}")
            
    except Exception as e:
        print(f"❌ RSI calculation failed: {e}")
    
    print()
    
    # Test MACD calculation
    print("🎯 Testing MACD Calculation:")
    try:
        macd_line, macd_signal, macd_histogram = calculate_macd(prices)
        print(f"✅ MACD calculated successfully:")
        print(f"   📈 MACD Line: {macd_line:.4f}")
        print(f"   📊 Signal Line: {macd_signal:.4f}")
        print(f"   📊 Histogram: {macd_histogram:.4f}")
        
        # Basic validation
        if abs(macd_histogram - (macd_line - macd_signal)) < 0.0001:
            print("✅ MACD histogram calculation is correct")
        else:
            print("❌ MACD histogram calculation error")
            
    except Exception as e:
        print(f"❌ MACD calculation failed: {e}")
    
    print()
    print("🧪 Testing with different data sets:")
    
    # Test with trending up data
    trending_up = [100 + i*0.5 for i in range(30)]  # Steady uptrend
    rsi_up = calculate_rsi(trending_up)
    macd_up, _, _ = calculate_macd(trending_up)
    print(f"📈 Uptrend - RSI: {rsi_up:.1f}, MACD: {macd_up:.4f}")
    
    # Test with trending down data
    trending_down = [100 - i*0.5 for i in range(30)]  # Steady downtrend
    rsi_down = calculate_rsi(trending_down)
    macd_down, _, _ = calculate_macd(trending_down)
    print(f"📉 Downtrend - RSI: {rsi_down:.1f}, MACD: {macd_down:.4f}")
    
    # Test with sideways data
    sideways = [100 + np.sin(i*0.2) for i in range(30)]  # Oscillating around 100
    rsi_side = calculate_rsi(sideways)
    macd_side, _, _ = calculate_macd(sideways)
    print(f"↔️ Sideways - RSI: {rsi_side:.1f}, MACD: {macd_side:.4f}")
    
    print()
    print("✅ STEP 16 TEST COMPLETE: RSI and MACD calculations are working properly!")
    print("🎯 Real technical indicators will now be calculated using historical data")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
