#!/usr/bin/env python3
"""
Test complete app startup after enhanced_yfinance_service fix
"""

import sys
import os

# Add current directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing complete app import chain...")
    
    print("1. Testing enhanced_yfinance_service...")
    from app.services.enhanced_yfinance_service import EnhancedYFinanceService
    print("   ✅ Enhanced YFinance Service imported")
    
    print("2. Testing data_service...")  
    from app.services.data_service import DataService
    print("   ✅ Data Service imported")
    
    print("3. Testing stocks route...")
    from app.routes.stocks import stocks
    print("   ✅ Stocks route imported")
    
    print("4. Testing portfolio route...")
    from app.routes.portfolio import portfolio  
    print("   ✅ Portfolio route imported")
    
    print("5. Testing create_app...")
    from app import create_app
    print("   ✅ create_app imported")
    
    print("6. Creating app instance...")
    app = create_app('development')
    print("   ✅ App created successfully")
    
    print("\n🎉 ALL IMPORT CHAIN TESTS PASSED!")
    print("✅ The enhanced_yfinance_service fix has resolved the deployment error!")
    
except Exception as e:
    print(f"❌ Error at step: {e}")
    import traceback
    traceback.print_exc()
