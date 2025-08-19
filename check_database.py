#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Portfolio, Watchlist

def check_database_contents():
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking database contents...")
        
        # Check users
        users = User.query.all()
        print(f"Users in database: {len(users)}")
        for user in users:
            print(f"  - {user.username} (ID: {user.id})")
        
        # Check portfolios
        portfolios = Portfolio.query.all()
        print(f"Portfolios in database: {len(portfolios)}")
        for portfolio in portfolios:
            print(f"  - {portfolio.name} (User ID: {portfolio.user_id})")
        
        # Check watchlists
        watchlists = Watchlist.query.all()
        print(f"Watchlists in database: {len(watchlists)}")
        for watchlist in watchlists:
            print(f"  - {watchlist.name} (User ID: {watchlist.user_id})")

if __name__ == "__main__":
    check_database_contents()
