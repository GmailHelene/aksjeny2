#!/usr/bin/env python3
"""Test script to verify pricing endpoint is working"""

from app import create_app
from flask import url_for

def test_pricing_endpoint():
    app = create_app()
    
    with app.test_request_context():
        try:
            pricing_url = url_for('pricing.pricing_page')
            print(f"✅ SUCCESS: pricing.pricing_page endpoint works: {pricing_url}")
            return True
        except Exception as e:
            print(f"❌ ERROR: pricing.pricing_page endpoint failed: {e}")
            return False

if __name__ == "__main__":
    test_pricing_endpoint()
