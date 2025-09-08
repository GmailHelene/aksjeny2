# Comprehensive verification test for access control fixes
from flask import Flask, url_for
from flask_login import current_user, login_user
from app import create_app
from app.models import User
from app.utils.access_control_unified import (
    get_access_level, check_endpoint_access,
    is_exempt_user, has_active_subscription,
    DEMO_ACCESSIBLE, PREMIUM_ONLY, ALWAYS_ACCESSIBLE
)
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_access_control_fixes():
    """Run verification tests on access control changes"""
    logger.info("Starting comprehensive verification of access control fixes...")
    
    # Create test app
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    
    # Check if the important routes are in DEMO_ACCESSIBLE
    portfolio_routes = [r for r in DEMO_ACCESSIBLE if 'portfolio.' in r]
    profile_routes = [r for r in DEMO_ACCESSIBLE if 'profile.' in r or 'main.profile' in r]
    
    logger.info(f"Found {len(portfolio_routes)} portfolio routes in DEMO_ACCESSIBLE")
    logger.info(f"Found {len(profile_routes)} profile routes in DEMO_ACCESSIBLE")
    
    # Check specific important routes
    critical_routes = [
        'portfolio.portfolio_overview',
        'portfolio.view_portfolio',
        'portfolio.create_portfolio',
        'main.profile',
        'profile.profile_page'
    ]
    
    for route in critical_routes:
        if route in DEMO_ACCESSIBLE:
            logger.info(f"✅ {route} is correctly in DEMO_ACCESSIBLE")
        else:
            logger.error(f"❌ {route} is MISSING from DEMO_ACCESSIBLE!")
    
    # Check for conflicts with PREMIUM_ONLY
    conflicts = [r for r in DEMO_ACCESSIBLE if r in PREMIUM_ONLY]
    if conflicts:
        logger.warning(f"Found {len(conflicts)} routes that are in both DEMO_ACCESSIBLE and PREMIUM_ONLY: {conflicts}")
    else:
        logger.info("✅ No conflicts between DEMO_ACCESSIBLE and PREMIUM_ONLY")
    
    # Check diagnostic and test routes in ALWAYS_ACCESSIBLE
    diagnostic_route = 'diagnostic.auth_status'
    test_route = 'test.test_access_control'
    
    if diagnostic_route in ALWAYS_ACCESSIBLE:
        logger.info(f"✅ {diagnostic_route} is correctly in ALWAYS_ACCESSIBLE")
    else:
        logger.error(f"❌ {diagnostic_route} is MISSING from ALWAYS_ACCESSIBLE!")
        
    if test_route in ALWAYS_ACCESSIBLE:
        logger.info(f"✅ {test_route} is correctly in ALWAYS_ACCESSIBLE")
    else:
        logger.error(f"❌ {test_route} is MISSING from ALWAYS_ACCESSIBLE!")
    
    # Check decorator update in portfolio.py
    # This would require additional code to inspect file contents
    
    logger.info("Verification complete")
    
    # Clean up
    app_context.pop()
    
    return {
        'portfolio_routes': portfolio_routes,
        'profile_routes': profile_routes,
        'critical_routes_check': all(route in DEMO_ACCESSIBLE for route in critical_routes),
        'conflicts': conflicts,
        'diagnostic_route_check': diagnostic_route in ALWAYS_ACCESSIBLE,
        'test_route_check': test_route in ALWAYS_ACCESSIBLE
    }

if __name__ == "__main__":
    verify_access_control_fixes()
