import os

def delete_file(filepath):
    """Sletter en fil hvis den finnes"""
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            print(f"✅ Slettet: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Kunne ikke slette {filepath}: {e}")
            return False
    else:
        print(f"⚪ Finnes ikke: {filepath}")
        return False

# Liste over testfiler som skal slettes
test_files = [
    # Root test files
    "test_500_errors_comprehensive.py",
    "test_500_fixes.py",
    "test_access_control.py",
    "test_all_fixes.py",
    "test_endpoints.py",
    "test_user.json",
    "test_user_instance.json",
    "subscription_test.log",
    "auth_test.log",
    "contrast_test.html",
    "style_test.html",
    "styling_test.html",
    
    # App test files
    "app/test_app.py",
    "app/basic_test.py",
    "app/startup_test.py",
    "app/production_test.py",
    "app/auth_system_test.py",
    "app/create_test_users.py",
    "app/run_all_tests.py",
    "app/simple_test_server.py",
    "app/tests/test_endpoints.py",
    "app/tests/test_all_endpoints_access.py",
    "app/tests/test_frontend_urls_access.py"
]

print("🗑️ SLETTER TESTFILER FRA WORKSPACE")
print("=" * 50)

deleted_count = 0
for filepath in test_files:
    if delete_file(filepath):
        deleted_count += 1

print(f"\n🎉 Slettet {deleted_count} av {len(test_files)} testfiler!")
print("Workspace opprydding ferdig!")
