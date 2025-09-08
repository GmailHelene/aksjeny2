"""
Test script to check if access control changes have resolved the issues
"""

from flask import url_for, request
from flask_login import current_user
from app.utils.access_control_unified import (
    get_access_level, check_endpoint_access, 
    is_exempt_user, has_active_subscription,
    DEMO_ACCESSIBLE, PREMIUM_ONLY, ALWAYS_ACCESSIBLE
)
import logging

def test_access_control():
    """Test if access control changes have fixed the issues"""
    logging.info("Running access control test...")
    
    # Check user status
    logging.info(f"Current user: authenticated={current_user.is_authenticated}")
    
    if current_user.is_authenticated:
        # Check access level
        access_level = get_access_level()
        logging.info(f"Access level: {access_level}")
        
        # Check important endpoints
        endpoints_to_check = [
            'main.profile',
            'profile.profile_page',
            'portfolio.portfolio_overview',
            'portfolio.view_portfolio',
            'portfolio.create_portfolio'
        ]
        
        for endpoint in endpoints_to_check:
            allowed, redirect_to, message = check_endpoint_access(endpoint)
            logging.info(f"Endpoint {endpoint}: allowed={allowed}, redirect_to={redirect_to}")
            
            # Check if endpoint is in our lists
            in_demo = endpoint in DEMO_ACCESSIBLE
            in_premium = endpoint in PREMIUM_ONLY
            in_always = endpoint in ALWAYS_ACCESSIBLE
            
            logging.info(f"  In DEMO_ACCESSIBLE: {in_demo}")
            logging.info(f"  In PREMIUM_ONLY: {in_premium}")
            logging.info(f"  In ALWAYS_ACCESSIBLE: {in_always}")
    else:
        logging.info("No authenticated user to test with")
    
    # List all routes in DEMO_ACCESSIBLE related to portfolio and profile
    portfolio_routes = [r for r in DEMO_ACCESSIBLE if 'portfolio.' in r]
    profile_routes = [r for r in DEMO_ACCESSIBLE if 'profile.' in r or 'main.profile' in r]
    
    logging.info(f"Portfolio routes in DEMO_ACCESSIBLE: {portfolio_routes}")
    logging.info(f"Profile routes in DEMO_ACCESSIBLE: {profile_routes}")
    
    logging.info("Access control test complete")
    
    return {
        'authenticated': current_user.is_authenticated,
        'access_level': get_access_level() if current_user.is_authenticated else 'none',
        'is_exempt': is_exempt_user() if current_user.is_authenticated else False,
        'has_subscription': has_active_subscription() if current_user.is_authenticated else False,
        'portfolio_routes': portfolio_routes,
        'profile_routes': profile_routes
    }
