#!/usr/bin/env python3

from app import create_app
from app.models import User, Portfolio, PortfolioStock, Watchlist
from app.models.watchlist import WatchlistItem
from datetime import datetime

def test_user_dashboard():
    app = create_app()
    
    with app.app_context():
        # Test with helene_luxus user
        print("Searching for user 'helene_luxus'...")
        user = User.query.filter_by(username='helene_luxus').first()
        if not user:
            print("❌ User helene_luxus not found, trying all users...")
            users = User.query.all()
            print(f"Found {len(users)} users:")
            for u in users:
                print(f"  - {u.username}")
            # Use first user instead
            if users:
                user = users[0]
                print(f"Using first user: {user.username}")
            else:
                print("❌ No users found at all")
                return
            
        print(f"✅ Found user: {user.username}")
        
        # Get portfolios and watchlists  
        portfolios = Portfolio.query.filter_by(user_id=user.id).all()
        watchlists = Watchlist.query.filter_by(user_id=user.id).all()
        
        print(f"📊 User has {len(portfolios)} portfolios and {len(watchlists)} watchlists")
        
        # Test user_stats calculation like in main.py
        total_value = 0
        total_gain_loss = 0
        recent_activities = []
        
        for portfolio in portfolios:
            portfolio_stocks = PortfolioStock.query.filter_by(portfolio_id=portfolio.id).all()
            print(f"Portfolio '{portfolio.name}' has {len(portfolio_stocks)} stocks")
            
            for stock in portfolio_stocks:
                # Add to recent activities
                recent_activities.append({
                    'type': 'portfolio_add',
                    'description': f'Lagt til {stock.symbol}',
                    'time': '2 timer siden',
                    'stock': stock.symbol
                })
                print(f"  - {stock.symbol}: {stock.shares} shares at ${stock.purchase_price}")
                
        for watchlist in watchlists:
            watchlist_items = WatchlistItem.query.filter_by(watchlist_id=watchlist.id).all()
            print(f"Watchlist '{watchlist.name}' has {len(watchlist_items)} items")
            
            for item in watchlist_items:
                # Add to recent activities  
                recent_activities.append({
                    'type': 'watchlist_add',
                    'description': f'Søkte etter {item.symbol}',
                    'time': '1 time siden',
                    'stock': item.symbol
                })
                print(f"  - {item.symbol}")
        
        # Sort activities by most recent first (limited to 5)
        recent_activities = recent_activities[:5]
        
        user_stats = {
            'total_value': total_value,
            'total_gain_loss': total_gain_loss,
            'portfolios_count': len(portfolios),
            'watchlists_count': len(watchlists),
            'recent_activities': recent_activities
        }
        
        print(f"\n📈 User Stats:")
        print(f"  Portfolios: {user_stats['portfolios_count']}")
        print(f"  Watchlists: {user_stats['watchlists_count']}")
        print(f"  Recent Activities: {len(user_stats['recent_activities'])}")
        
        if user_stats['recent_activities']:
            print(f"\n🔥 Recent Activities:")
            for activity in user_stats['recent_activities']:
                print(f"  - {activity['description']} ({activity['time']})")
        else:
            print(f"\n❌ No recent activities found!")
            
        return user_stats

if __name__ == "__main__":
    test_user_dashboard()
