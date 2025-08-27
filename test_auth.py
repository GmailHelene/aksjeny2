#!/usr/bin/env python3

# Quick test script to check authentication status
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests

# Test authentication locally
cookies_jar = requests.Session()

# Test admin login
# WARNING: The test-login endpoint should only be enabled in development environments.
# Ensure your backend disables or protects this endpoint in production.
resp = cookies_jar.get('http://localhost:5002/admin/test-login/testuser')
print(f"Admin login response: {resp.status_code} - {resp.text}")

# Check if authenticated by testing a protected route
resp2 = cookies_jar.get('http://localhost:5002/profile')
print(f"Profile access: {resp2.status_code} - URL: {resp2.url}")

# Check home page navigation
resp3 = cookies_jar.get('http://localhost:5002/')
print(f"Home page - Auth detected: {'AUTHENTICATED USER' in resp3.text}")
print(f"Home page - Limited nav: {'LIMITED NAVIGATION' in resp3.text}")
