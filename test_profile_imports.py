#!/usr/bin/env python3

"""Test script for profile route functionality"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.routes.main import main
    print("✅ Successfully imported main blueprint")
    
    # Try to import required models
    try:
        from app.models.user import User
        print("✅ Successfully imported User model")
    except Exception as e:
        print(f"❌ Failed to import User model: {e}")
    
    try:
        from app.models.favorites import Favorites
        print("✅ Successfully imported Favorites model")
    except Exception as e:
        print(f"❌ Failed to import Favorites model: {e}")
    
    try:
        from app.models.referral import Referral
        print("✅ Successfully imported Referral model")
    except Exception as e:
        print(f"❌ Failed to import Referral model: {e}")
    
    try:
        from app.utils.access_control import EXEMPT_EMAILS
        print("✅ Successfully imported EXEMPT_EMAILS")
    except Exception as e:
        print(f"❌ Failed to import EXEMPT_EMAILS: {e}")
    
    try:
        from app.extensions import db
        print("✅ Successfully imported database extension")
    except Exception as e:
        print(f"❌ Failed to import database extension: {e}")
        
    print("\n📋 Module import test completed")
    
except Exception as e:
    print(f"❌ Failed to import main blueprint: {e}")
    import traceback
    print(f"Full traceback: {traceback.format_exc()}")
