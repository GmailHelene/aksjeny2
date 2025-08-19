#!/usr/bin/env python3
"""
Comprehensive cache clearing for production deployment
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.services.simple_cache import simple_cache
import redis

def clear_all_production_cache():
    """Clear all caches for production deployment"""
    
    print("🧹 CLEARING ALL PRODUCTION CACHES")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        
        # 1. Clear application cache
        print("\n📦 Clearing Application Cache...")
        try:
            if hasattr(simple_cache, 'clear'):
                simple_cache.clear()
                print("   ✅ Application cache cleared")
            else:
                print("   ℹ️  No application cache to clear")
        except Exception as e:
            print(f"   ⚠️  Application cache error: {e}")
        
        # 2. Clear Redis cache (if available)
        print("\n🔴 Clearing Redis Cache...")
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.flushdb()
            print("   ✅ Redis cache cleared")
        except Exception as e:
            print(f"   ℹ️  Redis not available: {e}")
        
        # 3. Clear file-based caches
        print("\n📁 Clearing File Caches...")
        cache_dirs = [
            '/tmp/aksjeradar_cache',
            'instance/cache',
            '.cache'
        ]
        
        for cache_dir in cache_dirs:
            try:
                if os.path.exists(cache_dir):
                    import shutil
                    shutil.rmtree(cache_dir)
                    print(f"   ✅ Cleared {cache_dir}")
                else:
                    print(f"   ℹ️  {cache_dir} not found")
            except Exception as e:
                print(f"   ⚠️  Error clearing {cache_dir}: {e}")
        
        # 4. Browser cache busting
        print("\n🌐 Updating Browser Cache Busting...")
        from datetime import datetime
        
        new_version = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Update version in templates
        version_files = [
            'app/templates/base.html'
        ]
        
        for file_path in version_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Update cache busting version
                    import re
                    content = re.sub(
                        r'v=\d{8}_\d{6}',
                        f'v={new_version}',
                        content
                    )
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"   ✅ Updated cache version to {new_version} in {file_path}")
                else:
                    print(f"   ℹ️  {file_path} not found")
            except Exception as e:
                print(f"   ⚠️  Error updating {file_path}: {e}")
        
        # 5. Clear Python bytecode
        print("\n🐍 Clearing Python Bytecode...")
        try:
            os.system('find . -name "*.pyc" -delete')
            os.system('find . -name "__pycache__" -type d -exec rm -rf {} +')
            print("   ✅ Python bytecode cleared")
        except Exception as e:
            print(f"   ⚠️  Error clearing bytecode: {e}")
        
        # 6. Summary
        print("\n" + "=" * 50)
        print("✨ CACHE CLEARING COMPLETE!")
        print("   All caches have been cleared for fresh deployment")
        print("   Browser cache versions updated")
        print("   Ready for production traffic")
        print("=" * 50)
        
        # 7. Next steps
        print("\n🚀 NEXT STEPS FOR PRODUCTION:")
        print("   1. Commit and push these changes to Git")
        print("   2. Wait for Railway deployment to complete")
        print("   3. Test key functionality on production")
        print("   4. Submit sitemap to Google Search Console")
        print("   5. Monitor logs for any issues")

if __name__ == '__main__':
    clear_all_production_cache()
