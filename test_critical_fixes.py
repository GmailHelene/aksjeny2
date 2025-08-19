#!/usr/bin/env python3
"""
Test the critical production fixes we just implemented:
1. DataService.get_comparative_data method availability
2. Market overview template rendering
3. Fundamental select template existence
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.data_service import DataService
from flask import Flask
from jinja2 import Template

def test_data_service_method():
    """Test that get_comparative_data method exists and is callable"""
    print("🔍 Testing DataService.get_comparative_data method...")
    
    # Check if method exists
    if hasattr(DataService, 'get_comparative_data'):
        print("✅ Method exists on DataService class")
        
        # Test method call
        try:
            symbols = ['EQNR.OL', 'AAPL']
            result = DataService.get_comparative_data(symbols, period='1mo', interval='1d')
            print(f"✅ Method callable - returned data for {len(result)} symbols")
            return True
        except Exception as e:
            print(f"❌ Method call failed: {e}")
            return False
    else:
        print("❌ Method get_comparative_data not found on DataService")
        return False

def test_template_exists():
    """Test that fundamental_select.html template was created"""
    print("\n🔍 Testing fundamental_select.html template...")
    
    template_path = '/workspaces/aksjeny/app/templates/analysis/fundamental_select.html'
    if os.path.exists(template_path):
        print("✅ Template file exists")
        
        # Test template content
        with open(template_path, 'r') as f:
            content = f.read()
            if 'fundamental analyse' in content and 'url_for' in content:
                print("✅ Template has expected content")
                return True
            else:
                print("❌ Template missing expected content")
                return False
    else:
        print("❌ Template file does not exist")
        return False

def test_market_overview_dict_access():
    """Test that market overview template uses correct dict access patterns"""
    print("\n🔍 Testing market overview template dict access...")
    
    template_path = '/workspaces/aksjeny/app/templates/analysis/market_overview.html'
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            content = f.read()
            
        # Check for problematic patterns
        problematic_patterns = ['data.change|', 'data.name|', 'data.price|', 'data.last_price|']
        remaining_issues = []
        
        for pattern in problematic_patterns:
            if pattern in content:
                remaining_issues.append(pattern)
        
        if not remaining_issues:
            print("✅ No problematic dict access patterns found")
            
            # Check for correct patterns
            correct_patterns = ["data.get('change'", "data.get('name'", "data.get('price'"]
            found_correct = [p for p in correct_patterns if p in content]
            
            if found_correct:
                print(f"✅ Found correct dict access patterns: {len(found_correct)}")
                return True
            else:
                print("❌ No correct dict access patterns found")
                return False
        else:
            print(f"❌ Found problematic patterns: {remaining_issues}")
            return False
    else:
        print("❌ Market overview template not found")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing critical production fixes...\n")
    
    results = []
    results.append(test_data_service_method())
    results.append(test_template_exists())
    results.append(test_market_overview_dict_access())
    
    print("\n" + "="*50)
    print(f"📊 Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 All critical fixes are working correctly!")
        return 0
    else:
        print("⚠️  Some issues remain - check output above")
        return 1

if __name__ == '__main__':
    sys.exit(main())
