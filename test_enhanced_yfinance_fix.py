#!/usr/bin/env python3
"""
Test import of enhanced_yfinance_service after fix
"""

import sys
import os

# Add current directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing enhanced_yfinance_service import...")
    from app.services.enhanced_yfinance_service import EnhancedYFinanceService
    print("✅ Successfully imported EnhancedYFinanceService")
    
    # Test instantiation
    service = EnhancedYFinanceService()
    print("✅ Successfully created EnhancedYFinanceService instance")
    
    print("✅ enhanced_yfinance_service fix is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
