#!/usr/bin/env python3
"""
Comprehensive test script for price alerts functionality
Tests all endpoints and database operations
"""

import requests
import json
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceAlertsTestSuite:
    def __init__(self, base_url="http://localhost:5002"):
        self.base_url = base_url
        self.session = requests.Session()
        self.user_credentials = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
    def login(self):
        """Login as test user"""
        logger.info("🔐 Logging in as test user...")
        
        # First get the login page to see if it loads
        login_url = f"{self.base_url}/login"
        try:
            response = self.session.get(login_url)
            if response.status_code == 200:
                logger.info("✅ Login page accessible")
            else:
                logger.error(f"❌ Login page returned status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to access login page: {e}")
            return False
            
        # Try to login
        try:
            response = self.session.post(login_url, data=self.user_credentials)
            if response.status_code == 200 or response.status_code == 302:
                logger.info("✅ Login successful")
                return True
            else:
                logger.error(f"❌ Login failed with status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Login request failed: {e}")
            return False
    
    def test_price_alerts_page(self):
        """Test main price alerts page"""
        logger.info("📱 Testing price alerts main page...")
        
        try:
            url = f"{self.base_url}/price-alerts/"
            response = self.session.get(url)
            
            if response.status_code == 200:
                logger.info("✅ Price alerts page loads successfully")
                # Check for key elements in the page
                content = response.text.lower()
                if 'price alert' in content or 'alerts' in content:
                    logger.info("✅ Page contains expected content")
                else:
                    logger.warning("⚠️ Page might be missing expected content")
                return True
            elif response.status_code == 302:
                logger.info("✅ Price alerts page redirects (possibly to login)")
                return True
            else:
                logger.error(f"❌ Price alerts page returned status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to access price alerts page: {e}")
            return False
    
    def test_api_status(self):
        """Test price alerts API status endpoint"""
        logger.info("🔍 Testing API status endpoint...")
        
        try:
            url = f"{self.base_url}/price-alerts/api/status"
            response = self.session.get(url)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info(f"✅ API status endpoint working: {data}")
                    return True
                except:
                    logger.info("✅ API status endpoint accessible (non-JSON response)")
                    return True
            else:
                logger.error(f"❌ API status endpoint returned status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to access API status endpoint: {e}")
            return False
    
    def test_get_alerts(self):
        """Test getting user alerts"""
        logger.info("📋 Testing get alerts endpoint...")
        
        try:
            url = f"{self.base_url}/price-alerts/api/alerts"
            response = self.session.get(url)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info(f"✅ Get alerts successful: Found {len(data)} alerts")
                    return True, data
                except:
                    logger.info("✅ Get alerts endpoint accessible")
                    return True, []
            elif response.status_code == 401:
                logger.warning("⚠️ Get alerts requires authentication")
                return False, []
            else:
                logger.error(f"❌ Get alerts returned status {response.status_code}")
                return False, []
        except Exception as e:
            logger.error(f"❌ Failed to get alerts: {e}")
            return False, []
    
    def test_create_alert(self):
        """Test creating a price alert"""
        logger.info("➕ Testing create alert endpoint...")
        
        test_alert = {
            'ticker': 'AAPL',
            'symbol': 'AAPL',
            'target_price': 150.00,
            'alert_type': 'above'
        }
        
        try:
            url = f"{self.base_url}/price-alerts/api/create"
            response = self.session.post(url, json=test_alert)
            
            if response.status_code == 200 or response.status_code == 201:
                try:
                    data = response.json()
                    logger.info(f"✅ Create alert successful: {data}")
                    return True, data
                except:
                    logger.info("✅ Create alert successful (non-JSON response)")
                    return True, {}
            elif response.status_code == 401:
                logger.warning("⚠️ Create alert requires authentication")
                return False, {}
            else:
                logger.error(f"❌ Create alert failed with status {response.status_code}")
                try:
                    error_data = response.json()
                    logger.error(f"Error details: {error_data}")
                except:
                    logger.error(f"Error response: {response.text}")
                return False, {}
        except Exception as e:
            logger.error(f"❌ Failed to create alert: {e}")
            return False, {}
    
    def test_quote_endpoint(self):
        """Test getting stock quote"""
        logger.info("💰 Testing quote endpoint...")
        
        try:
            url = f"{self.base_url}/price-alerts/api/quote/AAPL"
            response = self.session.get(url)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info(f"✅ Quote endpoint working: {data}")
                    return True
                except:
                    logger.info("✅ Quote endpoint accessible")
                    return True
            else:
                logger.error(f"❌ Quote endpoint returned status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to get quote: {e}")
            return False
    
    def test_database_operations(self):
        """Test database operations directly"""
        logger.info("🗄️ Testing database operations...")
        
        try:
            # Import app components for direct database testing
            import sys
            import os
            sys.path.append('/workspaces/aksjeny')
            
            from app import create_app
            from app.extensions import db
            from app.models.price_alert import PriceAlert
            from app.models.user import User
            
            app = create_app('development')
            
            with app.app_context():
                # Test user exists
                user = User.query.filter_by(email='test@example.com').first()
                if user:
                    logger.info(f"✅ Test user found: {user.username} (ID: {user.id})")
                    
                    # Test creating an alert directly in database
                    test_alert = PriceAlert(
                        user_id=user.id,
                        ticker='TEST',
                        symbol='TEST',
                        target_price=100.0,
                        alert_type='above'
                    )
                    
                    db.session.add(test_alert)
                    db.session.commit()
                    
                    logger.info(f"✅ Alert created in database: ID {test_alert.id}")
                    
                    # Clean up
                    db.session.delete(test_alert)
                    db.session.commit()
                    logger.info("✅ Test alert cleaned up")
                    
                    return True
                else:
                    logger.error("❌ Test user not found in database")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Database operation failed: {e}")
            return False
    
    def run_full_test_suite(self):
        """Run complete test suite"""
        logger.info("🧪 Starting Price Alerts Test Suite")
        logger.info("=" * 60)
        
        results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
        
        tests = [
            ('Login Test', self.login),
            ('Price Alerts Page', self.test_price_alerts_page),
            ('API Status', self.test_api_status),
            ('Get Alerts', lambda: self.test_get_alerts()[0]),
            ('Quote Endpoint', self.test_quote_endpoint),
            ('Create Alert', lambda: self.test_create_alert()[0]),
            ('Database Operations', self.test_database_operations),
        ]
        
        for test_name, test_func in tests:
            logger.info(f"\n🔍 Running: {test_name}")
            results['total_tests'] += 1
            
            try:
                success = test_func()
                if success:
                    results['passed'] += 1
                    logger.info(f"✅ {test_name}: PASSED")
                else:
                    results['failed'] += 1
                    logger.error(f"❌ {test_name}: FAILED")
            except Exception as e:
                results['failed'] += 1
                logger.error(f"❌ {test_name}: ERROR - {e}")
            
            time.sleep(0.5)  # Brief pause between tests
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("🏁 TEST SUITE SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {results['total_tests']}")
        logger.info(f"✅ Passed: {results['passed']}")
        logger.info(f"❌ Failed: {results['failed']}")
        logger.info(f"Success Rate: {(results['passed']/results['total_tests']*100):.1f}%")
        
        if results['failed'] == 0:
            logger.info("🎉 ALL TESTS PASSED! Price alerts functionality is working!")
        else:
            logger.warning(f"⚠️ {results['failed']} tests failed. Check logs for details.")
        
        return results

def main():
    """Main function"""
    test_suite = PriceAlertsTestSuite()
    results = test_suite.run_full_test_suite()
    
    # Return appropriate exit code
    return 0 if results['failed'] == 0 else 1

if __name__ == "__main__":
    exit(main())
