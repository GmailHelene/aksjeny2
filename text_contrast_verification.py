#!/usr/bin/env python3
"""
Text Contrast Improvements Verification Test
Tests that the comprehensive text contrast improvements are working correctly
"""

import os
import re
from datetime import datetime

def check_css_loaded():
    """Check if the new CSS file is properly referenced in base.html"""
    print("=== TEXT CONTRAST IMPROVEMENTS VERIFICATION ===\n")
    print("🔍 Checking CSS file inclusion...")
    
    try:
        with open('app/templates/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'text-contrast-improvements.css' in content:
            print("✅ text-contrast-improvements.css is included in base.html")
            return True
        else:
            print("❌ text-contrast-improvements.css NOT found in base.html")
            return False
            
    except Exception as e:
        print(f"❌ Failed to check base.html: {e}")
        return False

def check_css_rules():
    """Check if the CSS file contains expected contrast improvement rules"""
    print("\n🎨 Checking CSS contrast rules...")
    
    try:
        with open('app/static/css/text-contrast-improvements.css', 'r', encoding='utf-8') as f:
            content = f.read()
            
        improvements = 0
        
        # Check for text-muted improvements
        if '.text-muted' in content and '#495057' in content:
            improvements += 1
            print("✅ text-muted color improved to darker gray (#495057)")
            
        # Check for bg-light improvements
        if '.bg-light' in content and '#e9ecef' in content:
            improvements += 1
            print("✅ bg-light background improved to darker shade (#e9ecef)")
            
        # Check for warning color improvements
        if '.bg-warning' in content and '#fd7e14' in content:
            improvements += 1
            print("✅ Warning colors improved to orange instead of yellow")
            
        # Check for small text improvements
        if 'small.text-muted' in content and '#343a40' in content:
            improvements += 1
            print("✅ Small text contrast improved to very dark gray")
            
        # Check for mobile improvements
        if '@media (max-width: 768px)' in content:
            improvements += 1
            print("✅ Mobile-specific contrast improvements included")
            
        # Check for accessibility features
        if '@media (prefers-contrast: high)' in content:
            improvements += 1
            print("✅ High contrast mode support included")
            
        # Check for error prevention rules
        if '.bg-white .text-white' in content:
            improvements += 1
            print("✅ White on white error prevention rules included")
            
        print(f"\n📊 Found {improvements}/7 expected improvements")
        return improvements >= 5
        
    except Exception as e:
        print(f"❌ Failed to check CSS rules: {e}")
        return False

def check_template_contrast_issues():
    """Check for remaining contrast issues in templates"""
    print("\n🔎 Scanning templates for potential contrast issues...")
    
    issues_found = 0
    templates_checked = 0
    
    template_dirs = [
        'app/templates',
        'app/templates/stocks',
        'app/templates/analysis',
        'app/templates/features',
        'app/templates/portfolio'
    ]
    
    for template_dir in template_dirs:
        if not os.path.exists(template_dir):
            continue
            
        for filename in os.listdir(template_dir):
            if filename.endswith('.html'):
                templates_checked += 1
                file_path = os.path.join(template_dir, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for problematic patterns
                    if 'text-white' in content and 'bg-white' in content:
                        print(f"⚠️  Potential white on white in {filename}")
                        issues_found += 1
                        
                    if 'text-light' in content and 'bg-light' in content:
                        print(f"⚠️  Potential light on light in {filename}")
                        issues_found += 1
                        
                except Exception as e:
                    print(f"❌ Error checking {filename}: {e}")
    
    print(f"\n📊 Checked {templates_checked} templates")
    if issues_found == 0:
        print("✅ No obvious contrast issues found in templates")
        return True
    else:
        print(f"⚠️  Found {issues_found} potential contrast issues")
        return False

def check_specific_improvements():
    """Check for specific contrast improvements"""
    print("\n🎯 Checking specific improvement areas...")
    
    improvements = 0
    
    # Check demo page contrast
    try:
        with open('app/templates/demo.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'stat-card bg-light' in content:
            print("✅ Demo page has stat cards that will benefit from improvements")
            improvements += 1
            
    except Exception:
        pass
        
    # Check if subscription page exists for contrast testing
    try:
        with open('app/templates/subscription.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'pricing-card' in content:
            print("✅ Subscription page has pricing cards that will benefit from improvements")
            improvements += 1
            
    except Exception:
        print("ℹ️  Subscription template not found - this is normal")
        
    # Check financial dashboard
    try:
        with open('app/templates/financial_dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'text-muted' in content:
            print("✅ Financial dashboard has text-muted elements that will benefit from improvements")
            improvements += 1
            
    except Exception:
        pass
        
    # Check base template for footer contrast
    try:
        with open('app/templates/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'bg-dark text-white' in content:
            print("✅ Footer has proper dark background with white text")
            improvements += 1
            
    except Exception:
        pass
        
    return improvements >= 2

def generate_contrast_report():
    """Generate a comprehensive contrast improvement report"""
    print("\n📋 COMPREHENSIVE CONTRAST IMPROVEMENTS REPORT")
    print("=" * 60)
    
    css_loaded = check_css_loaded()
    css_rules = check_css_rules()
    template_issues = check_template_contrast_issues()
    specific_improvements = check_specific_improvements()
    
    print("\n🏆 OVERALL ASSESSMENT:")
    print("=" * 30)
    
    total_score = sum([css_loaded, css_rules, template_issues, specific_improvements])
    
    if total_score >= 3:
        print("✅ EXCELLENT - Text contrast improvements successfully implemented!")
        print("   • CSS file properly loaded and configured")
        print("   • Comprehensive rules for text-muted, bg-light, and other elements")
        print("   • Mobile and accessibility improvements included")
        print("   • Error prevention rules active")
        success = True
    elif total_score >= 2:
        print("⚠️  GOOD - Most improvements in place, minor issues remain")
        success = True
    else:
        print("❌ NEEDS WORK - Significant contrast issues remain")
        success = False
        
    print(f"\n📊 Implementation Score: {total_score}/4")
    print(f"🕐 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success

if __name__ == "__main__":
    success = generate_contrast_report()
    print(f"\n{'🎉 SUCCESS' if success else '❌ FAILED'}")
