"""Diagnostic blueprint route for access control.

This route intentionally does NOT execute the pytest test function
`test_access_control` (which depends on fixtures like `auth_client`).
Instead it performs a lightweight, side‑effect free diagnostic using the
same underlying access control utilities and returns a JSON report.

Important: The previous implementation imported and executed the pytest
test directly, which caused runtime errors (fixture injection missing)
and made the file itself look like a test module to pytest. We rename
the function to avoid collection and remove the direct test invocation.
"""

from flask import Blueprint, jsonify, current_app
from flask_login import current_user

# Prevent pytest from collecting anything in this module as tests
__all__ = ["access_control_check"]

test = Blueprint('test', __name__, url_prefix='/test')

@test.route('/access-control')
def access_control_check():
    """Return a structured JSON snapshot of access control state."""
    report = {
        'status': 'ok',
        'errors': [],
        'user': {},
        'diagnostics': {}
    }
    try:
        # Basic user info
        user_info = {
            'id': getattr(current_user, 'id', None),
            'email': getattr(current_user, 'email', None) if current_user.is_authenticated else None,
            'is_authenticated': current_user.is_authenticated
        }
        report['user'] = user_info

        # Import access control utilities lazily to avoid circular imports
        from app.utils.access_control_unified import (
            get_access_level, check_endpoint_access, DEMO_ACCESSIBLE, PREMIUM_ONLY, ALWAYS_ACCESSIBLE
        )

        access_level = get_access_level()
        report['diagnostics']['access_level'] = access_level

        # Representative endpoints to probe
        endpoints_to_check = [
            'main.profile',
            'profile.profile_page',
            'portfolio.portfolio_overview'
        ]
        endpoint_results = {}
        for ep in endpoints_to_check:
            try:
                allowed, redirect_to, message = check_endpoint_access(ep)
                endpoint_results[ep] = {
                    'allowed': allowed,
                    'redirect_to': redirect_to,
                    'message': message
                }
            except Exception as inner_e:
                endpoint_results[ep] = {'error': str(inner_e)}
                report['errors'].append(f"endpoint_check:{ep}:{inner_e}")
        report['diagnostics']['endpoints'] = endpoint_results

        # Summaries
        report['diagnostics']['counts'] = {
            'always_accessible': len(ALWAYS_ACCESSIBLE),
            'demo_accessible': len(DEMO_ACCESSIBLE),
            'premium_only': len(PREMIUM_ONLY)
        }

    except Exception as e:
        # Capture any unexpected top-level error
        try:
            current_app.logger.error(f"Access control diagnostic error: {e}")
        except Exception:
            pass
        report['status'] = 'error'
        report['errors'].append(str(e))

    return jsonify(report), (200 if report['status'] == 'ok' else 500)

