#!/usr/bin/env python3
"""
Simple syntax check for stocks.py
"""

def check_syntax():
    """Check that stocks.py has valid syntax"""
    try:
        with open('app/routes/stocks.py', 'r') as f:
            code = f.read()
        
        # Compile the code to check for syntax errors
        compile(code, 'app/routes/stocks.py', 'exec')
        print("✅ SUCCESS: stocks.py has valid syntax!")
        return True
        
    except SyntaxError as e:
        print(f"❌ SYNTAX ERROR in stocks.py: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

if __name__ == '__main__':
    check_syntax()
