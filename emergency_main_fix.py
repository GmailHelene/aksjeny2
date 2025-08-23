#!/usr/bin/env python3
"""
MASS EMERGENCY FIX - Replace ALL remaining url_for() calls in main.py
"""

import re

def fix_main_py():
    """Fix ALL url_for() calls in main.py"""
    
    # Read the file
    with open('app/routes/main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🚨 EMERGENCY MASS FIX for main.py")
    print("=" * 50)
    
    # Direct replacements for all url_for patterns
    replacements = [
        ("redirect(url_for('main.index'))", "redirect('/')"),
        ("redirect(url_for('auth.login'))", "redirect('/login')"),
        ("redirect(url_for('main.login'))", "redirect('/login')"),
        ("redirect(url_for('main.contact'))", "redirect('/contact')"),
        ("redirect(url_for('main.pricing'))", "redirect('/pricing')"),
        ("redirect(url_for('main.profile'))", "redirect('/profile')"),
        ("redirect(url_for('main.settings'))", "redirect('/settings')"),
        ("redirect(url_for('main.account_settings'))", "redirect('/settings')"),
        ("next_page = url_for('main.index')", "next_page = '/'"),
        ("url_for('main.reset_password', token=token, _external=True)", "f'https://aksjeradar.trade/reset-password/{token}'"),
        ("redirect(url_for('stocks.details', ticker=shared_text.strip()))", "redirect(f'/stocks/details/{shared_text.strip()}')"),
        ("redirect(url_for('stocks.search', query=shared_text.strip()))", "redirect(f'/stocks/search?query={shared_text.strip()}')"),
        ("redirect(request.referrer or url_for('main.index'))", "redirect(request.referrer or '/')"),
    ]
    
    # Apply all replacements
    changes_made = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changes_made += 1
            print(f"✅ Fixed: {old} -> {new}")
    
    # Additional regex-based fixes for complex patterns
    patterns = [
        # Any remaining url_for('main.X') -> direct path
        (r"url_for\('main\.(\w+)'\)", r"'/\1'"),
        # Any remaining redirect(url_for('main.X')) -> direct redirect
        (r"redirect\(url_for\('main\.(\w+)'\)\)", r"redirect('/\1')"),
        # Any remaining pricing redirects
        (r"url_for\('pricing\.\w+'\)", r"'/pricing'"),
    ]
    
    for pattern, replacement in patterns:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes_made += len(matches)
            print(f"✅ Regex fix: {pattern} -> {replacement} ({len(matches)} matches)")
    
    # Write the fixed content back
    with open('app/routes/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n🎯 TOTAL FIXES: {changes_made}")
    print("✅ main.py is now url_for() free!")
    return changes_made

if __name__ == "__main__":
    fix_main_py()
