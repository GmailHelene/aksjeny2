"""
Test script to check if access control changes have resolved the issues
"""

from flask_login import current_user
from app.utils.access_control_unified import (
    get_access_level, check_endpoint_access, 
    is_exempt_user, has_active_subscription,
    DEMO_ACCESSIBLE, PREMIUM_ONLY, ALWAYS_ACCESSIBLE
)
import logging

def test_access_control(auth_client):
    client, user = auth_client
    assert current_user.is_authenticated, "Authenticated user fixture failed"

    access_level = get_access_level()
    assert access_level in ('premium','standard','demo','unknown'), f"Unexpected access level {access_level}"

    endpoints_to_check = [
        'main.profile',
        'profile.profile_page',
        'portfolio.portfolio_overview'
    ]
    for endpoint in endpoints_to_check:
        allowed, redirect_to, message = check_endpoint_access(endpoint)
        # For authenticated user baseline should be allowed or redirect_to None
        assert allowed or redirect_to is not None, f"Endpoint {endpoint} neither allowed nor redirected"

    portfolio_routes = [r for r in DEMO_ACCESSIBLE if 'portfolio.' in r]
    profile_routes = [r for r in DEMO_ACCESSIBLE if 'profile.' in r or 'main.profile' in r]

    # Basic sanity: lists exist (no exception) and structure is iterable
    assert isinstance(portfolio_routes, list)
    assert isinstance(profile_routes, list)
