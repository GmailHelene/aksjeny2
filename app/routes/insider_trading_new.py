"""
Insider Trading Routes for Aksjeradar
Provides comprehensive insider trading data and analytics
"""

import logging
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import current_user, login_required

from ..services.data_service import DataService
from ..services.insider_trading_service import InsiderTradingService
from ..utils.access_control import access_required, demo_access

# Create blueprint
insider_trading = Blueprint('insider_trading', __name__)
logger = logging.getLogger(__name__)

# Initialize insider trading service
insider_service = InsiderTradingService()

@insider_trading.route('/')
@access_required
def index():
    """Enhanced insider trading main page with comprehensive data and analytics"""
    try:
        # Get recent insider trading data
        insider_data = DataService.get_insider_trading_data() or []
        
        # Get popular stocks for sidebar
        popular_stocks = DataService.get_popular_stocks() or []
        
        # Transform and enhance data for display
        enhanced_insider_data = []
        total_buys = total_sells = total_value = unique_insiders = 0
        insider_names = set()
        
        for transaction in insider_data[:50]:  # Limit to recent 50
            # Enhanced transaction data
            transaction_data = {
                'date': transaction.get('transaction_date', 'N/A'),
                'time': '12:45',  # Mock time, can be enhanced
                'symbol': transaction.get('symbol', 'UNKNOWN'),
                'company': transaction.get('company_name', 'Unknown Company'),
                'person': transaction.get('insider_name', 'Unknown'),
                'role': transaction.get('title', 'Officer'),
                'transaction_type': 'KJØP' if 'buy' in str(transaction.get('transaction_type', '')).lower() else 'SALG',
                'quantity': transaction.get('shares', 0),
                'price': transaction.get('price', 0),
                'total_value': transaction.get('value', 0)
            }
            
            enhanced_insider_data.append(transaction_data)
            
            # Calculate summary statistics
            if transaction_data['transaction_type'] == 'KJØP':
                total_buys += 1
            else:
                total_sells += 1
                
            total_value += float(transaction_data['total_value'] or 0)
            insider_names.add(transaction_data['person'])
        
        unique_insiders = len(insider_names)
        
        # Calculate summary stats
        insider_summary = {
            'total_buys': total_buys,
            'total_sells': total_sells,
            'net_value': f"{total_value:,.0f}",
            'unique_insiders': unique_insiders
        }
        
        # Market statistics for sidebar
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
                             insider_data=enhanced_insider_data,
                             popular_stocks=popular_stocks,
                             insider_summary=insider_summary,
                             market_stats=market_stats,
                             top_active_stocks=top_active_stocks,
                             hot_stocks_count=24,
                             signal_count=12,
                             alerts_count=7)
                             
    except Exception as e:
        logger.error(f"Error in insider trading index: {e}")
        flash('Kunne ikke laste innsidehandel data. Prøv igjen senere.', 'error')
        return render_template('insider_trading/index.html',
                             insider_data=[],
                             popular_stocks=[],
                             insider_summary={},
                             market_stats={},
                             top_active_stocks=[])

