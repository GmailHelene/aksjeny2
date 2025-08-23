#!/usr/bin/env python3
"""
Enkel testfil sletter - sletter spesifikke testfiler fra workspace
"""

import os

def main():
    # Alle testfiler vi vil slette
    test_files = [
        # Root directory test files
        "test_500_errors_comprehensive.py",
        "test_500_fixes.py", 
        "test_500_fixes_verification.py",
        "test_access_control.py",
        "test_achievement_api.py",
        "test_actual_issues.py",
        "test_add_columns.py",
        "test_ai_predictions.py",
        "test_all_critical_routes.py",
        "test_all_fixes.py",
        "test_all_issues.py",
        "test_app_loads.py",
        "test_auth_debug.py",
        "test_blueprint_import.py",
        "test_builderror_fix.py",
        "test_button_functionality.py",
        "test_button_functionality_comprehensive.py",
        "test_buy_button_mobile_fixes.py",
        "test_chart_api.py",
        "test_chart_api_fix.py",
        "test_chart_components.py",
        "test_color_fixes.py",
        "test_compare.py",
        "test_compare_fix.py",
        "test_comparison.py",
        "test_comparison_page.py",
        "test_complete_import_chain.py",
        "test_comprehensive.py",
        "test_comprehensive_fixes.py",
        "test_comprehensive_user_issues.py",
        "test_contrast_fixes.py",
        "test_critical_fixes.py",
        "test_critical_issues.py",
        "test_critical_routes.py",
        "test_critical_routes_comprehensive.py",
        "test_csrf_login.py",
        "test_current_issues.py",
        "test_dashboard_with_user.py",
        "test_database_fix.py",
        "test_endpoints.py",
        "test_enhanced_yfinance_fix.py",
        "test_favorites_api.py",
        "test_favorites_debug.py",
        "test_fix.py",
        "test_fixes.py",
        "test_fixes_verification.py",
        
        # Andre test filer
        "test_user.json",
        "test_user_instance.json",
        "subscription_test.log",
        "auth_test.log",
        "endpoint_test_output.txt",
        "endpoint_test_report.json",
        "endpoint_test_results.json",
        "navigation-test.html",
        "style_test.html",
        "styling_test.html",
        "contrast_test.html"
    ]
    
    deleted_count = 0
    
    print("🗑️ SLETTER TESTFILER...")
    print("=" * 40)
    
    for filename in test_files:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"✅ Slettet: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Feil: {filename} - {e}")
        else:
            print(f"⚪ Ikke funnet: {filename}")
    
    print(f"\n🎉 Slettet {deleted_count} testfiler!")

if __name__ == "__main__":
    main()
