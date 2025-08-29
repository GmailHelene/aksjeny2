#!/usr/bin/env python3
"""
Test script to check Flask route registration
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def check_routes():
    print("🔍 Checking Flask route registration...")
    
    app = create_app('development')
    
    with app.app_context():
        print("\n📋 All registered routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.rule} -> {rule.endpoint} (methods: {rule.methods})")
            
        print("\n🎯 Profile-related routes:")
        profile_routes = [rule for rule in app.url_map.iter_rules() if 'profile' in rule.rule.lower()]
        for rule in profile_routes:
            print(f"  {rule.rule} -> {rule.endpoint} (methods: {rule.methods})")
            
        print("\n🎭 Demo-related routes:")
        demo_routes = [rule for rule in app.url_map.iter_rules() if 'demo' in rule.rule.lower()]
        for rule in demo_routes:
            print(f"  {rule.rule} -> {rule.endpoint} (methods: {rule.methods})")
            
        # Check specific route
        from flask import url_for
        try:
            profile_url = url_for('main.profile')
            print(f"\n✅ Profile URL resolves to: {profile_url}")
        except Exception as e:
            print(f"\n❌ Profile URL resolution error: {e}")

if __name__ == '__main__':
    check_routes()
