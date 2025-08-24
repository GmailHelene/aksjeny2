#!/usr/bin/env python3
"""
Test search functionality specifically for Tesla
"""
import sys
import os

# Add app to path
sys.path.insert(0, '/app')

def test_tesla_search():
    """Test Tesla search functionality"""
    try:
        from app import create_app
        from app.services.data_service import FALLBACK_GLOBAL_DATA
        
        app = create_app()
        
        with app.app_context():
            print("🔍 Testing Tesla search functionality...")
            
            # Check if Tesla exists in fallback data
            if 'TSLA' in FALLBACK_GLOBAL_DATA:
                tesla_data = FALLBACK_GLOBAL_DATA['TSLA']
                print(f"✅ TSLA found in FALLBACK_GLOBAL_DATA:")
                print(f"   Name: {tesla_data.get('name', 'N/A')}")
                print(f"   Price: ${tesla_data.get('last_price', 'N/A')}")
                print(f"   Change: {tesla_data.get('change_percent', 'N/A')}%")
            else:
                print("❌ TSLA NOT found in FALLBACK_GLOBAL_DATA")
            
            # Test name mapping
            name_mappings = {
                'tesla': 'TSLA',
                'dnb': 'DNB.OL', 
                'apple': 'AAPL',
                'microsoft': 'MSFT',
                'equinor': 'EQNR.OL',
                'telenor': 'TEL.OL'
            }
            
            if 'tesla' in name_mappings:
                mapped = name_mappings['tesla']
                print(f"✅ 'tesla' maps to '{mapped}'")
                
                if mapped in FALLBACK_GLOBAL_DATA:
                    print(f"✅ Mapped ticker '{mapped}' exists in data")
                else:
                    print(f"❌ Mapped ticker '{mapped}' NOT in data")
            else:
                print("❌ 'tesla' mapping not found")
            
            # Test search simulation
            query = "tesla"
            query_lower = query.lower()
            query_upper = query.upper()
            
            results = []
            
            # Check direct mapping first
            mapped_ticker = name_mappings.get(query_lower)
            if mapped_ticker and mapped_ticker in FALLBACK_GLOBAL_DATA:
                data = FALLBACK_GLOBAL_DATA[mapped_ticker]
                results.append({
                    'ticker': mapped_ticker,
                    'name': data['name'],
                    'price': f"${data['last_price']:.2f}",
                    'change_percent': round(data['change_percent'], 2)
                })
                print(f"✅ Direct mapping result: {results[0]}")
            
            # Search through all data
            for ticker, data in FALLBACK_GLOBAL_DATA.items():
                if (query_upper in ticker or 
                    query_lower in data['name'].lower()):
                    # Skip if already found
                    if not any(r['ticker'] == ticker for r in results):
                        results.append({
                            'ticker': ticker,
                            'name': data['name'],
                            'price': f"${data['last_price']:.2f}",
                            'change_percent': round(data['change_percent'], 2)
                        })
                        print(f"✅ Search match: {ticker} - {data['name']}")
            
            print(f"\n📊 Total results for 'tesla': {len(results)}")
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result['ticker']}: {result['name']} - {result['price']}")
            
            if len(results) > 0:
                print("🎉 Tesla search should work correctly!")
                return True
            else:
                print("❌ Tesla search would return no results")
                return False
                
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_tesla_search()
    sys.exit(0 if success else 1)
