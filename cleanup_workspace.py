#!/usr/bin/env python3
"""
🧹 AKSJERADAR WORKSPACE CLEANUP
Rydder opp i alle unødvendige test-, backup- og rapport-filer
"""
import os
import glob

def cleanup_workspace():
    print("🧹 WORKSPACE CLEANUP - SLETTER UNØDVENDIGE FILER")
    print("=" * 60)
    
    # Filer og patterns som kan slettes
    files_to_delete = [
        # Test filer
        "actual_issues_analysis.py",
        "analysis_route_auth_test.py", 
        "button_functionality_manual_test.py",
        "color_fix_verification.py",
        "comprehensive_500_verification.py",
        "comprehensive_cache_clearer.py",
        "comprehensive_endpoint_test.py",
        "comprehensive_page_test.py",
        "comprehensive_platform_test.py",
        "comprehensive_production_test.py", 
        "comprehensive_stock_fixes.py",
        "comprehensive_styling_test.py",
        "comprehensive_template_test.py",
        "comprehensive_ui_test.py",
        "complete_production_fix.py",
        
        # Markdown rapporter
        "AKSJERADAR_STATUS_KOMPLETT_OPPDATERT.md",
        "ALLE_KRITISKE_FEIL_KOMPLETT_LØST_FINAL.md",
        "ANALYSIS_PAGES_FIXED_FINAL.md", 
        "ANALYSIS_ROUTE_500_ERRORS_FIXED.md",
        "ANALYSIS_ROUTE_BUILDERROR_FIXED.md",
        "ARBEIDSRAPPORT_OPPDATERING_0208.md",
        "BUILDERROR_CRITICAL_FIX_COMPLETE.md",
        "BUILDERROR_FIXES_COMPLETE.md",
        "BUILDERROR_PORTFOLIO_TIPS_FIXED_FINAL.md",
        "BUY_BUTTON_MOBILE_MENU_FIXES_COMPLETE.md",
        "BUY_STAR_BUTTONS_AND_TEXT_CONTRAST_FIXES_COMPLETE.md",
        "CACHE_404_FIXED_COMPLETE_GUIDE_20250724.md",
        "CACHE_BUSTING_COMPLETE_SOLUTION_20250724.md",
        "COLOR_CONTRAST_FIXES_COMPLETE_REPORT.md",
        "COMPLETE_500_ERROR_FIXES_FINAL_REPORT.md",
        "COMPLETE_FIX_REPORT_20250820.md",
        "COMPLETE_IMPLEMENTATION_FINAL_REPORT.md",
        "COMPLETE_PRODUCTION_FIXES_FINAL_REPORT.md",
        "COMPLETION_REPORT_20250820.md",
        "COMPREHENSIVE_FIXES_COMPLETE_FINAL_REPORT.md",
        "COMPREHENSIVE_FIXES_COMPLETE_FINAL_SUMMARY.md",
        "COMPREHENSIVE_FIXES_COMPLETE_FINAL.md",
        "COMPREHENSIVE_FIXES_FINAL_STATUS.md",
        "COMPREHENSIVE_PLATFORM_FIXES_COMPLETE_FINAL_REPORT.md",
        "COMPREHENSIVE_PLATFORM_FIXES_TODO.md",
        "COMPREHENSIVE_STYLING_AND_NAVIGATION_FIXES_20250821.md",
        "COMPREHENSIVE_STYLING_FIXES_COMPLETE.md",
        "COMPREHENSIVE_UPDATES_COMPLETE_REPORT_20250820.md",
        "500_ERRORS_FIXED_FINAL_REPORT.md",
        "NAVIGATION_FIXES_COMPLETE_REPORT.md",
        
        # Cache og temp filer
        "cache_clear_report.json",
        "commit_message.md",
        "contrast_test.html",
        "convey_test.html",
        "cookies.txt",
        "auth_test.log",
        
        # Script filer (one-time utilities)
        "add_missing_columns.py",
        "add_notification_columns.py", 
        "builderror_scanner.py",
        "check_database.py",
        "check_favorites_table.py",
        "check_real_users.py",
        "cleanup_unused_files.py",
        "clear_all_cache.py",
        "clear_cache.py",
        "clear_production_cache.py"
    ]
    
    deleted_count = 0
    
    # Slett spesifikke filer
    for file_path in files_to_delete:
        if os.path.exists(file_path):
            try:
                print(f"🗑️  Sletter: {file_path}")
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                print(f"❌ Kunne ikke slette {file_path}: {e}")
    
    # Slett app test-filer
    app_test_patterns = [
        "app/*test*.py",
        "app/test_*.py",
        "app/*_test.py"
    ]
    
    for pattern in app_test_patterns:
        files = glob.glob(pattern)
        for file_path in files:
            try:
                print(f"🗑️  Sletter app test: {file_path}")
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                print(f"❌ Kunne ikke slette {file_path}: {e}")
    
    print(f"\n✅ CLEANUP FERDIG!")
    print(f"📊 Slettet {deleted_count} unødvendige filer")
    print("🎉 Workspace er nå ryddig og profesjonell!")
    print("\n💡 Kun nødvendige produksjonsfiler gjenstår")

if __name__ == "__main__":
    cleanup_workspace()
