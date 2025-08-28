#!/usr/bin/env python3
"""Simple script to add test favorites"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def add_test_favorites():
    try:
        from app import create_app
        from app.models.favorites import Favorites
        from app.models.user import User
        from app.extensions import db
        from config import DevelopmentConfig
        
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            # Get the first user
            user = User.query.first()
            if not user:
                print("No users found in database")
                return False
                
            print(f"Found user: {user.username} (ID: {user.id})")
            
            # Check existing favorites
            existing = Favorites.query.filter_by(user_id=user.id).count()
            print(f"Existing favorites: {existing}")
            
            # Add some test favorites if none exist
            if existing == 0:
                test_stocks = [
                    ('AAPL', 'Apple Inc.', 'NASDAQ'),
                    ('TSLA', 'Tesla Inc.', 'NASDAQ'),
                    ('EQNR.OL', 'Equinor ASA', 'OSE'),
                    ('DNB.OL', 'DNB Bank ASA', 'OSE')
                ]
                
                for symbol, name, exchange in test_stocks:
                    try:
                        favorite = Favorites.add_favorite(
                            user_id=user.id,
                            symbol=symbol,
                            name=name,
                            exchange=exchange
                        )
                        print(f"Added {symbol}: {name}")
                    except Exception as e:
                        print(f"Error adding {symbol}: {e}")
                
                db.session.commit()
                print("Test favorites added!")
            else:
                print("User already has favorites:")
                favs = Favorites.query.filter_by(user_id=user.id).all()
                for fav in favs:
                    print(f"  - {fav.symbol}: {fav.name}")
            
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    add_test_favorites()
