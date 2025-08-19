#!/usr/bin/env python3

import sys
import os
sys.path.append('/workspaces/aksjeny')

from app import create_app
from app.models import User

def test_template_error():
    """Debug what error is appearing in the template"""
    
    app = create_app()
    
    with app.app_context():
        # Find user
        user = User.query.filter_by(username='helene_luxus').first()
        if not user:
            print("❌ User not found!")
            return
            
        print(f"✅ Found user: {user.username}")
        
        # Test with authentication
        with app.test_client() as client:
            # Login
            with client.session_transaction() as sess:
                sess['user_id'] = str(user.id)
                sess['_fresh'] = True
                
            print("🔍 Testing homepage with logged-in user...")
            response = client.get('/')
            
            print(f"Status code: {response.status_code}")
            
            html_content = response.get_data(as_text=True)
            
            # Look for error/exception content
            if 'error' in html_content.lower() or 'exception' in html_content.lower():
                print("\n🚨 Found error/exception in HTML:")
                print("="*80)
                
                # Extract lines around error
                lines = html_content.split('\n')
                for i, line in enumerate(lines):
                    if 'error' in line.lower() or 'exception' in line.lower():
                        # Show context around error
                        start = max(0, i-5)
                        end = min(len(lines), i+5)
                        for j in range(start, end):
                            marker = ">>> " if j == i else "    "
                            print(f"{marker}{j:4d}: {lines[j]}")
                        print("="*80)
            
            # Check for authentication issues
            print("\n🔍 Checking authentication status in template:")
            if 'current_user.is_authenticated' in html_content:
                print("✅ current_user.is_authenticated found in template")
            else:
                print("❌ current_user.is_authenticated not found")
                
            # Check what's in user_stats
            if 'user_stats' in html_content:
                print("✅ user_stats found in template")
                
                # Find the user_stats section
                user_stats_start = html_content.find('user_stats')
                if user_stats_start != -1:
                    # Get context around user_stats
                    context_start = max(0, user_stats_start - 200)
                    context_end = min(len(html_content), user_stats_start + 500)
                    context = html_content[context_start:context_end]
                    print("\n📊 user_stats context:")
                    print("="*60)
                    print(context)
                    print("="*60)
            else:
                print("❌ user_stats not found in template")
                
            # Check JavaScript variables
            if 'user_stats' in html_content and 'JSON.stringify' in html_content:
                print("✅ JavaScript user_stats variable found")
            else:
                print("❌ JavaScript user_stats variable not found")

if __name__ == "__main__":
    test_template_error()
