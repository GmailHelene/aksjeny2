"""
Stock Details Debug - Special diagnostic tool to troubleshoot TradingView integration
"""
from flask import Blueprint, render_template, current_app, request, jsonify
from flask_login import current_user
from ..utils.access_control import demo_access
import traceback
import datetime  # Add missing import

# Create blueprint for stock details diagnostics
details_debug = Blueprint('details_debug', __name__)

@details_debug.route('/debug/<symbol>')
@demo_access
def debug_details(symbol):
    """Diagnostic page for stock details with TradingView troubleshooting"""
    try:
        # Log access
        current_app.logger.info(f"DEBUG: Accessing details debug page for {symbol}")
        
        # User info for diagnostics
        user_info = {
            'is_authenticated': current_user.is_authenticated,
            'user_agent': request.headers.get('User-Agent', 'Unknown'),
            'referrer': request.referrer,
            'remote_addr': request.remote_addr,
        }
        
        if current_user.is_authenticated:
            if hasattr(current_user, 'email'):
                user_info['email'] = current_user.email
            if hasattr(current_user, 'username'):
                user_info['username'] = current_user.username
            if hasattr(current_user, 'subscription_type'):
                user_info['subscription_type'] = current_user.subscription_type
                
        # Render simplified diagnostic template
        return render_template('diagnostics/tradingview_debug.html',
                               symbol=symbol,
                               user_info=user_info)
                               
    except Exception as e:
        current_app.logger.error(f"Error in debug_details for {symbol}: {e}")
        current_app.logger.error(f"Full traceback: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@details_debug.route('/debug-api/<symbol>')
@demo_access
def debug_details_api(symbol):
    """API endpoint for diagnostics to test if API calls work"""
    try:
        from ..services.data_service import DataService
        
        # Basic stock info
        stock_info = {
            'symbol': symbol,
            'price': 100.0,
            'name': f"Debug {symbol}",
            'api_reachable': True,
            'current_time': str(datetime.datetime.now())
        }
        
        # Try to get real data if possible
        try:
            real_data = DataService.get_stock_info(symbol)
            if real_data and isinstance(real_data, dict):
                stock_info['real_data_available'] = True
                stock_info['price'] = real_data.get('regularMarketPrice', real_data.get('last_price', 0))
                stock_info['name'] = real_data.get('name', real_data.get('longName', symbol))
        except Exception as data_error:
            stock_info['real_data_available'] = False
            stock_info['data_error'] = str(data_error)
        
        return jsonify(stock_info)
        
    except Exception as e:
        current_app.logger.error(f"Error in debug_details_api for {symbol}: {e}")
        return jsonify({
            'error': str(e),
            'api_reachable': False
        }), 500

# Register blueprint in the app
def register_details_debug_blueprint(app):
    app.register_blueprint(details_debug, url_prefix='/stocks/details-debug')
