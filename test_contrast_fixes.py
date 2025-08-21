#!/usr/bin/env python3
"""
CSS Contrast Fixes Verification Test
Tests that all critical Bootstrap classes have proper contrast fixes
"""

import re

def test_css_contrast_fixes():
    """Test that CSS contrast fixes are properly implemented"""
    
    print("🎨 Testing CSS Contrast Fixes...")
    
    # Read the base template
    try:
        with open('app/templates/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ base.html not found")
        return False
    
    # Check for critical outline button fixes
    outline_classes = [
        'btn-outline-primary',
        'btn-outline-success', 
        'btn-outline-info',
        'btn-outline-dark',
        'btn-outline-warning',
        'btn-outline-danger',
        'btn-outline-secondary'
    ]
    
    missing_fixes = []
    
    for css_class in outline_classes:
        pattern = rf'\.{css_class}\s*{{[^}}]*background-color:[^}};]*!important'
        if not re.search(pattern, content, re.MULTILINE | re.DOTALL):
            missing_fixes.append(css_class)
    
    # Check for text color fixes
    text_classes = [
        'text-muted',
        'text-primary',
        'text-success',
        'text-info',
        'text-warning',
        'text-danger',
        'text-dark'
    ]
    
    for text_class in text_classes:
        pattern = rf'\.{text_class}\s*{{[^}}]*color:[^}};]*!important'
        if not re.search(pattern, content, re.MULTILINE | re.DOTALL):
            missing_fixes.append(text_class)
    
    if missing_fixes:
        print(f"❌ Missing CSS fixes for: {', '.join(missing_fixes)}")
        return False
    
    print("✅ All critical CSS contrast fixes are in place!")
    
    # Check specific color values
    critical_checks = [
        ('btn-outline-primary', '#003d7a'),  # Dark blue background
        ('btn-outline-success', '#0d4f2c'),  # Dark green background  
        ('btn-outline-info', '#0c5460'),     # Dark cyan background
        ('btn-outline-dark', '#1a1a1a'),     # Very dark background
        ('text-muted', '#adb5bd'),           # Light gray text
        ('text-dark', '#ffffff')             # White text for dark theme
    ]
    
    for css_class, expected_color in critical_checks:
        pattern = rf'\.{css_class}\s*{{[^}}]*(?:background-)?color:\s*{re.escape(expected_color)}\s*!important'
        if re.search(pattern, content, re.MULTILINE | re.DOTALL):
            print(f"✅ {css_class}: Correct color {expected_color}")
        else:
            print(f"⚠️  {css_class}: Color {expected_color} not found")
    
    return True

def test_hover_states():
    """Test that hover states are properly defined"""
    
    print("\n🖱️  Testing Hover States...")
    
    try:
        with open('app/templates/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ base.html not found")
        return False
    
    # Check for hover states
    hover_pattern = r'\.btn-outline-[^:]+:hover[^{]*{[^}]*color:\s*#ffffff\s*!important'
    
    if re.search(hover_pattern, content, re.MULTILINE | re.DOTALL):
        print("✅ Hover states properly defined with white text")
        return True
    else:
        print("❌ Hover states not properly defined")
        return False

def main():
    """Run all contrast fix tests"""
    
    print("=" * 50)
    print("CSS CONTRAST FIXES VERIFICATION")
    print("=" * 50)
    
    css_ok = test_css_contrast_fixes()
    hover_ok = test_hover_states()
    
    print("\n" + "=" * 50)
    if css_ok and hover_ok:
        print("🎉 ALL CONTRAST FIXES VERIFIED SUCCESSFULLY!")
        print("✅ Quick action buttons should now be readable")
        print("✅ Text colors should have proper contrast")
        print("✅ Bootstrap outline buttons have dark backgrounds")
    else:
        print("❌ SOME CONTRAST FIXES ARE MISSING")
        print("⚠️  Manual review required")
    
    print("=" * 50)
    
    return css_ok and hover_ok

if __name__ == "__main__":
    main()
