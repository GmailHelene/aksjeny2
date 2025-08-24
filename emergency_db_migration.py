#!/usr/bin/env python3
"""
Emergency database migration to fix production 500 errors
Run this on Railway production to create missing tables
"""
import os
import sys
import logging
from datetime import datetime

# Add app to path
sys.path.insert(0, '/app')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def emergency_db_migration():
    """Emergency migration to create missing tables"""
    try:
        # Set DATABASE_URL from environment if available
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            logger.info(f"Using DATABASE_URL: {database_url[:50]}...")
        else:
            logger.warning("No DATABASE_URL found in environment")

        # Import app and models
        from app import create_app, db
        from app.models import (
            UserStats, Watchlist, WatchlistStock, 
            Achievement, UserAchievement
        )
        
        app = create_app()
        
        with app.app_context():
            logger.info("🚀 Starting emergency database migration...")
            
            # Create all tables
            db.create_all()
            logger.info("✅ Database tables created/updated successfully")
            
            # Test critical tables
            test_results = {}
            
            # Test UserStats
            try:
                count = UserStats.query.count()
                test_results['user_stats'] = f"✅ OK ({count} records)"
                logger.info(f"UserStats table: {count} records")
            except Exception as e:
                test_results['user_stats'] = f"❌ ERROR: {e}"
                logger.error(f"UserStats table error: {e}")
            
            # Test Watchlist
            try:
                count = Watchlist.query.count()
                test_results['watchlist'] = f"✅ OK ({count} records)"
                logger.info(f"Watchlist table: {count} records")
            except Exception as e:
                test_results['watchlist'] = f"❌ ERROR: {e}"
                logger.error(f"Watchlist table error: {e}")
            
            # Test WatchlistStock
            try:
                count = WatchlistStock.query.count()
                test_results['watchlist_stock'] = f"✅ OK ({count} records)"
                logger.info(f"WatchlistStock table: {count} records")
            except Exception as e:
                test_results['watchlist_stock'] = f"❌ ERROR: {e}"
                logger.error(f"WatchlistStock table error: {e}")
            
            # Test Achievement
            try:
                count = Achievement.query.count()
                test_results['achievement'] = f"✅ OK ({count} records)"
                logger.info(f"Achievement table: {count} records")
            except Exception as e:
                test_results['achievement'] = f"❌ ERROR: {e}"
                logger.error(f"Achievement table error: {e}")
            
            # Test UserAchievement
            try:
                count = UserAchievement.query.count()
                test_results['user_achievement'] = f"✅ OK ({count} records)"
                logger.info(f"UserAchievement table: {count} records")
            except Exception as e:
                test_results['user_achievement'] = f"❌ ERROR: {e}"
                logger.error(f"UserAchievement table error: {e}")
            
            # Print results summary
            logger.info("=" * 60)
            logger.info("EMERGENCY DATABASE MIGRATION COMPLETE")
            logger.info("=" * 60)
            for table, status in test_results.items():
                logger.info(f"{table}: {status}")
            logger.info("=" * 60)
            
            # Check if all tables are working
            all_ok = all("✅" in status for status in test_results.values())
            if all_ok:
                logger.info("🎉 ALL CRITICAL TABLES ARE WORKING!")
                logger.info("500 errors should now be resolved.")
            else:
                logger.warning("⚠️  Some tables still have issues.")
                logger.warning("Manual intervention may be required.")
                
            return all_ok
            
    except Exception as e:
        logger.error(f"💥 MIGRATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = emergency_db_migration()
    sys.exit(0 if success else 1)
