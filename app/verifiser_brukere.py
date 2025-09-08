#!/usr/bin/env python3
"""
Verifiser at alle exempt brukere har riktige tilganger
"""
import sys
import os
sys.path.insert(0, '/workspaces/aksjeradarv6')

from app import create_app
from app.models.user import User

def verifiser_brukere():
    app = create_app()
    with app.app_context():
        exempt_emails = ['testuser@aksjeradar.trade', 'testuser@aksjeradar.trade', 'helene721@gmail.com']
        
        print("🔍 Verifiserer alle exempt brukere:")
        print("=" * 50)
        
        for email in exempt_emails:
            user = User.query.filter_by(email=email).first()
            if user:
                print(f"✅ {email}")
                print(f"   Username: {user.username}")
                print(f"   Has subscription: {user.has_subscription}")
                print(f"   Subscription type: {user.subscription_type}")
                print(f"   Is admin: {user.is_admin}")
                print(f"   Has password: {'Yes' if user.password_hash else 'No'}")
                print()
            else:
                print(f"❌ {email} - Ikke funnet!")
                print()

if __name__ == '__main__':
    verifiser_brukere()
