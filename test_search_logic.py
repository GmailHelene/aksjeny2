"""
Manual test of search functionality logic
"""

def test_search_logic():
    """Test the search logic manually"""
    
    print("🔍 Testing Search Functionality Logic")
    print("=" * 50)
    
    # Mock the fallback data (simplified)
    FALLBACK_GLOBAL_DATA = {
        'TSLA': {
            'name': 'Tesla Inc.',
            'last_price': 230.10,
            'change_percent': 2.5,
            'sector': 'Technology'
        },
        'AAPL': {
            'name': 'Apple Inc.',
            'last_price': 185.70,
            'change_percent': 0.67,
            'sector': 'Technology'
        }
    }
    
    FALLBACK_OSLO_DATA = {
        'DNB.OL': {
            'name': 'DNB Bank ASA',
            'last_price': 212.80,
            'change_percent': -0.56,
            'sector': 'Finance'
        },
        'EQNR.OL': {
            'name': 'Equinor ASA',
            'last_price': 342.55,
            'change_percent': 0.68,
            'sector': 'Energy'
        }
    }
    
    # Test different search queries
    test_queries = ['tesla', 'TSLA', 'dnb', 'apple', 'equinor']
    
    for query in test_queries:
        print(f"\n🔎 Testing search for: '{query}'")
        
        # Mimic the search logic from stocks.py
        all_results = []
        query_lower = query.lower()
        query_upper = query.upper()
        
        # Enhanced name mappings
        name_mappings = {
            'tesla': 'TSLA',
            'dnb': 'DNB.OL', 
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'equinor': 'EQNR.OL',
        }
        
        # Check direct name mapping first
        mapped_ticker = name_mappings.get(query_lower)
        if mapped_ticker:
            print(f"   ✅ Found direct mapping: '{query}' -> '{mapped_ticker}'")
            if mapped_ticker in FALLBACK_GLOBAL_DATA:
                data = FALLBACK_GLOBAL_DATA[mapped_ticker]
                all_results.append({
                    'ticker': mapped_ticker,
                    'symbol': mapped_ticker,
                    'name': data['name'],
                    'market': 'NASDAQ',
                    'price': f"{data['last_price']:.2f} USD",
                    'change_percent': data['change_percent'],
                    'sector': data['sector']
                })
            elif mapped_ticker in FALLBACK_OSLO_DATA:
                data = FALLBACK_OSLO_DATA[mapped_ticker]
                all_results.append({
                    'ticker': mapped_ticker,
                    'symbol': mapped_ticker,
                    'name': data['name'],
                    'market': 'Oslo Børs',
                    'price': f"{data['last_price']:.2f} NOK",
                    'change_percent': data['change_percent'],
                    'sector': data['sector']
                })
        
        # Search through Oslo Børs data
        for ticker, data in FALLBACK_OSLO_DATA.items():
            # Skip if already found via mapping
            if any(r['ticker'] == ticker for r in all_results):
                continue
                
            if (query_upper in ticker or 
                query_lower in data['name'].lower() or
                query_upper in data['name'].upper()):
                all_results.append({
                    'ticker': ticker,
                    'symbol': ticker,
                    'name': data['name'],
                    'market': 'Oslo Børs',
                    'price': f"{data['last_price']:.2f} NOK",
                    'change_percent': data['change_percent'],
                    'sector': data['sector']
                })
        
        # Search through global data
        for ticker, data in FALLBACK_GLOBAL_DATA.items():
            # Skip if already found via mapping
            if any(r['ticker'] == ticker for r in all_results):
                continue
                
            if (query_upper in ticker or 
                query_lower in data['name'].lower() or
                query_upper in data['name'].upper()):
                all_results.append({
                    'ticker': ticker,
                    'symbol': ticker,
                    'name': data['name'],
                    'market': 'NASDAQ',
                    'price': f"{data['last_price']:.2f} USD",
                    'change_percent': data['change_percent'],
                    'sector': data['sector']
                })
        
        print(f"   📊 Results found: {len(all_results)}")
        for result in all_results:
            print(f"      - {result['ticker']}: {result['name']} ({result['market']})")
    
    print("\n" + "=" * 50)
    print("🎯 CONCLUSION:")
    print("The search logic should work correctly.")
    print("If users see 'Ingen resultater funnet', the issue is likely:")
    print("1. Import errors in the route (fallback data not loading)")
    print("2. Exception being caught and returning empty results")
    print("3. Template rendering issues")
    print("4. Access control redirecting before search executes")

if __name__ == "__main__":
    test_search_logic()
