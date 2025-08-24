#!/usr/bin/env python3
"""Quick syntax test for main routes"""

# Test import of main routes
try:
    from app.routes.main import main
    print("✅ Main routes imported successfully")
except SyntaxError as e:
    print(f"❌ Syntax error in main routes: {e}")
except ImportError as e:
    print(f"⚠️ Import error (expected): {e}")
except Exception as e:
    print(f"❌ Other error: {e}")

# Test import of other routes
try:
    from app.routes.stocks import stocks
    print("✅ Stocks routes imported successfully")
except SyntaxError as e:
    print(f"❌ Syntax error in stocks routes: {e}")
except ImportError as e:
    print(f"⚠️ Import error (expected): {e}")
except Exception as e:
    print(f"❌ Other error: {e}")

try:
    from app.routes.analysis import analysis
    print("✅ Analysis routes imported successfully")
except SyntaxError as e:
    print(f"❌ Syntax error in analysis routes: {e}")
except ImportError as e:
    print(f"⚠️ Import error (expected): {e}")
except Exception as e:
    print(f"❌ Other error: {e}")

try:
    from app.routes.portfolio import portfolio
    print("✅ Portfolio routes imported successfully")
except SyntaxError as e:
    print(f"❌ Syntax error in portfolio routes: {e}")
except ImportError as e:
    print(f"⚠️ Import error (expected): {e}")
except Exception as e:
    print(f"❌ Other error: {e}")

print("\n✅ All syntax tests completed!")
