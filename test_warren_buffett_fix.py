#!/usr/bin/env python3
"""
Test Warren Buffett analysis fix
"""
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.services.buffett_analyzer import BuffettAnalyzer
    
    # Test the analyzer
    print("Testing Warren Buffett Analyzer...")
    
    # Test with different symbols
    test_symbols = ['AAPL', 'EQNR.OL', 'TEL.OL']
    
    for symbol in test_symbols:
        print(f"\nTesting {symbol}:")
        try:
            result = BuffettAnalyzer.analyze_stock(symbol)
            if result and isinstance(result, dict):
                # Check if metrics field exists
                if 'metrics' in result:
                    print(f"✅ {symbol}: Has 'metrics' field")
                    metrics = result['metrics']
                    required_fields = ['roe', 'profit_margin', 'revenue_growth', 'debt_ratio']
                    for field in required_fields:
                        if field in metrics:
                            print(f"  ✅ {field}: {metrics[field]}")
                        else:
                            print(f"  ❌ Missing field: {field}")
                else:
                    print(f"❌ {symbol}: Missing 'metrics' field")
                    print(f"Available fields: {list(result.keys())}")
                    
                # Check buffett_score
                if 'buffett_score' in result:
                    print(f"✅ {symbol}: Has 'buffett_score': {result['buffett_score']}")
                else:
                    print(f"❌ {symbol}: Missing 'buffett_score'")
                    
            else:
                print(f"❌ {symbol}: No result or wrong type")
                
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")
    
    print("\n" + "="*50)
    print("Warren Buffett Analyzer Test Complete")
    print("="*50)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ General error: {e}")
