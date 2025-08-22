#!/usr/bin/env python3
"""
Simple Forum and Navigation Validation Script
Validates the basic structure and configuration of forum and navigation fixes
"""

import os
import re
from datetime import datetime

def validate_forum_implementation():
    """Validate that forum is properly implemented"""
    print("🔍 FORUM IMPLEMENTATION VALIDATION")
    print("=" * 50)
    
    validation_results = {
        "forum_routes_exist": False,
        "forum_templates_exist": False, 
        "forum_models_exist": False,
        "forum_blueprint_registered": False,
        "navigation_contains_forum": False,
        "footer_cleaned": False,
        "stocks_navigation_updated": False
    }
    
    # Check forum routes
    try:
        with open('app/routes/forum.py', 'r', encoding='utf-8') as f:
            forum_routes = f.read()
        
        if 'def index():' in forum_routes and 'ForumPost.query' in forum_routes:
            validation_results["forum_routes_exist"] = True
            print("✅ Forum routes exist and use real database queries")
        else:
            print("❌ Forum routes missing or incomplete")
    except FileNotFoundError:
        print("❌ Forum routes file not found")
    
    # Check forum templates
    forum_templates = ['index.html', 'create.html', 'view.html', 'category.html']
    try:
        for template in forum_templates:
            if os.path.exists(f'app/templates/forum/{template}'):
                validation_results["forum_templates_exist"] = True
        if validation_results["forum_templates_exist"]:
            print("✅ Forum templates exist")
        else:
            print("❌ Forum templates missing")
    except:
        print("❌ Error checking forum templates")
    
    # Check forum models
    try:
        with open('app/models/forum.py', 'r', encoding='utf-8') as f:
            forum_models = f.read()
        
        if 'class ForumPost(' in forum_models and 'class ForumCategory(' in forum_models:
            validation_results["forum_models_exist"] = True
            print("✅ Forum models exist")
        else:
            print("❌ Forum models incomplete")
    except FileNotFoundError:
        print("❌ Forum models file not found")
    
    # Check forum blueprint registration
    try:
        with open('app/__init__.py', 'r', encoding='utf-8') as f:
            init_content = f.read()
        
        if "('.routes.forum', 'forum', '/forum')" in init_content:
            validation_results["forum_blueprint_registered"] = True
            print("✅ Forum blueprint registered correctly")
        else:
            print("❌ Forum blueprint not registered")
    except FileNotFoundError:
        print("❌ Unable to check blueprint registration")
    
    return validation_results

def validate_navigation_fixes():
    """Validate navigation and footer fixes"""
    print("\\n🧭 NAVIGATION FIXES VALIDATION")
    print("=" * 50)
    
    validation_results = {
        "navigation_contains_forum": False,
        "footer_cleaned": False,
        "stocks_navigation_updated": False
    }
    
    try:
        with open('app/templates/base.html', 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # Check for Resources dropdown with Forum link
        if 'Resources' in base_content and 'Forum' in base_content:
            if "url_for('forum.index')" in base_content:
                validation_results["navigation_contains_forum"] = True
                print("✅ Navigation contains Resources dropdown with Forum link")
            else:
                print("❌ Forum link not properly configured in navigation")
        else:
            print("❌ Resources dropdown or Forum link missing from navigation")
        
        # Check footer cleanup
        if 'Læring & Guider' not in base_content and 'Om Aksjeradar' not in base_content:
            validation_results["footer_cleaned"] = True
            print("✅ Footer headers removed successfully")
        else:
            print("❌ Footer headers still present")
        
        # Check stocks navigation update
        if "url_for('stocks.index')" in base_content and 'Oversikt' in base_content:
            validation_results["stocks_navigation_updated"] = True
            print("✅ Stocks navigation updated with Oversikt as first item")
        else:
            print("❌ Stocks navigation not properly updated")
            
    except FileNotFoundError:
        print("❌ Unable to check base template")
    
    return validation_results

def validate_mock_data_separation():
    """Check that mock data is properly separated from real data"""
    print("\\n📊 MOCK DATA SEPARATION VALIDATION") 
    print("=" * 50)
    
    # Check forum routes for mock data
    try:
        with open('app/routes/forum.py', 'r', encoding='utf-8') as f:
            forum_content = f.read()
        
        mock_indicators = ['mock', 'fake', 'dummy', 'demo', 'placeholder']
        has_mock_data = any(indicator in forum_content.lower() for indicator in mock_indicators)
        
        if not has_mock_data:
            print("✅ Forum routes are clean of mock data")
        else:
            print("⚠️  Forum routes may contain demo/mock data references")
            
    except FileNotFoundError:
        print("❌ Unable to check forum routes for mock data")

def run_comprehensive_validation():
    """Run all validation checks"""
    
    print("🚀 COMPREHENSIVE FORUM & NAVIGATION VALIDATION")
    print("=" * 60)
    print(f"Validation started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all validations
    forum_results = validate_forum_implementation()
    nav_results = validate_navigation_fixes()
    validate_mock_data_separation()
    
    # Overall assessment
    print("\\n📋 VALIDATION SUMMARY")
    print("=" * 40)
    
    all_results = {**forum_results, **nav_results}
    passed = sum(all_results.values())
    total = len(all_results)
    
    print(f"Passed: {passed}/{total} checks")
    print(f"Success rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\\n🎉 ALL VALIDATIONS PASSED!")
        print("✅ Forum functionality should work correctly")
        print("✅ Navigation fixes are properly implemented") 
        print("✅ No 500 errors expected from forum access")
    elif passed >= total * 0.8:
        print("\\n⚠️  MOSTLY SUCCESSFUL - Minor issues detected")
        print("✅ Core functionality should work")
        print("⚠️  Some improvements may be needed")
    else:
        print("\\n❌ SIGNIFICANT ISSUES DETECTED")
        print("❌ Forum may experience 500 errors")
        print("❌ Navigation fixes incomplete")
    
    # Specific recommendations
    print("\\n💡 RECOMMENDATIONS")
    print("-" * 30)
    
    if not all_results.get("forum_blueprint_registered", False):
        print("🔧 Register forum blueprint in app/__init__.py")
    
    if not all_results.get("navigation_contains_forum", False):
        print("🔧 Add Forum link to Resources dropdown in navigation")
    
    if not all_results.get("footer_cleaned", False):
        print("🔧 Remove footer header texts")
    
    if not all_results.get("stocks_navigation_updated", False):
        print("🔧 Update stocks navigation to prioritize Oversikt")
    
    print("\\n✅ Validation complete!")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_validation()
    exit(0 if success else 1)
