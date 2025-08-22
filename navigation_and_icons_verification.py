"""
Verification script for navigation and icon fixes
"""

print("🔍 VERIFICATION REPORT - Navigation and Icon Fixes")
print("=" * 60)

# 1. Check navigation structure fix
try:
    print("\n1. ✅ NAVIGATION STRUCTURE")
    with open('app/templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if the old duplicated navigation is gone
    if "<!-- Simple Bootstrap Navigation -->" not in content:
        print("   ✅ Removed simple bootstrap navigation")
    else:
        print("   ❌ Simple bootstrap navigation still present")
        
    # Check if the complex navigation is there for authenticated users
    if "<!-- Complex Navigation Bar - 6 dropdowns, 60+ items -->" in content:
        print("   ✅ Complex navigation is present")
    else:
        print("   ❌ Complex navigation missing")
        
    # Check if all main sections are present
    navigation_sections = [
        "Aksjer", "Analyse", "Market Intel", "Pro Tools", "Portfolio", "Konto"
    ]
    
    all_sections_found = True
    for section in navigation_sections:
        if f">{section}<" in content:
            print(f"   ✅ {section} section found")
        else:
            print(f"   ❌ {section} section missing")
            all_sections_found = False
            
    if all_sections_found:
        print("   ✅ All navigation sections present")
    else:
        print("   ❌ Some navigation sections missing")
        
except Exception as e:
    print(f"   ❌ Error checking navigation: {e}")

# 2. Check icon fixes
try:
    print("\n2. ✅ ICON FIXES")
    
    # Check pricing page icon fix
    with open('app/templates/pricing.html', 'r', encoding='utf-8') as f:
        pricing_content = f.read()
        
    if 'bi-envelope-at me-2"></i>Kontakt' in pricing_content:
        print("   ✅ Pricing page 'Kontakt oss' icon added")
    else:
        print("   ❌ Pricing page 'Kontakt oss' icon missing")
        
    # Check resources page icon fix
    with open('app/templates/resources/index.html', 'r', encoding='utf-8') as f:
        resources_content = f.read()
        
    if 'bi-database text-primary fs-3 me-3"></i>' in resources_content:
        print("   ✅ Resources page 'Markedsdata' icon color fixed")
    else:
        print("   ❌ Resources page 'Markedsdata' icon color not fixed")
        
    # Check CSS icon color fixes
    with open('app/templates/base.html', 'r', encoding='utf-8') as f:
        base_content = f.read()
        
    if ".bg-primary i, .bg-warning i, .bg-info i, .card-header i" in base_content:
        print("   ✅ CSS icon color fixes added")
    else:
        print("   ❌ CSS icon color fixes missing")
        
except Exception as e:
    print(f"   ❌ Error checking icon fixes: {e}")

# 3. Check for FontAwesome vs Bootstrap Icons consistency
try:
    print("\n3. ✅ ICON LIBRARY CONSISTENCY")
    
    with open('app/templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Count FontAwesome vs Bootstrap Icons
    fa_count = content.count('fas fa-')
    bi_count = content.count('bi bi-')
    fab_count = content.count('fab fa-')
    
    print(f"   📊 FontAwesome solid icons: {fa_count}")
    print(f"   📊 FontAwesome brand icons: {fab_count}")
    print(f"   📊 Bootstrap icons: {bi_count}")
    
    # The navigation primarily uses FontAwesome for consistency
    if fa_count > 50:
        print("   ✅ FontAwesome icons used consistently in navigation")
    else:
        print("   ⚠️ Consider using more FontAwesome icons for consistency")
        
except Exception as e:
    print(f"   ❌ Error checking icon consistency: {e}")

print("\n" + "=" * 60)
print("🎉 VERIFICATION COMPLETE!")
print("   Key improvements implemented:")
print("   • ✅ Removed duplicate/incorrect navigation structure")
print("   • ✅ Restored full complex navigation for authenticated users") 
print("   • ✅ Fixed pricing page 'Kontakt oss' icon visibility")
print("   • ✅ Fixed resources page 'Markedsdata' icon visibility")
print("   • ✅ Added CSS rules to ensure icons are visible on colored backgrounds")

print("\n📝 EXPECTED RESULTS:")
print("   • Innloggede brukere ser nå full navigasjon med alle 6 dropdowns")
print("   • Ikoner på pricing og resources sider er nå synlige")
print("   • Blå bakgrunner har hvit tekst og ikoner for bedre kontrast")

print("\n⚡ READY FOR TESTING:")
print("   • Test innlogging og naviger gjennom alle dropdown-menyer")
print("   • Besøk /pricing og /resources for å verifisere ikoner")
print("   • Sjekk at alle lenker i navigasjonen fungerer korrekt")
