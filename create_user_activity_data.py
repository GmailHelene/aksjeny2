#!/usr/bin/env python3
"""
Script to create realistic user activity data for dashboard
"""
from app import create_app
from app.models.user import User
from app.models.portfolio import Portfolio, PortfolioStock
from app.models.watchlist import Watchlist, WatchlistItem
from app.extensions import db
from datetime import datetime, timedelta
import random

def create_user_activity_data():
    app = create_app()
    
    with app.app_context():
        try:
            # Check existing users
            existing_users = User.query.all()
            print(f"Found {len(existing_users)} existing users")
            
            # Create some test users if none exist
            if len(existing_users) == 0:
                print("Creating test users...")
                # Create test users
                users_data = [
                    {
                        'username': 'helene_luxus', 
                        'email': 'helene.luxus@example.com', 
                        'password': 'password123'
                    },
                    {
                        'username': 'eirik_berntsen', 
                        'email': 'eirik.berntsen@example.com', 
                        'password': 'password123'
                    },
                    {
                        'username': 'tonjekit91', 
                        'email': 'tonje.kit@example.com', 
                        'password': 'password123'
                    },
                    {
                        'username': 'helene721', 
                        'email': 'helene.marie@example.com', 
                        'password': 'password123'
                    }
                ]
                
                # Create users if they don't exist
                created_users = []
                for user_data in users_data:
                    existing_user = User.query.filter_by(username=user_data['username']).first()
                    if existing_user:
                        created_users.append(existing_user)
                        print(f"User {user_data['username']} already exists")
                    else:
                        # Create user with correct field names
                        user = User(
                            username=user_data['username'],
                            email=user_data['email']
                        )
                        # Set password using the method
                        user.set_password(user_data['password'])
                        db.session.add(user)
                        created_users.append(user)
                        print(f"Created user: {user_data['username']}")
                
                db.session.commit()
                print(f"✅ Created/found {len(created_users)} users")
                
                # Use created users for activity
                existing_users = created_users
            
            # Get all users (including newly created ones)
            users = User.query.all()
            print(f"Total users for activity creation: {len(users)}")
            
            for user in users:
                print(f"\nCreating activity data for user: {user.username} (ID: {user.id})")
                
                # Create some portfolios if none exist
                existing_portfolios = Portfolio.query.filter_by(user_id=user.id).count()
                if existing_portfolios == 0:
                    print("Creating sample portfolios...")
                    
                    # Main portfolio
                    main_portfolio = Portfolio(
                        name="Min Hovedportefølje",
                        user_id=user.id,
                        created_at=datetime.utcnow() - timedelta(days=30)
                    )
                    db.session.add(main_portfolio)
                    db.session.flush()  # Get the ID
                    
                    # Add some stocks to portfolio
                    sample_stocks = [
                        {'ticker': 'EQNR.OL', 'quantity': 50, 'purchase_price': 275.50},
                        {'ticker': 'DNB.OL', 'quantity': 30, 'purchase_price': 200.00},
                        {'ticker': 'NHY.OL', 'quantity': 100, 'purchase_price': 62.30}
                    ]
                    
                    for stock_data in sample_stocks:
                        stock = PortfolioStock(
                            portfolio_id=main_portfolio.id,
                            ticker=stock_data['ticker'],
                            quantity=stock_data['quantity'],
                            purchase_price=stock_data['purchase_price'],
                            purchase_date=datetime.utcnow() - timedelta(days=random.randint(1, 25))
                        )
                        db.session.add(stock)
                    
                    print(f"Created portfolio with {len(sample_stocks)} stocks")
                
                # Create watchlists if none exist
                existing_watchlists = Watchlist.query.filter_by(user_id=user.id).count()
                if existing_watchlists == 0:
                    print("Creating sample watchlist...")
                    
                    watchlist = Watchlist(
                        name="Mine Favoritter",
                        user_id=user.id,
                        created_at=datetime.utcnow() - timedelta(days=20)
                    )
                    db.session.add(watchlist)
                    db.session.flush()
                    
                    # Add watchlist items
                    watchlist_tickers = ['AAPL', 'MSFT', 'TSLA', 'NFLX', 'TEL.OL']
                    for ticker in watchlist_tickers:
                        item = WatchlistItem(
                            watchlist_id=watchlist.id,
                            ticker=ticker,
                            added_date=datetime.utcnow() - timedelta(days=random.randint(1, 15))
                        )
                        db.session.add(item)
                    
                    print(f"Created watchlist with {len(watchlist_tickers)} items")

            # Continue with existing logic for users that weren't in the test data
            # Skip duplicate logic as we already processed all users above
            
            # Commit all changes
            db.session.commit()
            print("\n✅ Successfully created user activity data!")
            
            # Verify the data
            users = User.query.all()
            for user in users:
                portfolio_count = Portfolio.query.filter_by(user_id=user.id).count()
                watchlist_count = Watchlist.query.filter_by(user_id=user.id).count()
                
                total_watchlist_items = 0
                user_watchlists = Watchlist.query.filter_by(user_id=user.id).all()
                for wl in user_watchlists:
                    total_watchlist_items += WatchlistItem.query.filter_by(watchlist_id=wl.id).count()
                
                print(f"User {user.username}: {portfolio_count} portfolios, {total_watchlist_items} watchlist items")
                
        except Exception as e:
            print(f"❌ Error creating user data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    create_user_activity_data()
