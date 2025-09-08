"""
Test route to verify access control changes
"""

from flask import Blueprint, jsonify, render_template, current_app
from flask_login import current_user
import logging

# Create a blueprint for testing
test = Blueprint('test', __name__, url_prefix='/test')

@test.route('/access-control')
def test_access_control():
    """Test if access control changes have fixed the issues"""
    try:
        # Import test function
        from test_access_control import test_access_control as run_test
        
        # Run the test
        results = run_test()
        
        # Add user details
        user_info = {
            'id': getattr(current_user, 'id', None),
            'email': getattr(current_user, 'email', None) if current_user.is_authenticated else None,
            'is_authenticated': current_user.is_authenticated
        }
        
        # Return results as JSON
        return jsonify({
            'user': user_info,
            'test_results': results
        })
    except Exception as e:
        current_app.logger.error(f"Error running access control test: {e}")
        return jsonify({
            'error': str(e)
        }), 500
