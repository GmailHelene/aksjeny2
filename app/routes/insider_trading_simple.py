"""
Simplified Insider Trading Routes for Aksjeradar
Fixed version for basic functionality
"""

import logging
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import current_user, login_required

from ..services.data_service import DataService
from ..utils.access_control import access_required, demo_access

# Create blueprint
insider_trading = Blueprint('insider_trading', __name__)
logger = logging.getLogger(__name__)

@insider_trading.route('/')
@demo_access
def index():
    """Enhanced insider trading main page"""
    try:
        # Get recent insider trading data
        insider_data = DataService.get_insider_trading_data() or []
        
        # Get popular stocks for sidebar
        popular_stocks = DataService.get_popular_stocks() or []
        
        # Mock market statistics
        market_stats = {
            'total_buys': 127,
            'total_sells': 89,
            'total_value': '1.2B'
        }
        
        # Top active stocks
        top_active_stocks = [
            {'symbol': 'EQNR', 'activity': '12'},
            {'symbol': 'TEL', 'activity': '8'},
            {'symbol': 'NOK', 'activity': '6'},
            {'symbol': 'DNB', 'activity': '5'},
            {'symbol': 'MOWI', 'activity': '4'}
        ]
        
        return render_template('insider_trading/index.html',
                             insider_data=insider_data[:20],  # Latest 20
                             popular_stocks=popular_stocks,
                             market_stats=market_stats,
                             top_active_stocks=top_active_stocks,
                             hot_stocks_count=24,
                             signal_count=12,
                             alerts_count=7,
                             insider_summary={
                                 'total_buys': 67,
                                 'total_sells': 32,
                                 'net_value': '45.6M',
                                 'unique_insiders': 156
                             })
    except Exception as e:
        logger.error(f"Error in insider trading index: {e}")
        return render_template('insider_trading/index.html',
                             insider_data=[],
                             popular_stocks=[],
                             market_stats={'total_buys': 0, 'total_sells': 0, 'total_value': '0'},
                             top_active_stocks=[],
                             hot_stocks_count=0,
                             signal_count=0,
                             alerts_count=0,
                             insider_summary={'total_buys': 0, 'total_sells': 0, 'net_value': '0', 'unique_insiders': 0})

@insider_trading.route('/search', methods=['GET', 'POST'])
@demo_access
def search():
    """Simplified insider trading search"""
    symbol = request.args.get('symbol', '').strip().upper()
    
    # Handle POST requests from the search form
    if request.method == 'POST':
        form_data = request.form
        symbol = form_data.get('symbol', '').strip().upper()
        return redirect(url_for('insider_trading.search', symbol=symbol))
    
    if not symbol:
        flash('Vennligst oppgi et aksjensymbol for å søke.', 'warning')
        return redirect(url_for('insider_trading.index'))
    
    try:
        # Simplified - just return mock data for now
        flash(f'Viser innsidehandel data for {symbol}', 'info')
        
        # Mock data for demonstration
        insider_data = [{
            'date': '2025-07-20',
            'time': '12:45',
            'insider_name': 'John Doe',
            'title': 'CEO', 
            'transaction_type': 'Kjøp',
            'shares': 1000,
            'price': 100.0,
            'total_value': 100000,
            'shares_owned_after': 10000,
            'ownership_percent': 5.0,
            'form_type': 'Form 4'
        }, {
            'date': '2025-07-18',
            'time': '15:30',
            'insider_name': 'Jane Smith',
            'title': 'CFO', 
            'transaction_type': 'Salg',
            'shares': 500,
            'price': 95.0,
            'total_value': 47500,
            'shares_owned_after': 8500,
            'ownership_percent': 4.2,
            'form_type': 'Form 4'
        }]
        
        return render_template('insider_trading/index.html',
                             insider_data=insider_data,
                             popular_stocks=DataService.get_popular_stocks() or [],
                             selected_symbol=symbol,
                             insider_summary={'total_buys': 1, 'total_sells': 1, 'net_value': '52,500', 'unique_insiders': 2},
                             market_stats={'total_buys': 127, 'total_sells': 89, 'total_value': '1.2B'},
                             top_active_stocks=[
                                 {'symbol': 'EQNR', 'activity': '12'},
                                 {'symbol': 'TEL', 'activity': '8'},
                                 {'symbol': 'NOK', 'activity': '6'}
                             ],
                             hot_stocks_count=24,
                             signal_count=12,
                             alerts_count=7,
                             search_params={})
                             
    except Exception as e:
        logger.error(f"Error searching insider trading for {symbol}: {e}")
        flash('Teknisk feil. Viser demo data.', 'warning')
        
        return render_template('insider_trading/index.html',
                             insider_data=[],
                             popular_stocks=[],
                             selected_symbol=symbol,
                             insider_summary={'total_buys': 0, 'total_sells': 0, 'net_value': '0', 'unique_insiders': 0},
                             market_stats={'total_buys': 127, 'total_sells': 89, 'total_value': '1.2B'},
                             top_active_stocks=[],
                             hot_stocks_count=24,
                             signal_count=12,
                             alerts_count=7,
                             search_params={})

@insider_trading.route('/api/latest')
@demo_access
def api_latest():
    """API endpoint for latest insider trading data"""
    try:
        limit = request.args.get('limit', 50, type=int)
        insider_data = DataService.get_insider_trading_data() or []
        
        # Return latest transactions
        latest = insider_data[:limit]
        
        return jsonify({
            'success': True,
            'data': latest,
            'count': len(latest)
        })
        
    except Exception as e:
        logger.error(f"Error getting latest insider trading data: {e}")
        return jsonify({'error': 'Failed to get latest data'}), 500

@insider_trading.route('/api/export')
@demo_access
def api_export():
    """Export insider trading data"""
    try:
        return jsonify({'message': 'Export feature under development'})
            
    except Exception as e:
        logger.error(f"Error exporting insider trading data: {e}")
        return jsonify({'error': 'Export failed'}), 500

@insider_trading.route('/api/stats')
@demo_access
def api_stats():
    """Get insider trading statistics"""
    try:
        # Mock stats
        stats = {
            'total_transactions': 156,
            'total_buys': 89,
            'total_sells': 67,
            'unique_companies': 45,
            'unique_insiders': 234
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting insider trading stats: {e}")
        return jsonify({'error': 'Failed to get stats'}), 500

@insider_trading.route('/api/trending')
@demo_access
def api_trending():
    """Get trending insider trading activity"""
    try:
        # Mock trending data
        trending = [
            {
                'symbol': 'EQNR',
                'company_name': 'Equinor ASA',
                'activity_score': 95,
                'net_transactions': 12,
                'net_value': 5600000,
                'trend': 'up'
            },
            {
                'symbol': 'TEL',
                'company_name': 'Telenor ASA',
                'activity_score': 87,
                'net_transactions': 8,
                'net_value': 3200000,
                'trend': 'up'
            }
        ]
        
        return jsonify({
            'success': True,
            'trending': trending
        })
        
    except Exception as e:
        logger.error(f"Error getting trending insider trading: {e}")
        return jsonify({'error': 'Failed to get trending data'}), 500
