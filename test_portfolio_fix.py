#!/usr/bin/env python3
"""
Test script to verify our portfolio button fixes are working correctly.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from app.models import User, Portfolio, PortfolioStock
from app.extensions import db
from flask import url_for
import json

def test_portfolio_add_route():
    """Test the portfolio add route with JSON data"""
    app = create_app()
    
    with app.app_context():
        with app.test_client() as client:
            # Test the portfolio add route with JSON data
            try:
                response = client.post('/portfolio/add', 
                                     json={
                                         'ticker': 'DNB.OL',
                                         'quantity': 1,
                                         'purchase_price': 185.20
                                     },
                                     content_type='application/json')
                
                print(f"Portfolio add route response status: {response.status_code}")
                print(f"Portfolio add route response data: {response.get_json()}")
                
                if response.status_code == 200:
                    data = response.get_json()
                    if data and data.get('success'):
                        print("✅ Portfolio add route working correctly!")
                        return True
                    else:
                        print(f"❌ Portfolio add route failed: {data.get('error') if data else 'No data returned'}")
                        return False
                else:
                    print(f"❌ Portfolio add route returned error status: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error testing portfolio add route: {e}")
                return False

def test_stock_details_route():
    """Test the stock details route to check volume/market cap display"""
    app = create_app()
    
    with app.app_context():
        with app.test_client() as client:
            try:
                response = client.get('/stocks/details/DNB.OL')
                
                print(f"Stock details route response status: {response.status_code}")
                
                if response.status_code == 200:
                    html_content = response.get_data(as_text=True)
                    
                    # Check if volume and market cap are displayed
                    if 'Volum' in html_content and 'Markedsverdi' in html_content:
                        # Check if they show actual values instead of "-"
                        volume_showing_dash = 'Volum</div>\n                                <div class="fw-bold">\n                                    -' in html_content
                        market_cap_showing_dash = 'Markedsverdi</div>\n                                <div class="fw-bold">\n                                    -' in html_content
                        
                        if not volume_showing_dash and not market_cap_showing_dash:
                            print("✅ Stock details volume and market cap display working correctly!")
                            return True
                        else:
                            print(f"❌ Volume or market cap still showing '-': Volume={volume_showing_dash}, MarketCap={market_cap_showing_dash}")
                            return False
                    else:
                        print("❌ Volume and market cap sections not found in stock details")
                        return False
                else:
                    print(f"❌ Stock details route returned error status: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error testing stock details route: {e}")
                return False

def main():
    """Run all tests"""
    print("🧪 Testing Portfolio Button and Data Display Fixes")
    print("=" * 50)
    
    # Test 1: Portfolio add route
    print("\n1. Testing Portfolio Add Route (JSON support)")
    portfolio_test_passed = test_portfolio_add_route()
    
    # Test 2: Stock details data display
    print("\n2. Testing Stock Details Data Display")
    stock_details_test_passed = test_stock_details_route()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"Portfolio add route: {'✅ PASS' if portfolio_test_passed else '❌ FAIL'}")
    print(f"Stock details data: {'✅ PASS' if stock_details_test_passed else '❌ FAIL'}")
    
    if portfolio_test_passed and stock_details_test_passed:
        print("\n🎉 All tests passed! Portfolio button and data display fixes are working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
