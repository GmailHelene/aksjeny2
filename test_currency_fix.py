#!/usr/bin/env python3
"""Test currency data field fix"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.data_service import DataService

print("🔍 Testing currency data fix...")

# Test get_currency_overview
currency_data = DataService.get_currency_overview()
print(f"✅ Currency data returned {len(currency_data)} items")

# Check the first few currency pairs
for symbol, data in list(currency_data.items())[:3]:
    print(f"\n📊 {symbol}:")
    print(f"  - Name: {data.get('name', 'N/A')}")
    print(f"  - Price (old): {data.get('price', 'NOT FOUND')}")
    print(f"  - Last Price (new): {data.get('last_price', 'NOT FOUND')}")
    print(f"  - Change: {data.get('change', 0)}")
    print(f"  - Change %: {data.get('change_percent', 0)}")

# Test enhanced fallback specifically
print("\n🔧 Testing enhanced fallback currency data...")
fallback_data = DataService._get_enhanced_fallback_currency()
print(f"✅ Fallback data returned {len(fallback_data)} items")

for symbol, data in list(fallback_data.items())[:2]:
    print(f"\n📊 Fallback {symbol}:")
    print(f"  - Name: {data.get('name', 'N/A')}")
    print(f"  - Last Price: {data.get('last_price', 'NOT FOUND')}")
    print(f"  - Change: {data.get('change', 0)}")
    print(f"  - Change %: {data.get('change_percent', 0)}")

print("\n✅ Currency field test complete!")