@insider_trading.route('/search', methods=['GET', 'POST'])
@access_required
def search():
    """Enhanced insider trading search with advanced filtering"""
    symbol = request.args.get('symbol', '').strip().upper()
    transaction_type = request.args.get('transaction_type', '')
    period = int(request.args.get('period', 30))
    min_value = request.args.get('min_value', type=float)
    role = request.args.get('role', '')
    sort = request.args.get('sort', 'date_desc')
    company_name = request.args.get('company_name', '')
    insider_name = request.args.get('insider_name', '')
    significant_only = request.args.get('significant_only') == '1'
    
    # Handle POST requests from the search form
    if request.method == 'POST':
        form_data = request.form
        symbol = form_data.get('symbol', '').strip().upper()
        return redirect(url_for('insider_trading.search', symbol=symbol))
    
    if not symbol:
        flash('Vennligst oppgi et aksjensymbol for å søke.', 'warning')
        return redirect(url_for('insider_trading.index'))
    
    try:
        # Get insider trading data for specific symbol using enhanced filtering
        insider_transactions = insider_service.get_insider_transactions(symbol) or []
        
        # Apply filters (implementation details)
        filtered_transactions = []
        for transaction in insider_transactions:
            # Date filter
            if period:
                try:
                    transaction_date = datetime.strptime(transaction.transaction_date, '%Y-%m-%d')
                except:
                    transaction_date = datetime.now()
                cutoff_date = datetime.now() - timedelta(days=period)
                if transaction_date < cutoff_date:
                    continue
            
            # Transaction type filter
            if transaction_type and transaction.transaction_type != transaction_type:
                continue
                
            # Minimum value filter
            if min_value and transaction.value < min_value:
                continue
                
            # Role filter
            if role and transaction.title != role:
                continue
                
            # Significant transactions only
            if significant_only and transaction.value < 1000000:  # 1M threshold
                continue
                
            filtered_transactions.append(transaction)
        
        # Get popular stocks for context
        popular_stocks = DataService.get_popular_stocks() or []
        
        # Transform and enhance transactions for display
        insider_data = []
        total_buys = total_sells = total_value = unique_insiders = 0
        insider_names = set()
        
        for transaction in filtered_transactions:
            transaction_data = {
                'date': transaction.transaction_date if hasattr(transaction, 'transaction_date') else 'N/A',
                'time': '12:45',  # Can be enhanced with actual time data
                'person': transaction.insider_name if hasattr(transaction, 'insider_name') else 'Ukjent',
                'role': transaction.title if hasattr(transaction, 'title') else 'Officer',
                'transaction_type': 'KJØP' if 'buy' in str(transaction.transaction_type).lower() or 'purchase' in str(transaction.transaction_type).lower() else 'SALG',
                'quantity': transaction.shares if hasattr(transaction, 'shares') else 0,
                'price': transaction.price if hasattr(transaction, 'price') else 0,
                'total_value': transaction.value if hasattr(transaction, 'value') else 0,
                'symbol': symbol
            }
            
            insider_data.append(transaction_data)
            
            # Calculate summary statistics
            if transaction_data['transaction_type'] == 'KJØP':
                total_buys += 1
            else:
                total_sells += 1
                
            total_value += float(transaction_data['total_value'] or 0)
            insider_names.add(transaction_data['person'])
        
        unique_insiders = len(insider_names)
        
        # Apply sorting
        if sort == 'date_desc':
            insider_data.sort(key=lambda x: x['date'], reverse=True)
        elif sort == 'date_asc':
            insider_data.sort(key=lambda x: x['date'])
        elif sort == 'value_desc':
            insider_data.sort(key=lambda x: float(x['total_value'] or 0), reverse=True)
        elif sort == 'value_asc':
            insider_data.sort(key=lambda x: float(x['total_value'] or 0))
        
        # Calculate summary stats
        insider_summary = {
            'total_buys': total_buys,
            'total_sells': total_sells,
            'net_value': f"{total_value:,.0f}",
            'unique_insiders': unique_insiders
        }
        
        # Market statistics for sidebar
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
        
        if not insider_data:
            flash(f'Ingen innsidehandel data funnet for {symbol} med de valgte filtrene.', 'info')
        
        return render_template('insider_trading/index.html',
                             insider_data=insider_data,
                             popular_stocks=popular_stocks,
                             selected_symbol=symbol,
                             insider_summary=insider_summary,
                             market_stats=market_stats,
                             top_active_stocks=top_active_stocks,
                             hot_stocks_count=24,
                             signal_count=12,
                             alerts_count=7,
                             search_params={
                                 'transaction_type': transaction_type,
                                 'period': period,
                                 'min_value': min_value,
                                 'role': role,
                                 'sort': sort,
                                 'company_name': company_name,
                                 'insider_name': insider_name,
                                 'significant_only': significant_only
                             })
                             
    except Exception as e:
        logger.error(f"Error searching insider trading for {symbol}: {e}")
        flash('Feil ved søk etter innsidehandel data.', 'error')
        return redirect(url_for('insider_trading.index'))

@insider_trading.route('/api/latest')
@access_required
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
@access_required
def api_export():
    """Export insider trading data"""
    try:
        symbol = request.args.get('symbol', '')
        format_type = request.args.get('format', 'csv')
        
        # Get data to export
        if symbol:
            data = insider_service.get_insider_transactions(symbol) or []
        else:
            data = DataService.get_insider_trading_data() or []
        
        if format_type == 'csv':
            # Return CSV format
            return jsonify({
                'success': True,
                'message': 'CSV export functionality would be implemented here',
                'data_count': len(data)
            })
        else:
            return jsonify({'error': 'Unsupported format'}), 400
            
    except Exception as e:
        logger.error(f"Error exporting insider trading data: {e}")
        return jsonify({'error': 'Export failed'}), 500

@insider_trading.route('/api/stats')
@access_required
def api_stats():
    """Get insider trading statistics"""
    try:
        # Get basic stats
        all_data = DataService.get_insider_trading_data() or []
        
        stats = {
            'total_transactions': len(all_data),
            'total_buys': len([t for t in all_data if 'buy' in str(t.get('transaction_type', '')).lower()]),
            'total_sells': len([t for t in all_data if 'sell' in str(t.get('transaction_type', '')).lower()]),
            'unique_companies': len(set(t.get('symbol', '') for t in all_data)),
            'unique_insiders': len(set(t.get('insider_name', '') for t in all_data))
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting insider trading stats: {e}")
        return jsonify({'error': 'Failed to get stats'}), 500

@insider_trading.route('/api/trending')
@access_required
def api_trending():
    """Get trending insider trading activity"""
    try:
        # Mock trending data - would be calculated from real data
        trending = [
            {
                'symbol': 'EQNR',
                'company_name': 'Equinor ASA',
                'activity_score': 95,
                'recent_transactions': 12,
                'net_sentiment': 'positive'
            },
            {
                'symbol': 'TEL',
                'company_name': 'Telenor ASA', 
                'activity_score': 87,
                'recent_transactions': 8,
                'net_sentiment': 'neutral'
            },
            {
                'symbol': 'DNB',
                'company_name': 'DNB Bank ASA',
                'activity_score': 73,
                'recent_transactions': 5,
                'net_sentiment': 'positive'
            }
        ]
        
        return jsonify({
            'success': True,
            'trending': trending
        })
        
    except Exception as e:
        logger.error(f"Error getting trending insider trading: {e}")
        return jsonify({'error': 'Failed to get trending data'}), 500
