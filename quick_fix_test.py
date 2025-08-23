#!/usr/bin/env python3
"""
Quick verification of the three user-reported issues
"""

import sys
import os

# Add current directory to Python path  
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def quick_test():
    """Quick test of the three problematic routes"""
    try:
        from app import create_app
        
        app = create_app()
        
        print("🔧 QUICK FIX VERIFICATION")
        print("=" * 40)
        
        with app.test_client() as client:
            
            # Test the three specific routes
            tests = [
                ('/analysis/tradingview', 'TradingView charts'),
                ('/analysis/warren-buffett?ticker=TEL.OL', 'Warren Buffett with TEL.OL'),
                ('/analysis/sentiment?symbol=FLNG.OL', 'Sentiment with FLNG.OL')
            ]
            
            all_passed = True
            
            for url, description in tests:
                print(f"\n✅ Testing: {description}")
                print(f"   URL: {url}")
                
                try:
                    response = client.get(url)
                    
                    if response.status_code == 200:
                        print(f"   ✅ Status: 200 OK")
                        
                        # Check for 500 error content
                        content = response.get_data(as_text=True)
                        if '500' in content or 'Internal Server Error' in content:
                            print(f"   ❌ Contains 500 error content")
                            all_passed = False
                        else:
                            print(f"   ✅ No error content detected")
                            
                    elif response.status_code == 500:
                        print(f"   ❌ Status: 500 Internal Server Error")
                        all_passed = False
                        
                    else:
                        print(f"   ⚠️ Status: {response.status_code}")
                        
                except Exception as e:
                    print(f"   ❌ Exception: {str(e)}")
                    all_passed = False
            
            print("\n" + "=" * 40)
            if all_passed:
                print("🎉 ALL TESTS PASSED!")
                print("✅ TradingView: Should load (charts may need network)")
                print("✅ Warren Buffett: TEL.OL analysis should work")
                print("✅ Sentiment: FLNG.OL analysis should work")
            else:
                print("⚠️ Some tests failed - check output above")
                
            return all_passed
            
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return False

if __name__ == '__main__':
    quick_test()
