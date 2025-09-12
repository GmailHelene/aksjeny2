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
        
        # Market statistics from real data
        market_stats = {
            'total_buys': len([trade for trade in insider_data if trade.get('transaction_type') == 'Buy']),
            'total_sells': len([trade for trade in insider_data if trade.get('transaction_type') == 'Sell']),
            'total_value': f"{sum(trade.get('value', 0) for trade in insider_data if trade.get('value', 0) > 0):,.0f} NOK" if insider_data else '0 NOK'
        }
        
        # Calculate top active stocks from real data
        if insider_data:
            stock_activity = {}
            for trade in insider_data:
                symbol = trade.get('symbol', 'N/A')
                if symbol in stock_activity:
                    stock_activity[symbol] += 1
                else:
                    stock_activity[symbol] = 1
            
            top_active_stocks = [
                {'symbol': symbol, 'activity': str(count)}
                for symbol, count in sorted(stock_activity.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
        else:
            # Fallback when no data available
            top_active_stocks = [
                {'symbol': 'Venter på data', 'activity': 'N/A'},
                {'symbol': 'Venter på data', 'activity': 'N/A'},
                {'symbol': 'Venter på data', 'activity': 'N/A'},
                {'symbol': 'Venter på data', 'activity': 'N/A'},
                {'symbol': 'Venter på data', 'activity': 'N/A'}
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
    """Simplified insider trading search with robust undefined/empty symbol safeguards.

    Treats 'undefined', 'null', placeholder dashes and pure whitespace as empty.
    """
    from ..utils.param_utils import normalize_symbol
    raw_symbol = (request.args.get('symbol') or request.form.get('symbol') or '').strip()
    # Normalize and sanitize special unwanted tokens
    lowered = raw_symbol.lower()
    if lowered in {'undefined', 'null', 'none', '-', '--'}:
        raw_symbol = ''
    symbol = normalize_symbol(raw_symbol) or ''

    # Handle POST requests (form submission)
    if request.method == 'POST':
        if not symbol:
            flash('Vennligst oppgi et aksjesymbol.', 'warning')
            return redirect(url_for('insider_trading.index'))
        return redirect(url_for('insider_trading.search', symbol=symbol))
    
    if not symbol:
        flash('Vennligst oppgi et aksjesymbol for å søke.', 'warning')
        return redirect(url_for('insider_trading.index'))
    
    try:
        # Extract additional optional filters
        transaction_type = request.args.get('transaction_type', '').strip().lower()  # 'buy'/'sell'
        period = request.args.get('period', '30').strip()  # days back
        min_value = request.args.get('min_value', '').strip()
        role = request.args.get('role', '').strip().lower()
        insider_name = request.args.get('insider_name', '').strip().lower()
        sort_param = request.args.get('sort', 'date_desc').strip().lower()

        # Sanitize numeric inputs
        try:
            days_back = int(period)
            if days_back <= 0 or days_back > 365:
                days_back = 30
        except ValueError:
            days_back = 30
        try:
            min_value_num = int(min_value) if min_value else 0
        except ValueError:
            min_value_num = 0

        # Get insider trading data for the specified symbol
        insider_data = DataService.get_insider_trading_data(symbol)
        
        if not insider_data:
            flash(f'Ingen innsidehandel data funnet for {symbol}', 'warning')
            return redirect(url_for('insider_trading.index'))
        original_count = len(insider_data)

        # Apply time period filter (assuming trade has 'date' key)
        if days_back:
            cutoff = datetime.utcnow() - timedelta(days=days_back)
            filtered = []
            for trade in insider_data:
                dt = trade.get('date') or trade.get('transaction_date')
                dt_obj = None
                if isinstance(dt, datetime):
                    dt_obj = dt
                elif isinstance(dt, str):
                    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%Y-%m-%dT%H:%M:%S'):
                        try:
                            dt_obj = datetime.strptime(dt[:19], fmt)
                            break
                        except Exception:
                            continue
                if not dt_obj or dt_obj >= cutoff:
                    filtered.append(trade)
            insider_data = filtered

        # Filter by transaction type
        if transaction_type in {'buy','purchase','kjøp'}:
            insider_data = [t for t in insider_data if t.get('transaction_type','').lower() in {'buy','purchase'}]
        elif transaction_type in {'sell','sale','salg'}:
            insider_data = [t for t in insider_data if t.get('transaction_type','').lower() in {'sell','sale'}]

        # Filter by minimum value
        if min_value_num > 0:
            insider_data = [t for t in insider_data if (t.get('value') or t.get('total_value') or 0) >= min_value_num]

        # Filter by insider role/position
        if role:
            insider_data = [t for t in insider_data if role in (t.get('position') or t.get('role') or '').lower()]

        # Filter by insider name
        if insider_name:
            insider_data = [t for t in insider_data if insider_name in (t.get('insider') or t.get('insider_name') or '').lower()]

        # Sorting
        if sort_param == 'value_desc':
            insider_data.sort(key=lambda t: t.get('value') or t.get('total_value') or 0, reverse=True)
        elif sort_param == 'value_asc':
            insider_data.sort(key=lambda t: t.get('value') or t.get('total_value') or 0)
        elif sort_param == 'date_asc':
            def _date_key(t):
                dt = t.get('date') or t.get('transaction_date')
                if isinstance(dt, datetime):
                    return dt
                if isinstance(dt, str):
                    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%Y-%m-%dT%H:%M:%S'):
                        try:
                            return datetime.strptime(dt[:19], fmt)
                        except Exception:
                            continue
                return datetime.utcnow()
            insider_data.sort(key=_date_key)
        else:  # default date_desc
            def _date_key_desc(t):
                dt = t.get('date') or t.get('transaction_date')
                if isinstance(dt, datetime):
                    return dt
                if isinstance(dt, str):
                    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%Y-%m-%dT%H:%M:%S'):
                        try:
                            return datetime.strptime(dt[:19], fmt)
                        except Exception:
                            continue
                return datetime.utcnow()
            insider_data.sort(key=_date_key_desc, reverse=True)
            
        # Calculate summary data
        buy_trades = [t for t in insider_data if t.get('transaction_type') == 'Purchase']
        sell_trades = [t for t in insider_data if t.get('transaction_type') == 'Sale']
        total_buys = len(buy_trades)
        total_sells = len(sell_trades)
        
        # Calculate net value
        buy_value = sum(t.get('value', 0) for t in buy_trades)
        sell_value = sum(t.get('value', 0) for t in sell_trades)
        net_value = buy_value - sell_value
        
        # Calculate unique insiders
        unique_insiders = len(set(t.get('insider') for t in insider_data))
        
        # Format net value
        if abs(net_value) >= 1000000:
            net_value_formatted = f"{net_value/1000000:.1f}M"
        else:
            net_value_formatted = f"{net_value/1000:.1f}K"
        
        # Add sign to the net value
        if net_value > 0:
            net_value_formatted = "+" + net_value_formatted
        
        # Get popular stocks for sidebar
        popular_stocks = DataService.get_popular_stocks() or []
        
        # General market statistics
        market_stats = {
            'total_buys': 127, 
            'total_sells': 89, 
            'total_value': '1.2B'
        }
        
        # Top active stocks
        top_active_stocks = [
            {'symbol': 'EQNR.OL', 'activity': '12'},
            {'symbol': 'DNB.OL', 'activity': '8'},
            {'symbol': 'TEL.OL', 'activity': '6'},
            {'symbol': 'NHY.OL', 'activity': '5'},
            {'symbol': 'MOWI.OL', 'activity': '4'}
        ]
        
        return render_template('insider_trading/index.html',
                             insider_data=insider_data,
                             popular_stocks=popular_stocks,
                             selected_symbol=symbol,
                             insider_summary={
                                 'total_buys': total_buys, 
                                 'total_sells': total_sells, 
                                 'net_value': net_value_formatted, 
                                 'unique_insiders': unique_insiders
                             },
                             market_stats=market_stats,
                             top_active_stocks=top_active_stocks,
                             hot_stocks_count=24,
                             signal_count=12,
                             alerts_count=7,
                             search_params={
                                 'symbol': symbol,
                                 'transaction_type': transaction_type,
                                 'period': days_back,
                                 'min_value': min_value_num,
                                 'role': role,
                                 'insider_name': insider_name,
                                 'sort': sort_param,
                                 'original_count': original_count,
                                 'filtered_count': len(insider_data)
                             })
                             
                             
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
        symbol = request.args.get('symbol', '').strip().upper()
        
        # Get insider trading data for the specified symbol or general data
        insider_data = DataService.get_insider_trading_data(symbol) or []
        
        # Return latest transactions
        latest = insider_data[:limit]
        
        return jsonify({
            'success': True,
            'data': latest,
            'count': len(latest),
            'symbol': symbol if symbol else None
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
