#!/usr/bin/env python3
"""
Create missing database tables for production deployment
"""
from app import create_app, db
from app.models import UserStats, Watchlist, WatchlistStock, Achievement, UserAchievement
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_missing_tables():
    """Create any missing database tables"""
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Creating missing database tables...")
            
            # Create all tables
            db.create_all()
            
            logger.info("✅ All database tables created successfully!")
            
            # Check if user_stats table exists by trying to query it
            try:
                existing_stats = UserStats.query.count()
                logger.info(f"✅ user_stats table accessible with {existing_stats} records")
            except Exception as e:
                logger.error(f"❌ user_stats table issue: {e}")
            
            # Check if watchlist tables exist
            try:
                existing_watchlists = Watchlist.query.count()
                existing_watchlist_stocks = WatchlistStock.query.count()
                logger.info(f"✅ watchlist tables accessible: {existing_watchlists} watchlists, {existing_watchlist_stocks} stocks")
            except Exception as e:
                logger.error(f"❌ watchlist tables issue: {e}")
            
            # Check if achievement tables exist
            try:
                existing_achievements = Achievement.query.count()
                existing_user_achievements = UserAchievement.query.count()
                logger.info(f"✅ achievement tables accessible: {existing_achievements} achievements, {existing_user_achievements} user achievements")
            except Exception as e:
                logger.error(f"❌ achievement tables issue: {e}")
                
        except Exception as e:
            logger.error(f"❌ Error creating tables: {e}")
            raise

if __name__ == '__main__':
    create_missing_tables()
