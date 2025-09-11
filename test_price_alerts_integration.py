#!/usr/bin/env python3
"""Integration test for price alerts creation and listing endpoints.
Verifies form POST /price-alerts/create and dashboard listing.
"""
import sys
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

BASE = 'http://localhost:5002'


def wait_for_server(path='/health', attempts=25, delay=1.5):
    url = BASE + path
    for i in range(attempts):
        try:
            r = requests.get(url, timeout=3)
            if r.status_code in (200, 302, 404):
                return True
        except Exception:
            pass
        time.sleep(delay)
    return False


def extract_csrf(html: str):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        token_input = soup.find('input', {'name': 'csrf_token'})
        if token_input:
            return token_input.get('value')
    except Exception:
        return None
    return None


def create_alert_session():
    s = requests.Session()
    # Load create page to fetch CSRF
    r = s.get(BASE + '/price-alerts/create', timeout=10)
    if r.status_code != 200:
        return False, f'Create page status {r.status_code}'
    csrf = extract_csrf(r.text)
    data = {
        'symbol': 'TEST.OL',
        'target_price': '123.45',
        'alert_type': 'above',
        'company_name': 'TestCo',
        'notes': 'Integration test'
    }
    if csrf:
        data['csrf_token'] = csrf
    pr = s.post(BASE + '/price-alerts/create', data=data, timeout=10, allow_redirects=False)
    if pr.status_code not in (302, 200):
        return False, f'POST create returned {pr.status_code}'
    # Follow redirect if any
    if pr.status_code == 302 and 'Location' in pr.headers:
        dash = s.get(BASE + pr.headers['Location'], timeout=10)
    else:
        dash = pr
    if dash.status_code != 200:
        return False, f'Dashboard load failed {dash.status_code}'
    if 'Prisvarsel' not in dash.text and 'Price' not in dash.text:
        return False, 'Dashboard missing expected text'
    # Simple heuristic: look for our symbol
    if 'TEST.OL' not in dash.text:
        return False, 'Alert symbol not present in dashboard (may be filtering)'
    return True, 'Alert created and visible'


def main():
    if not wait_for_server():
        print('Server not responding for integration test')
        return 1
    ok, msg = create_alert_session()
    status = '✅' if ok else '❌'
    print(f'{status} Price alerts integration: {msg}')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
