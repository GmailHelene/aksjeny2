#!/usr/bin/env python3

from app import create_app, db
from app.models.user import User
from app.models.portfolio import Portfolio, PortfolioStock
from app.models.watchlist import Watchlist, WatchlistItem
from datetime import datetime, timedelta
import random

def create_user_activity_data():
    """Create realistic user activity data for testing the dashboard"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if users exist
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
            
            # Norwegian stocks for realistic portfolio data
            norwegian_stocks = [
                'EQNR.OL', 'DNB.OL', 'NORSK.OL', 'TEL.OL', 'MOWI.OL',
                'YAR.OL', 'SALM.OL', 'NHY.OL', 'AKER.OL', 'XXL.OL',
                'ORKLA.OL', 'GAMING.OL', 'LSG.OL', 'SUBSEA.OL', 'AUTO.OL'
            ]
            
            # Create realistic portfolios and watchlists for each user
            for user in existing_users:
                print(f"Creating activity for user: {user.username}")
                
                # Create 1-2 portfolios per user
                num_portfolios = random.randint(1, 2)
                for i in range(num_portfolios):
                    portfolio_name = f"{user.username}'s {'Main' if i == 0 else 'Growth'} Portfolio"
                    
                    # Check if portfolio already exists
                    existing_portfolio = Portfolio.query.filter_by(user_id=user.id, name=portfolio_name).first()
                    if existing_portfolio:
                        print(f"  Portfolio {portfolio_name} already exists")
                        continue
                    
                    portfolio = Portfolio(
                        name=portfolio_name,
                        user_id=user.id,
                        created_at=datetime.utcnow() - timedelta(days=random.randint(30, 365))
                    )
                    db.session.add(portfolio)
                    db.session.flush()  # Get the ID
                    
                    # Add 3-8 stocks to portfolio
                    num_stocks = random.randint(3, 8)
                    selected_stocks = random.sample(norwegian_stocks, min(num_stocks, len(norwegian_stocks)))
                    
                    for symbol in selected_stocks:
                        stock = PortfolioStock(
                            portfolio_id=portfolio.id,
                            ticker=symbol,  # Use 'ticker' instead of 'symbol'
                            shares=random.randint(10, 1000),  # Use 'shares' instead of 'quantity'
                            purchase_price=random.uniform(50, 500),
                            purchase_date=datetime.utcnow() - timedelta(days=random.randint(1, 180))
                        )
                        db.session.add(stock)
                    
                    print(f"  Created portfolio: {portfolio_name} with {num_stocks} stocks")
                
                # Create 1-3 watchlists per user
                num_watchlists = random.randint(1, 3)
                for i in range(num_watchlists):
                    watchlist_names = ['Tech Stocks', 'Dividend Stocks', 'Growth Plays', 'Value Picks']
                    watchlist_name = f"{user.username}'s {random.choice(watchlist_names)}"
                    
                    # Check if watchlist already exists
                    existing_watchlist = Watchlist.query.filter_by(user_id=user.id, name=watchlist_name).first()
                    if existing_watchlist:
                        print(f"  Watchlist {watchlist_name} already exists")
                        continue
                    
                    watchlist = Watchlist(
                        name=watchlist_name,
                        user_id=user.id,
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 180))
                    )
                    db.session.add(watchlist)
                    db.session.flush()  # Get the ID
                    
                    # Add 2-6 stocks to watchlist
                    num_stocks = random.randint(2, 6)
                    selected_stocks = random.sample(norwegian_stocks, min(num_stocks, len(norwegian_stocks)))
                    
                    for symbol in selected_stocks:
                        item = WatchlistItem(
                            watchlist_id=watchlist.id,
                            symbol=symbol,
                            added_at=datetime.utcnow() - timedelta(days=random.randint(1, 90))
                        )
                        db.session.add(item)
                    
                    print(f"  Created watchlist: {watchlist_name} with {num_stocks} stocks")
            
            # Commit all changes
            db.session.commit()
            print("✅ Successfully created user activity data!")
            
            # Verify the data
            total_portfolios = Portfolio.query.count()
            total_stocks = PortfolioStock.query.count()
            total_watchlists = Watchlist.query.count()
            total_watchlist_items = WatchlistItem.query.count()
            
            print(f"\n📊 Data Summary:")
            print(f"   Users: {len(existing_users)}")
            print(f"   Portfolios: {total_portfolios}")
            print(f"   Portfolio Stocks: {total_stocks}")
            print(f"   Watchlists: {total_watchlists}")
            print(f"   Watchlist Items: {total_watchlist_items}")
            
        except Exception as e:
            print(f"❌ Error creating user data: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    create_user_activity_data()
