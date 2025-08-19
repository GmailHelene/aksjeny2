#!/usr/bin/env python3
"""
Debug script to check why dashboard activity is not showing properly
"""

import sys
sys.path.insert(0, '.')

from app import create_app
from app.models.user import User
from app.models.portfolio import Portfolio, PortfolioStock
from app.models.watchlist import Watchlist, WatchlistItem
from datetime import datetime

def debug_dashboard_activity():
    app = create_app()
    
    with app.app_context():
        print("🔍 Debugging dashboard activity...")
        
        # Check users
        users = User.query.all()
        print(f"📊 Found {len(users)} users:")
        for user in users:
            print(f"  - {user.username} (ID: {user.id})")
            
            # Check portfolios for this user
            portfolios = Portfolio.query.filter_by(user_id=user.id).all()
            print(f"    📁 Portfolios: {len(portfolios)}")
            for portfolio in portfolios:
                stocks = PortfolioStock.query.filter_by(portfolio_id=portfolio.id).all()
                print(f"      - {portfolio.name}: {len(stocks)} stocks")
                for stock in stocks[:3]:  # Show first 3
                    print(f"        • {stock.ticker}: {stock.shares} shares, purchased {stock.purchase_date}")
            
            # Check watchlists for this user
            watchlists = Watchlist.query.filter_by(user_id=user.id).all()
            print(f"    👁️ Watchlists: {len(watchlists)}")
            for watchlist in watchlists:
                items = WatchlistItem.query.filter_by(watchlist_id=watchlist.id).all()
                print(f"      - {watchlist.name}: {len(items)} items")
                for item in items[:3]:  # Show first 3
                    print(f"        • {item.symbol}, added {item.added_at}")
            
            print()
        
        # Now test the actual logic from the route
        print("🧪 Testing user stats calculation for helene_luxus...")
        helene = User.query.filter_by(username='helene_luxus').first()
        if helene:
            print(f"✅ Found user: {helene.username} (ID: {helene.id})")
            
            # Portfolio count
            portfolio_count = Portfolio.query.filter_by(user_id=helene.id).count()
            print(f"📁 Portfolio count: {portfolio_count}")
            
            # Watchlist items count
            user_watchlists = Watchlist.query.filter_by(user_id=helene.id).all()
            total_watchlist_items = 0
            for watchlist in user_watchlists:
                total_watchlist_items += WatchlistItem.query.filter_by(watchlist_id=watchlist.id).count()
            print(f"👁️ Watchlist items count: {total_watchlist_items}")
            
            # Recent activities
            recent_activities = []
            
            # Portfolio activities
            user_portfolios = Portfolio.query.filter_by(user_id=helene.id).order_by(Portfolio.created_at.desc()).limit(2).all()
            print(f"📁 Found {len(user_portfolios)} portfolios for activities")
            for portfolio in user_portfolios:
                recent_stocks = PortfolioStock.query.filter_by(portfolio_id=portfolio.id).order_by(PortfolioStock.purchase_date.desc()).limit(3).all()
                print(f"  - Portfolio '{portfolio.name}': {len(recent_stocks)} recent stocks")
                for stock in recent_stocks:
                    activity = {
                        'type': 'portfolio_add',
                        'icon': 'bi-plus',
                        'color': 'success',
                        'title': f'Lagt til {stock.ticker}',
                        'description': f'i {portfolio.name}',
                        'time_ago': f"Purchase date: {stock.purchase_date}",
                        'purchase_date': stock.purchase_date  # For proper sorting
                    }
                    recent_activities.append(activity)
                    print(f"    • Added activity: {activity['title']} ({activity['time_ago']})")
            
            # Watchlist activities
            print(f"👁️ Found {len(user_watchlists)} watchlists for activities")
            for watchlist in user_watchlists:
                recent_items = WatchlistItem.query.filter_by(watchlist_id=watchlist.id).order_by(WatchlistItem.added_at.desc()).limit(2).all()
                print(f"  - Watchlist '{watchlist.name}': {len(recent_items)} recent items")
                for item in recent_items:
                    activity = {
                        'type': 'watchlist_add',
                        'icon': 'bi-eye',
                        'color': 'info',
                        'title': f'Overvåker {item.symbol}',
                        'description': f'lagt til i {watchlist.name}',
                        'time_ago': f"Added: {item.added_at}",
                        'added_at': item.added_at  # For proper sorting
                    }
                    recent_activities.append(activity)
                    print(f"    • Added activity: {activity['title']} ({activity['time_ago']})")
            
            print(f"\n📊 Total activities found: {len(recent_activities)}")
            
            if recent_activities:
                print("🎯 Recent activities list:")
                for i, activity in enumerate(recent_activities[:4]):
                    print(f"  {i+1}. {activity['title']} - {activity['description']} ({activity['time_ago']})")
            else:
                print("❌ No activities found!")
                
        else:
            print("❌ User 'helene_luxus' not found!")

if __name__ == "__main__":
    debug_dashboard_activity()
