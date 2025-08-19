#!/usr/bin/env python3

import sys
import os
sys.path.append('/workspaces/aksjeny')

from app import create_app
from app.models import User
from flask_login import current_user

def test_route_directly():
    """Test the route logic directly"""
    
    app = create_app()
    
    with app.app_context():
        # Find user
        user = User.query.filter_by(username='helene_luxus').first()
        if not user:
            print("❌ User not found!")
            return
            
        print(f"✅ Found user: {user.username}")
        
        with app.test_client() as client:
            # Set up session
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
                
            # Now make request and check context
            with client.application.test_request_context():
                # Simulate the request environment
                with client.application.test_request_context('/'):
                    # Check if current_user is available
                    print(f"🔍 current_user object: {current_user}")
                    print(f"🔍 current_user.is_authenticated: {current_user.is_authenticated}")
                    print(f"🔍 current_user type: {type(current_user)}")
                    
                    if hasattr(current_user, 'id'):
                        print(f"🔍 current_user.id: {current_user.id}")
                    
            # Test actual route response
            response = client.get('/')
            print(f"📊 Response status: {response.status_code}")
            
            # Check what variables are in the response context
            if hasattr(response, 'context') and response.context:
                context_vars = list(response.context.keys())
                print(f"📋 Template context variables: {context_vars}")
                
                if 'user_stats' in response.context:
                    print(f"✅ user_stats found: {response.context['user_stats']}")
                else:
                    print("❌ user_stats not in template context")
            else:
                print("❌ No response context available")

if __name__ == "__main__":
    test_route_directly()
