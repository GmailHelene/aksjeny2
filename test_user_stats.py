#!/usr/bin/env python3
"""
Test script to verify user stats are working correctly
"""
from app import create_app
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.watchlist import Watchlist, WatchlistItem
from flask_login import login_user
from flask import url_for

def test_user_stats():
    app = create_app()
    
    with app.app_context():
        with app.test_request_context():
            # Get a test user
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return
            
            print(f"Testing with user: {user.username}")
            
            # Get user stats manually (simulating what main.py does)
            try:
                portfolios_count = Portfolio.query.filter_by(user_id=user.id).count()
                print(f"  Portfolios: {portfolios_count}")
                
                user_watchlists = Watchlist.query.filter_by(user_id=user.id).all()
                total_watchlist_items = 0
                for watchlist in user_watchlists:
                    items_count = WatchlistItem.query.filter_by(watchlist_id=watchlist.id).count()
                    total_watchlist_items += items_count
                    print(f"  Watchlist '{watchlist.name}': {items_count} items")
                
                print(f"  Total watchlist items: {total_watchlist_items}")
                
                if portfolios_count > 0 and total_watchlist_items > 0:
                    print("✅ User has activity data - dashboard should show real data")
                else:
                    print("⚠️ User has no activity data - dashboard will show defaults")
                
                # Test recent activities logic
                from app.models.portfolio import PortfolioStock
                recent_stocks = PortfolioStock.query.join(Portfolio).filter(
                    Portfolio.user_id == user.id
                ).order_by(PortfolioStock.purchase_date.desc()).limit(3).all()
                
                print(f"  Recent stocks added: {len(recent_stocks)}")
                for stock in recent_stocks:
                    print(f"    - {stock.ticker} on {stock.purchase_date}")
                
            except Exception as e:
                print(f"❌ Error getting user stats: {e}")

if __name__ == "__main__":
    test_user_stats()
