#!/usr/bin/env python3
"""Test script to verify pricing blueprint can be imported and has correct endpoints"""

try:
    from app.routes.pricing import pricing
    print('✅ SUCCESS: Pricing blueprint imports correctly')
    print(f'Blueprint name: {pricing.name}')
    
    # Check if the blueprint has the pricing_page endpoint
    endpoints = []
    for rule in pricing.url_map.iter_rules():
        if rule.endpoint:
            endpoints.append(rule.endpoint)
    
    print(f'Available endpoints: {endpoints}')
    
    if 'pricing_page' in endpoints:
        print('✅ SUCCESS: pricing_page endpoint found in blueprint')
    else:
        print('❌ ERROR: pricing_page endpoint NOT found in blueprint')
        
    # Test if the blueprint can generate the URL
    from flask import Flask
    test_app = Flask(__name__)
    test_app.register_blueprint(pricing, url_prefix='/pricing')
    
    with test_app.test_request_context():
        from flask import url_for
        url = url_for('pricing.pricing_page')
        print(f'✅ SUCCESS: Generated URL for pricing.pricing_page: {url}')
        
except Exception as e:
    print(f'❌ ERROR: {e}')
    import traceback
    traceback.print_exc()
