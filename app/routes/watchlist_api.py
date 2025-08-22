"""
API routes for watchlist operations.
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..extensions import csrf
from ..services.watchlist_service import WatchlistService
import logging

watchlist_api = Blueprint('watchlist_api', __name__)
logger = logging.getLogger(__name__)

@watchlist_api.route('/api/watchlist/data')
@login_required
def get_watchlist_data():
    """Get watchlist data with real-time prices"""
    try:
        stocks = WatchlistService.get_watchlist_data(current_user.id)
        return jsonify({
            'success': True,
            'stocks': stocks
        })
    except Exception as e:
        logger.error(f"Error getting watchlist data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@watchlist_api.route('/api/watchlist/add', methods=['POST'])
@csrf.exempt
@login_required
def add_to_watchlist():
    """Add stock to watchlist"""
    try:
        data = request.get_json()
        if not data or 'symbol' not in data:
            return jsonify({
                'success': False,
                'error': 'Symbol er påkrevd'
            }), 400
            
        symbol = data['symbol'].strip().upper()
        success, message = WatchlistService.add_to_watchlist(
            current_user.id,
            symbol,
            name=data.get('name')
        )
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        logger.error(f"Error adding to watchlist: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@watchlist_api.route('/api/watchlist/remove', methods=['POST'])
@csrf.exempt
@login_required
def remove_from_watchlist():
    """Remove stock from watchlist"""
    try:
        data = request.get_json()
        if not data or 'symbol' not in data:
            return jsonify({
                'success': False,
                'error': 'Symbol er påkrevd'
            }), 400
            
        symbol = data['symbol'].strip().upper()
        success, message = WatchlistService.remove_from_watchlist(
            current_user.id,
            symbol
        )
        
        return jsonify({
            'success': success,
            'message': message
        })
        
    except Exception as e:
        logger.error(f"Error removing from watchlist: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
