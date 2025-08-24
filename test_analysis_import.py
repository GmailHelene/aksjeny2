#!/usr/bin/env python3
"""Test script to validate analysis.py imports correctly"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.routes.analysis import analysis
    print('SUCCESS: analysis.py imports correctly')
    print(f'Blueprint name: {analysis.name}')
    print(f'URL prefix: {analysis.url_prefix}')
    
    # Check if the sentiment route is registered
    rules = [rule for rule in analysis.url_map.iter_rules()]
    print(f'Number of routes: {len(rules)}')
    for rule in rules:
        print(f'  Route: {rule.rule} -> {rule.endpoint}')
        
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
