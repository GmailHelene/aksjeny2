#!/usr/bin/env python3
"""
Basic test av kritiske importer og app opprettelse
"""
import sys
import os
import traceback
import pytest

# Add the project root to Python path
sys.path.insert(0, '/workspaces/aksjeradarv6')

def test_basic_imports():
    """Test grunnleggende importer (assert basert for pytest)."""
    print("🔍 TESTER GRUNNLEGGENDE IMPORTER...")
    print("=" * 50)

    mandatory = [
        ("Flask", lambda: __import__('flask')),
        ("Requests", lambda: __import__('requests')),
        ("SQLAlchemy", lambda: __import__('sqlalchemy')),
        ("App Extensions", lambda: __import__('app.extensions', fromlist=['db', 'login_manager'])),
        ("App Create", lambda: __import__('app', fromlist=['create_app'])),
        ("User Model", lambda: __import__('app.models.user', fromlist=['User'])),
        ("Main Routes", lambda: __import__('app.routes.main', fromlist=['main'])),
    ]
    optional = [
        ("Pandas", lambda: __import__('pandas')),
        ("YFinance", lambda: __import__('yfinance')),
    ]

    mandatory_failures = []
    optional_missing = []

    for name, import_func in mandatory + optional:
        try:
            import_func()
            print(f"✅ {name}: OK")
        except Exception as e:
            if (name, import_func) in mandatory:
                print(f"❌ {name}: {e} (MANDATORY)")
                mandatory_failures.append(name)
            else:
                print(f"⚠️ {name}: {e} (optional – skipping)")
                optional_missing.append(name)

    if mandatory_failures:
        pytest.fail(f"Mandatory import failures: {', '.join(mandatory_failures)}")

    if optional_missing:
        print(f"\nℹ️ Optional libraries missing: {', '.join(optional_missing)} (not failing test)")

    total_ok = len(mandatory) - len(mandatory_failures)
    print(f"\n📊 Import Test: {total_ok}/{len(mandatory)} mandatory bestått")

def test_app_creation():
    """Test app opprettelse (assert basert)."""
    print("\n🔍 TESTER APP OPPRETTELSE...")
    print("=" * 50)

    from app import create_app
    app = create_app()
    print("✅ App opprettet uten feil")
    print(f"✅ App navn: {app.name}")
    print(f"✅ Debug mode: {app.debug}")
    # Basic sanity assertions
    assert app is not None
    assert hasattr(app, 'config')

def test_database_connection():
    """Test database tilkobling (assert/skip basert)."""
    print("\n🔍 TESTER DATABASE TILKOBLING...")
    print("=" * 50)

    try:
        from app import create_app
        from app.models.user import User
    except Exception as e:  # Import errors should fail fast
        pytest.fail(f"Kritisk import-feil for database test: {e}")

    app = create_app()
    from app.extensions import db  # ensure extensions bound after app creation
    try:
        with app.app_context():
            user_count = User.query.count()
            print(f"✅ Database tilkoblet, {user_count} brukere funnet")
            assert user_count >= 0  # existence check
    except Exception as e:
        pytest.fail(f"Database test feilet: {e}")

def create_missing_files():
    """Opprett manglende filer"""
    print("\n🔧 OPPRETTER MANGLENDE FILER...")
    print("=" * 50)
    
    files_created = []
    
    # 1. Offline.html
    offline_path = "/workspaces/aksjeradarv6/offline.html"
    if not os.path.exists(offline_path):
        try:
            offline_content = '''<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline - Aksjeradar</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f8f9fa; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; margin-bottom: 20px; }
        p { color: #7f8c8d; font-size: 18px; line-height: 1.6; }
        .retry-btn { background: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; margin-top: 20px; }
        .retry-btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📶 Du er offline</h1>
        <p>Beklager, men du er for øyeblikket ikke tilkoblet internett.</p>
        <p>Aksjeradar krever en internettforbindelse for å hente de nyeste markedsdata.</p>
        <button class="retry-btn" onclick="window.location.reload()">🔄 Prøv igjen</button>
    </div>
</body>
</html>'''
            with open(offline_path, 'w', encoding='utf-8') as f:
                f.write(offline_content)
            print("✅ offline.html opprettet")
            files_created.append("offline.html")
        except Exception as e:
            print(f"❌ Kunne ikke opprette offline.html: {e}")
    
    # 2. Service Worker
    sw_path = "/workspaces/aksjeradarv6/static/js/service-worker.js"
    os.makedirs(os.path.dirname(sw_path), exist_ok=True)
    if not os.path.exists(sw_path):
        try:
            sw_content = '''// Aksjeradar Service Worker
const CACHE_NAME = 'aksjeradar-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js',
  '/offline.html'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request).catch(function() {
          return caches.match('/offline.html');
        });
      }
    )
  );
});'''
            with open(sw_path, 'w', encoding='utf-8') as f:
                f.write(sw_content)
            print("✅ service-worker.js opprettet")
            files_created.append("service-worker.js")
        except Exception as e:
            print(f"❌ Kunne ikke opprette service-worker.js: {e}")
    
    return files_created

def main():
    """Hovedfunksjon"""
    print("🧪 AKSJERADAR V6 - BASIC FEILSJEKK")
    print("=" * 60)
    
    # Test 1: Importer
    # Merk: I pytest-modus vil assert failures stoppe kjøring; for CLI samler vi resultater
    imports_ok = True
    app_ok = True
    db_ok = True
    try:
        test_basic_imports()
    except Exception:
        imports_ok = False

    try:
        test_app_creation()
    except Exception:
        app_ok = False

    try:
        test_database_connection()
    except Exception:
        db_ok = False
    
    # Test 4: Opprett manglende filer
    files_created = create_missing_files()
    
    # Rapport
    print("\n" + "=" * 60)
    print("📊 SLUTTRAPPORT")
    print("=" * 60)
    
    if imports_ok and app_ok:
        print("🎉 ALLE GRUNNLEGGENDE TESTER BESTÅTT!")
        print("✅ Importer: OK")
        print("✅ App opprettelse: OK")
        if db_ok:
            print("✅ Database: OK")
        else:
            print("⚠️ Database: Problemer (men ikke kritisk)")
        
        if files_created:
            print(f"🔧 {len(files_created)} filer opprettet: {', '.join(files_created)}")
        
        print("\n📝 NESTE STEG:")
        print("1. Start appen: python run.py")
        print("2. Test i nettleser: http://localhost:5002")
        print("3. Kjør full test: python test_alle_rettelser.py")
        
    else:
        print("❌ KRITISKE FEIL FUNNET:")
        if not imports_ok:
            print("   • Import problemer")
        if not app_ok:
            print("   • App opprettelse problemer")
        
        print("\n📝 FIKS FØRST:")
        print("1. Sjekk Python pakker: pip install -r requirements.txt")
        print("2. Sjekk fil struktur")
        print("3. Kjør denne testen igjen")
    
    print("=" * 60)
    
    return imports_ok and app_ok

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
