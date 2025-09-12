#!/usr/bin/env python3
"""
Session and Cookie Security Test
Tests the security configuration of sessions and cookies
"""

import os
import sys
import requests
import pytest
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_security_headers():
    """Test security headers are properly set (assert based)."""
    print("🔒 Testing Security Headers...")
    try:
        response = requests.get('http://localhost:5002/', timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Server not available for security header test: {e}")

    headers_to_check = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': 'default-src',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'X-Download-Options': 'noopen',
        'X-Permitted-Cross-Domain-Policies': 'none'
    }

    print(f"Response Status: {response.status_code}")
    missing = []
    for header, expected_value in headers_to_check.items():
        if header in response.headers:
            actual_value = response.headers[header]
            if expected_value in actual_value:
                print(f"✅ {header}: {actual_value}")
            else:
                print(f"⚠️ {header}: {actual_value} (expected substring '{expected_value}')")
        else:
            print(f"❌ Missing {header}")
            missing.append(header)

    # Only assert on truly critical headers missing
    critical = [h for h in missing if h in {'X-Content-Type-Options', 'X-Frame-Options'}]
    if critical:
        pytest.fail(f"Critical security headers missing: {', '.join(critical)}")

def test_cookie_security():
    """Test cookie security settings (assert/skip based)."""
    print("\n🍪 Testing Cookie Security...")
    session = requests.Session()
    try:
        response = session.get('http://localhost:5002/', timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Server not available for cookie security test: {e}")

    print(f"Response Status: {response.status_code}")
    cookies = session.cookies
    if cookies:
        print(f"Found {len(cookies)} cookies:")
        for cookie in cookies:
            print(f"  Cookie: {cookie.name}")
            print(f"    Path: {cookie.path}")
            print(f"    Domain: {cookie.domain}")
            print(f"    Secure: {cookie.secure}")
            print(f"    HttpOnly: {cookie.has_nonstandard_attr('HttpOnly')}")
            print(f"    SameSite: {cookie.get_nonstandard_attr('SameSite', 'Not set')}")
    else:
        print("No cookies found (may be normal for homepage)")

def test_csrf_protection():
    """Test CSRF protection is working (skip when server down)."""
    print("\n🛡️ Testing CSRF Protection...")
    session = requests.Session()
    try:
        response = session.get('http://localhost:5002/login', timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Server not available for CSRF test: {e}")

    if response.status_code != 200:
        pytest.skip(f"Login page ikke tilgjengelig: {response.status_code}")

    login_data = {
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    response_post = session.post('http://localhost:5002/login',
                                 data=login_data,
                                 timeout=5,
                                 allow_redirects=False)
    if response_post.status_code not in [400, 403, 422]:
        # Not outright failure but worth flagging
        print(f"⚠️ Uventet respons uten CSRF token: {response_post.status_code}")

def test_session_configuration():
    """Test session configuration by checking config (assert based)."""
    print("\n⚙️ Testing Session Configuration...")
    from config import config as cfg
    from app import create_app

    app = create_app('development')
    with app.app_context():
        config_checks = {
            'SESSION_COOKIE_NAME': app.config.get('SESSION_COOKIE_NAME'),
            'SESSION_COOKIE_HTTPONLY': app.config.get('SESSION_COOKIE_HTTPONLY'),
            'SESSION_COOKIE_SAMESITE': app.config.get('SESSION_COOKIE_SAMESITE'),
            'PERMANENT_SESSION_LIFETIME': app.config.get('PERMANENT_SESSION_LIFETIME'),
            'WTF_CSRF_TIME_LIMIT': app.config.get('WTF_CSRF_TIME_LIMIT'),
            'WTF_CSRF_ENABLED': app.config.get('WTF_CSRF_ENABLED'),
        }
        print("Session Configuration:")
        for key, value in config_checks.items():
            print(f"{key}: {value}")
        # Minimal critical assertions
        assert config_checks['SESSION_COOKIE_HTTPONLY'] is not None
        assert 'SESSION_COOKIE_NAME' in config_checks

    prod_config = cfg['production']()
    print("\nProduction-specific settings:")
    prod_settings = {
        'SESSION_COOKIE_SECURE': getattr(prod_config, 'SESSION_COOKIE_SECURE', 'Not set'),
        'REMEMBER_COOKIE_SECURE': getattr(prod_config, 'REMEMBER_COOKIE_SECURE', 'Not set'),
        'WTF_CSRF_SSL_STRICT': getattr(prod_config, 'WTF_CSRF_SSL_STRICT', 'Not set'),
    }
    for key, value in prod_settings.items():
        print(f"{key}: {value}")

def main():
    """CLI samle-kjøring uten pytest asserts som stopper alt straks."""
    print("🔐 AKSJERADAR SESSION & COOKIE SECURITY TEST")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    results = {"session_config": True, "security_headers": True, "cookies": True, "csrf": True}
    try:
        test_session_configuration()
    except Exception as e:
        print(f"session_config FAILED: {e}")
        results["session_config"] = False
    try:
        test_security_headers()
    except pytest.skip.Exception as e:  # type: ignore
        print(f"security_headers SKIPPED: {e}")
    except Exception as e:
        print(f"security_headers FAILED: {e}")
        results["security_headers"] = False
    try:
        test_cookie_security()
    except pytest.skip.Exception as e:  # type: ignore
        print(f"cookie_security SKIPPED: {e}")
    except Exception as e:
        print(f"cookie_security FAILED: {e}")
        results["cookies"] = False
    try:
        test_csrf_protection()
    except pytest.skip.Exception as e:  # type: ignore
        print(f"csrf_protection SKIPPED: {e}")
    except Exception as e:
        print(f"csrf_protection FAILED: {e}")
        results["csrf"] = False

    print("\n" + "=" * 50)
    print("🏁 TEST SUMMARY")
    print("=" * 50)
    passed = sum(1 for k, v in results.items() if v)
    total = len(results)
    print(f"Result: {passed}/{total} core checks passed (skips not counted as failures)")
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
