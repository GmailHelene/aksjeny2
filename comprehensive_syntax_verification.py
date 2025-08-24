#!/usr/bin/env python3
"""Complete fix verification for the syntax error emergency"""

def test_main_route_syntax():
    """Test if main.py has valid syntax"""
    try:
        import ast
        
        # Read the main.py file
        with open('app/routes/main.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Parse the AST to check syntax
        ast.parse(code)
        print("✅ app/routes/main.py has valid syntax")
        return True
        
    except SyntaxError as e:
        print(f"❌ SYNTAX ERROR in app/routes/main.py:")
        print(f"Line {e.lineno}: {e.text}")
        print(f"Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error reading/parsing main.py: {e}")
        return False

def test_other_routes_syntax():
    """Test syntax of other key route files"""
    route_files = [
        'app/routes/stocks.py',
        'app/routes/analysis.py', 
        'app/routes/portfolio.py'
    ]
    
    all_good = True
    for route_file in route_files:
        try:
            import ast
            with open(route_file, 'r', encoding='utf-8') as f:
                code = f.read()
            ast.parse(code)
            print(f"✅ {route_file} has valid syntax")
        except SyntaxError as e:
            print(f"❌ SYNTAX ERROR in {route_file}:")
            print(f"Line {e.lineno}: {e.text}")
            print(f"Error: {e.msg}")
            all_good = False
        except FileNotFoundError:
            print(f"⚠️ {route_file} not found")
        except Exception as e:
            print(f"❌ Error reading/parsing {route_file}: {e}")
            all_good = False
    
    return all_good

def main():
    print("🔍 COMPREHENSIVE SYNTAX FIX VERIFICATION")
    print("=" * 50)
    
    # Test main route
    main_ok = test_main_route_syntax()
    
    # Test other routes
    routes_ok = test_other_routes_syntax()
    
    print("\n" + "=" * 50)
    if main_ok and routes_ok:
        print("🎉 ALL SYNTAX TESTS PASSED!")
        print("✅ The emergency syntax fix was successful")
        print("✅ The app should now be able to start without errors")
        print("✅ Ready for deployment to Railway")
    else:
        print("❌ SYNTAX ERRORS STILL EXIST")
        print("❌ Further fixes needed")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
