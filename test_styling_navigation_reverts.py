#!/usr/bin/env python3
"""
Test script to verify styling and navigation reverts are working correctly
"""

def test_navigation_reverts():
    """Test that navigation positioning is reverted to original"""
    print("🔍 Testing Navigation Reverts...")
    
    # Test navigation positioning
    with open('app/templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check that ms-auto is used (right-aligned navigation)
    ms_auto_count = content.count('navbar-nav ms-auto')
    me_auto_count = content.count('navbar-nav me-auto')
    
    print(f"✅ Navigation positioning:")
    print(f"   - ms-auto (right-aligned): {ms_auto_count} instances")
    print(f"   - me-auto (left-aligned): {me_auto_count} instances") 
    
    if ms_auto_count > 0 and me_auto_count == 0:
        print("✅ Navigation is correctly right-aligned (reverted)")
    else:
        print("❌ Navigation positioning may still have issues")
    
    # Check for removal of custom positioning CSS
    problematic_css = [
        'padding-left: 0 !important',
        'margin-left: -4rem !important',
        'margin-left: -2rem !important',
        'right: 0 !important'
    ]
    
    css_issues = []
    for css in problematic_css:
        if css in content:
            css_issues.append(css)
    
    if not css_issues:
        print("✅ Custom positioning CSS successfully removed")
    else:
        print(f"❌ Still has problematic CSS: {css_issues}")

def test_styling_reverts():
    """Test that styling changes are reverted"""
    print("\n🎨 Testing Styling Reverts...")
    
    # Test index.html for color reverts
    with open('app/templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for green background removal
    if '#1b5e20' in content:
        print("❌ Dark green background still present")
    else:
        print("✅ Dark green background removed")
    
    # Check for bg-primary usage
    if 'bg-primary' in content:
        print("✅ Bootstrap bg-primary is being used")
    else:
        print("⚠️  No bg-primary found - check if this is intentional")
    
    # Check for excessive !important styles
    important_count = content.count('!important')
    print(f"✅ Inline !important styles: {important_count} (should be minimal)")
    
    # Test resources page
    try:
        with open('app/templates/resources/index.html', 'r', encoding='utf-8') as f:
            resources_content = f.read()
        
        # Check for custom CSS block removal
        if '<style>' in resources_content and 'Resources page specific styling fixes' in resources_content:
            print("❌ Custom CSS still present in resources page")
        else:
            print("✅ Custom CSS removed from resources page")
            
    except FileNotFoundError:
        print("⚠️  Resources template not found")

def test_builderror_fixes_preserved():
    """Test that BuildError fixes are still in place"""
    print("\n🛠️ Testing BuildError Fixes (Should be Preserved)...")
    
    templates_to_check = [
        'app/templates/base.html',
        'app/templates/portfolio/tips.html',
        'app/templates/admin/index.html',
        'app/templates/portfolio/add_tip.html'
    ]
    
    for template in templates_to_check:
        try:
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for correct endpoint usage
            if 'portfolio.stock_tips' in content:
                print(f"✅ {template}: Uses correct portfolio.stock_tips endpoint")
            elif 'portfolio.tips' in content and 'portfolio.stock_tips' not in content:
                print(f"❌ {template}: Still uses incorrect portfolio.tips endpoint")
            else:
                print(f"ℹ️  {template}: No portfolio tips endpoints found (may be OK)")
                
        except FileNotFoundError:
            print(f"⚠️  {template}: File not found")

def main():
    print("🚀 Testing Styling and Navigation Reverts")
    print("="*50)
    
    test_navigation_reverts()
    test_styling_reverts()
    test_builderror_fixes_preserved()
    
    print("\n" + "="*50)
    print("✅ Revert Testing Complete!")
    print("\nExpected Results:")
    print("- Navigation should be right-aligned (original behavior)")
    print("- No custom CSS overrides causing conflicts")
    print("- Default Bootstrap colors and styling")
    print("- BuildError fixes preserved for functionality")

if __name__ == "__main__":
    main()
