#!/usr/bin/env python3
"""
Comprehensive Cache Clearing Script for Aksjeradar Application
Clears all caches, temporary files, and resets application state
"""

import os
import sys
import shutil
import time
import logging
from pathlib import Path
import sqlite3
import redis
import json
from datetime import datetime

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveCacheClearer:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.cleared_items = []
        self.errors = []

    def clear_flask_cache(self):
        """Clear Flask-Caching cache"""
        try:
            cache_dirs = [
                os.path.join(self.app_root, 'app', 'cache'),
                os.path.join(self.app_root, 'cache'),
                os.path.join(self.app_root, 'flask_cache'),
                '/tmp/flask_cache'
            ]
            
            for cache_dir in cache_dirs:
                if os.path.exists(cache_dir):
                    shutil.rmtree(cache_dir)
                    self.cleared_items.append(f"Flask cache directory: {cache_dir}")
                    logger.info(f"✅ Cleared Flask cache: {cache_dir}")
            
        except Exception as e:
            self.errors.append(f"Flask cache clearing: {e}")
            logger.error(f"❌ Error clearing Flask cache: {e}")

    def clear_database_cache(self):
        """Clear database cache and temporary tables"""
        try:
            db_paths = [
                os.path.join(self.app_root, 'instance', 'database.db'),
                os.path.join(self.app_root, 'app', 'database.db'),
                os.path.join(self.app_root, 'database.db')
            ]
            
            for db_path in db_paths:
                if os.path.exists(db_path):
                    try:
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        
                        # Clear cache tables if they exist
                        cache_tables = [
                            'cache_entries',
                            'temp_data',
                            'session_data',
                            'market_cache',
                            'stock_cache',
                            'crypto_cache'
                        ]
                        
                        for table in cache_tables:
                            try:
                                cursor.execute(f"DELETE FROM {table}")
                                self.cleared_items.append(f"Database cache table: {table}")
                            except sqlite3.OperationalError:
                                # Table doesn't exist, which is fine
                                pass
                        
                        # Vacuum database
                        cursor.execute("VACUUM")
                        conn.commit()
                        conn.close()
                        
                        self.cleared_items.append(f"Database cache cleared: {db_path}")
                        logger.info(f"✅ Cleared database cache: {db_path}")
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Could not clear database cache {db_path}: {e}")
            
        except Exception as e:
            self.errors.append(f"Database cache clearing: {e}")
            logger.error(f"❌ Error clearing database cache: {e}")

    def clear_redis_cache(self):
        """Clear Redis cache if available"""
        try:
            # Try to connect to Redis
            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            r.ping()  # Test connection
            
            # Clear all Redis keys
            keys = r.keys('*')
            if keys:
                r.delete(*keys)
                self.cleared_items.append(f"Redis cache: {len(keys)} keys")
                logger.info(f"✅ Cleared Redis cache: {len(keys)} keys")
            
        except Exception as e:
            logger.info(f"ℹ️ Redis not available or no keys to clear: {e}")

    def clear_file_caches(self):
        """Clear file-based caches"""
        try:
            cache_patterns = [
                '**/__pycache__',
                '**/*.pyc',
                '**/*.pyo',
                '**/cache',
                '**/tmp',
                '**/temp',
                '**/.cache',
                '**/logs/*.log',
                '**/instance/cache',
                '**/static/cache',
                '**/data/cache'
            ]
            
            for pattern in cache_patterns:
                for item in Path(self.app_root).glob(pattern):
                    try:
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                        self.cleared_items.append(f"File cache: {item}")
                        logger.info(f"✅ Cleared file cache: {item}")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not clear {item}: {e}")
            
        except Exception as e:
            self.errors.append(f"File cache clearing: {e}")
            logger.error(f"❌ Error clearing file cache: {e}")

    def clear_session_data(self):
        """Clear session data"""
        try:
            session_dirs = [
                os.path.join(self.app_root, 'flask_session'),
                os.path.join(self.app_root, 'instance', 'sessions'),
                '/tmp/flask_session'
            ]
            
            for session_dir in session_dirs:
                if os.path.exists(session_dir):
                    shutil.rmtree(session_dir)
                    self.cleared_items.append(f"Session directory: {session_dir}")
                    logger.info(f"✅ Cleared sessions: {session_dir}")
            
        except Exception as e:
            self.errors.append(f"Session clearing: {e}")
            logger.error(f"❌ Error clearing sessions: {e}")

    def clear_application_cache(self):
        """Clear application-specific cache"""
        try:
            app_cache_files = [
                'market_data_cache.json',
                'stock_cache.json',
                'crypto_cache.json',
                'news_cache.json',
                'analysis_cache.json'
            ]
            
            for cache_file in app_cache_files:
                cache_path = os.path.join(self.app_root, 'app', 'cache', cache_file)
                if os.path.exists(cache_path):
                    os.remove(cache_path)
                    self.cleared_items.append(f"App cache file: {cache_file}")
                    logger.info(f"✅ Cleared app cache: {cache_file}")
            
        except Exception as e:
            self.errors.append(f"Application cache clearing: {e}")
            logger.error(f"❌ Error clearing application cache: {e}")

    def clear_logs(self):
        """Clear old log files"""
        try:
            log_dirs = [
                os.path.join(self.app_root, 'logs'),
                os.path.join(self.app_root, 'app', 'logs'),
                os.path.join(self.app_root, 'instance', 'logs')
            ]
            
            for log_dir in log_dirs:
                if os.path.exists(log_dir):
                    for log_file in os.listdir(log_dir):
                        if log_file.endswith('.log') and log_file != 'current.log':
                            log_path = os.path.join(log_dir, log_file)
                            os.remove(log_path)
                            self.cleared_items.append(f"Log file: {log_file}")
                            logger.info(f"✅ Cleared log: {log_file}")
            
        except Exception as e:
            self.errors.append(f"Log clearing: {e}")
            logger.error(f"❌ Error clearing logs: {e}")

    def clear_temp_files(self):
        """Clear temporary files"""
        try:
            temp_patterns = [
                '**/*.tmp',
                '**/*.temp',
                '**/nohup.out',
                '**/.DS_Store',
                '**/Thumbs.db'
            ]
            
            for pattern in temp_patterns:
                for item in Path(self.app_root).glob(pattern):
                    try:
                        item.unlink()
                        self.cleared_items.append(f"Temp file: {item.name}")
                        logger.info(f"✅ Cleared temp file: {item}")
                    except Exception as e:
                        logger.warning(f"⚠️ Could not clear temp file {item}: {e}")
            
        except Exception as e:
            self.errors.append(f"Temp file clearing: {e}")
            logger.error(f"❌ Error clearing temp files: {e}")

    def run_comprehensive_clear(self):
        """Run comprehensive cache clearing"""
        logger.info("🧹 Starting comprehensive cache clearing...")
        start_time = time.time()
        
        # Run all clearing operations
        self.clear_flask_cache()
        self.clear_database_cache()
        self.clear_redis_cache()
        self.clear_file_caches()
        self.clear_session_data()
        self.clear_application_cache()
        self.clear_logs()
        self.clear_temp_files()
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'cleared_items_count': len(self.cleared_items),
            'cleared_items': self.cleared_items,
            'errors_count': len(self.errors),
            'errors': self.errors
        }
        
        # Save report
        report_path = os.path.join(self.app_root, 'cache_clear_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        logger.info(f"🎉 Cache clearing completed in {duration} seconds")
        logger.info(f"✅ Cleared {len(self.cleared_items)} items")
        if self.errors:
            logger.warning(f"⚠️ {len(self.errors)} errors occurred")
        logger.info(f"📄 Report saved to: {report_path}")
        
        return report

def main():
    """Main function"""
    print("🧹 Aksjeradar Comprehensive Cache Clearer")
    print("=========================================")
    
    clearer = ComprehensiveCacheClearer()
    report = clearer.run_comprehensive_clear()
    
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ Items cleared: {report['cleared_items_count']}")
    print(f"   ⚠️ Errors: {report['errors_count']}")
    print(f"   ⏱️ Duration: {report['duration_seconds']} seconds")
    
    if report['errors']:
        print("\n❌ ERRORS:")
        for error in report['errors']:
            print(f"   • {error}")
    
    print(f"\n📄 Full report: cache_clear_report.json")
    print("✨ Cache clearing complete!")

if __name__ == "__main__":
    main()
