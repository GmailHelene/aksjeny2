#!/usr/bin/env python3
"""
Quick yfinance test to diagnose the AAPL data issue
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_yfinance_basic():
    """Test basic yfinance functionality"""
    try:
        import yfinance as yf
        print("✅ yfinance imported successfully")
        
        # Test basic AAPL fetch
        print("\n🧪 Testing AAPL data fetch...")
        ticker = yf.Ticker("AAPL")
        
        # Try different approaches
        print("Testing info...")
        try:
            info = ticker.info
            print(f"✅ AAPL info: {info.get('longName', 'N/A')} - ${info.get('regularMarketPrice', 'N/A')}")
        except Exception as e:
            print(f"❌ AAPL info failed: {e}")
        
        print("Testing 1mo history...")
        try:
            hist_1mo = ticker.history(period="1mo")
            print(f"✅ AAPL 1mo history: {len(hist_1mo)} rows")
            if not hist_1mo.empty:
                latest = hist_1mo.iloc[-1]
                print(f"   Latest close: ${latest['Close']:.2f}")
        except Exception as e:
            print(f"❌ AAPL 1mo history failed: {e}")
        
        print("Testing 5d history...")
        try:
            hist_5d = ticker.history(period="5d")
            print(f"✅ AAPL 5d history: {len(hist_5d)} rows")
        except Exception as e:
            print(f"❌ AAPL 5d history failed: {e}")
        
        print("Testing 1d history...")
        try:
            hist_1d = ticker.history(period="1d")
            print(f"✅ AAPL 1d history: {len(hist_1d)} rows")
        except Exception as e:
            print(f"❌ AAPL 1d history failed: {e}")
            
        # Test other symbols
        print("\n🧪 Testing other symbols...")
        for symbol in ["MSFT", "GOOGL", "TSLA", "EQNR.OL"]:
            try:
                test_ticker = yf.Ticker(symbol)
                test_hist = test_ticker.history(period="5d")
                print(f"✅ {symbol}: {len(test_hist)} rows")
            except Exception as e:
                print(f"❌ {symbol}: {e}")
                
    except ImportError:
        print("❌ yfinance not available")
    except Exception as e:
        print(f"❌ yfinance test failed: {e}")

def test_enhanced_service():
    """Test our enhanced yfinance service"""
    try:
        from app.services.enhanced_yfinance_service import EnhancedYFinanceService
        print("\n🔧 Testing EnhancedYFinanceService...")
        
        service = EnhancedYFinanceService()
        
        # Test AAPL with our service
        try:
            hist = service.get_ticker_history("AAPL", period="5d")
            print(f"✅ Enhanced service AAPL: {len(hist)} rows")
        except Exception as e:
            print(f"❌ Enhanced service AAPL failed: {e}")
            
        # Test multiple symbols
        for symbol in ["MSFT", "EQNR.OL"]:
            try:
                hist = service.get_ticker_history(symbol, period="5d")
                print(f"✅ Enhanced service {symbol}: {len(hist)} rows")
            except Exception as e:
                print(f"❌ Enhanced service {symbol}: {e}")
                
    except Exception as e:
        print(f"❌ Enhanced service test failed: {e}")

if __name__ == "__main__":
    print("🔍 YFINANCE DIAGNOSTIC TEST")
    print("=" * 40)
    
    test_yfinance_basic()
    test_enhanced_service()
    
    print("\n" + "=" * 40)
    print("🏁 DIAGNOSTIC COMPLETE")
