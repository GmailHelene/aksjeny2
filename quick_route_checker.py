#!/usr/bin/env python3
"""
Quick route checker to validate route definitions and templates
"""

import os
import sys
from pathlib import Path

def check_route_templates():
    """Check if templates exist for problematic routes"""
    
    base_dir = Path(__file__).parent
    template_dir = base_dir / 'app' / 'templates'
    
    routes_to_check = [
        ('/profile', 'profile.html'),
        ('/compare', 'stocks/compare.html'),
        ('/forum', 'forum/index.html'),
        ('/analysis/ai', 'analysis/ai.html'),
        ('/norwegian-intel/', 'norwegian_intel/index.html'),
        ('/portfolio', 'portfolio/index.html'),
    ]
    
    print("🔍 Checking route templates...")
    print("=" * 50)
    
    all_good = True
    
    for route, template_path in routes_to_check:
        full_template_path = template_dir / template_path
        status = "✅" if full_template_path.exists() else "❌"
        print(f"{status} {route:<25} → {template_path}")
        
        if not full_template_path.exists():
            all_good = False
            print(f"   Missing: {full_template_path}")
    
    print("\n🔍 Checking route files...")
    print("=" * 50)
    
    route_files = [
        'app/routes/main.py',
        'app/routes/stocks.py', 
        'app/routes/forum.py',
        'app/routes/analysis.py',
        'app/routes/norwegian_intel.py',
        'app/routes/portfolio.py'
    ]
    
    for route_file in route_files:
        full_path = base_dir / route_file
        status = "✅" if full_path.exists() else "❌"
        print(f"{status} {route_file}")
        
        if not full_path.exists():
            all_good = False
    
    print(f"\n{'🎉 All routes look good!' if all_good else '⚠️  Some routes need attention'}")
    return all_good

def check_blueprint_registration():
    """Check if blueprints are properly registered"""
    
    base_dir = Path(__file__).parent
    init_file = base_dir / 'app' / '__init__.py'
    
    print("\n🔍 Checking blueprint registration...")
    print("=" * 50)
    
    if not init_file.exists():
        print("❌ app/__init__.py not found")
        return False
    
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blueprints_to_check = [
        'main',
        'stocks', 
        'forum',
        'analysis',
        'norwegian_intel',
        'portfolio'
    ]
    
    for blueprint in blueprints_to_check:
        if f"'{blueprint}'" in content or f'"{blueprint}"' in content:
            print(f"✅ {blueprint} blueprint registered")
        else:
            print(f"❌ {blueprint} blueprint NOT registered")
    
    return True

if __name__ == "__main__":
    print("🚀 Quick Route Checker")
    print("=" * 50)
    
    templates_ok = check_route_templates()
    blueprints_ok = check_blueprint_registration()
    
    if templates_ok and blueprints_ok:
        print("\n🎉 Route validation completed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Some issues found. Check output above.")
        sys.exit(1)
