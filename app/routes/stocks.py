import math
import pandas as pd
import random
import time
import traceback
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask import Response
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from ..services.data_service import DataService, YFINANCE_AVAILABLE
from ..services.analysis_service import AnalysisService
from ..services.usage_tracker import usage_tracker
from ..utils.access_control import access_required, demo_access, subscription_required
from ..models.favorites import Favorites
from ..services.notification_service import NotificationService
from ..utils.exchange_utils import get_exchange_url

import logging
logger = logging.getLogger(__name__)

# Define the stocks Blueprint
stocks = Blueprint('stocks', __name__)

@stocks.route('/')
@access_required
def index():
    """Main stocks overview page"""
    return list_index()


@stocks.route('/list/oslo', strict_slashes=False)
@demo_access
def list_oslo():
    """List Oslo Stock Exchange stocks - accessible in demo mode"""
    try:
        # Get Oslo stocks from data service with guaranteed fallback
        stocks_raw = DataService.get_oslo_bors_overview() or DataService._get_guaranteed_oslo_data() or []
        # Convert list to dict if needed
        if isinstance(stocks_raw, list):
            stocks = {s.get('symbol', s.get('ticker', f'OSLO_{i}')): s for i, s in enumerate(stocks_raw) if isinstance(s, dict)}
        elif isinstance(stocks_raw, dict):
            stocks = stocks_raw
        else:
            stocks = {}
        # Get top gainers/losers, most active, insider trades, AI recommendations
        top_gainers = DataService.get_top_gainers('oslo') or []
        top_losers = DataService.get_top_losers('oslo') or []
        most_active = DataService.get_most_active('oslo') or []
        insider_trades = DataService.get_insider_trades('oslo') or []
        ai_recommendations = DataService.get_ai_recommendations('oslo') or []
        
        # Get real market status
        market_status = DataService.get_market_status()
        oslo_status = market_status.get('oslo_bors', {}) if market_status else {}
        
        return render_template('stocks/oslo_dedicated.html',
                             stocks=stocks,
                             top_gainers=top_gainers,
                             top_losers=top_losers,
                             most_active=most_active,
                             insider_trades=insider_trades,
                             ai_recommendations=ai_recommendations,
                             market_status=oslo_status,
                             market='Oslo Børs',
                             market_type='oslo',
                             category='oslo')
    except Exception as e:
        current_app.logger.error(f"Error loading Oslo stocks: {e}")
        # Use guaranteed fallback data even on exception
        try:
            stocks = DataService._get_guaranteed_oslo_data() or {}
            # Get market status even in fallback
            market_status = DataService.get_market_status()
            oslo_status = market_status.get('oslo_bors', {}) if market_status else {}
            return render_template('stocks/oslo_dedicated.html',
                                 stocks=stocks,
                                 top_gainers=[],
                                 top_losers=[],
                                 most_active=[],
                                 insider_trades=[],
                                 ai_recommendations=[],
                                 market_status=oslo_status,
                                 market='Oslo Børs',
                                 market_type='oslo',
                                 category='oslo')
        except:
            flash('Kunne ikke laste aksjedata. Prøv igjen senere.', 'error')
            return render_template('stocks/oslo_dedicated.html',
                                 stocks={},
                                 market='Oslo Børs',
                                 market_type='oslo',
                                 category='oslo',
                                 market_status={'status': 'Ukjent'},
                                 error=True)

@stocks.route('/list/global')
@subscription_required
def global_list():
    """Global stocks"""
    try:
        # Get global stocks with guaranteed fallback
        stocks_raw = DataService.get_global_stocks_overview() or DataService._get_guaranteed_global_data() or []
        # Convert list to dict if needed
        if isinstance(stocks_raw, list):
            stocks_data = {s.get('symbol', s.get('ticker', f'GLOBAL_{i}')): s for i, s in enumerate(stocks_raw) if isinstance(s, dict)}
        elif isinstance(stocks_raw, dict):
            stocks_data = stocks_raw
        else:
            stocks_data = {}
        top_gainers = DataService.get_top_gainers('global') or []
        top_losers = DataService.get_top_losers('global') or []
        most_active = DataService.get_most_active('global') or []
        insider_trades = DataService.get_insider_trades('global') or []
        ai_recommendations = DataService.get_ai_recommendations('global') or []
        
        return render_template('stocks/global_dedicated.html',
                             stocks_data=stocks_data,
                             top_gainers=top_gainers,
                             top_losers=top_losers,
                             most_active=most_active,
                             insider_trades=insider_trades,
                             ai_recommendations=ai_recommendations,
                             market='Globale aksjer',
                             market_type='global',
                             category='global')
    except Exception as e:
        current_app.logger.error(f"Error loading global stocks: {e}")
        # Use guaranteed fallback data even on exception
        try:
            stocks_data = DataService._get_guaranteed_global_data() or {}
            return render_template('stocks/global_dedicated.html',
                                 stocks_data=stocks_data,
                                 top_gainers=[],
                                 top_losers=[],
                                 most_active=[],
                                 insider_trades=[],
                                 ai_recommendations=[],
                                 market='Globale aksjer',
                                 market_type='global',
                                 category='global')
        except:
            flash('Kunne ikke laste globale aksjer. Prøv igjen senere.', 'error')
            return render_template('stocks/global_dedicated.html',
                                 stocks_data={},
                                 market='Globale aksjer',
                                 market_type='global',
                                 category='global',
                                 error=True)

@stocks.route('/list/crypto')
@demo_access
def list_crypto():
    """Crypto currencies"""
    try:
        # Get crypto data with guaranteed fallback
        stocks_raw = DataService.get_crypto_overview() or DataService._get_guaranteed_crypto_data() or []
        # Convert list to dict if needed
        if isinstance(stocks_raw, list):
            stocks_data = {s.get('symbol', s.get('ticker', f'CRYPTO_{i}')): s for i, s in enumerate(stocks_raw) if isinstance(s, dict)}
        elif isinstance(stocks_raw, dict):
            stocks_data = stocks_raw
        else:
            stocks_data = {}
        return render_template('stocks/crypto.html',
                             stocks=stocks_data,
                             market='Kryptovaluta',
                             market_type='crypto',
                             category='crypto',
                             get_exchange_url=get_exchange_url,
                             error=False)
                             
    except Exception as e:
        current_app.logger.error(f"Critical error in crypto route: {e}")
        # Use guaranteed fallback data even on exception
        try:
            stocks_data = DataService._get_guaranteed_crypto_data() or {}
            return render_template('stocks/crypto.html',
                                 stocks=stocks_data,
                                 market='Kryptovaluta',
                                 market_type='crypto',
                                 category='crypto',
                                 get_exchange_url=get_exchange_url,
                                 error=False)
        except:
            return render_template('stocks/crypto.html',
                                 stocks={},
                                 market='Kryptovaluta',
                                 market_type='crypto',
                                 category='crypto',
                                 get_exchange_url=get_exchange_url,
                                 error=True)

@stocks.route('/list/index')
@access_required
def list_index():
    """Main stock listing index page"""
    try:
        # Get combined market overview data
        oslo_raw = DataService.get_oslo_bors_overview() or DataService._get_guaranteed_oslo_data() or []
        global_raw = DataService.get_global_stocks_overview() or DataService._get_guaranteed_global_data() or []
        crypto_raw = DataService.get_crypto_overview() or DataService._get_guaranteed_crypto_data() or []

        # Convert lists to dicts if needed
        def to_dict(raw, prefix):
            if isinstance(raw, list):
                return {s.get('symbol', s.get('ticker', f'{prefix}_{i}')): s for i, s in enumerate(raw) if isinstance(s, dict)}
            elif isinstance(raw, dict):
                return raw
            else:
                return {}
        oslo_stocks = to_dict(oslo_raw, 'OSLO')
        global_stocks = to_dict(global_raw, 'GLOBAL')
        crypto_data = to_dict(crypto_raw, 'CRYPTO')

        # Combine popular stocks from different markets
        popular_stocks = {}
        # Add top Oslo stocks
        oslo_count = 0
        for symbol, data in oslo_stocks.items():
            if oslo_count < 5:
                popular_stocks[symbol] = data
                oslo_count += 1
        # Add top global stocks
        global_count = 0
        for symbol, data in global_stocks.items():
            if global_count < 5:
                popular_stocks[symbol] = data
                global_count += 1
        return render_template('stocks/main_overview.html',
                             stocks=popular_stocks,
                             top_gainers=DataService.get_top_gainers('global') or [],
                             top_losers=DataService.get_top_losers('global') or [],
                             most_active=DataService.get_most_active('global') or [],
                             insider_trades=DataService.get_insider_trades('global') or [],
                             ai_recommendations=DataService.get_ai_recommendations('global') or [],
                             market='Populære aksjer',
                             market_type='index',
                             category='index')
    except Exception as e:
        current_app.logger.error(f"Error loading index page: {e}")
        # Return minimal fallback
        return render_template('stocks/main_overview.html',
                             stocks={},
                             top_gainers=[],
                             top_losers=[],
                             most_active=[],
                             insider_trades=[],
                             ai_recommendations=[],
                             market='Populære aksjer',
                             market_type='index',
                             category='index',
                             error=True)

@stocks.route('/list/currency')
@demo_access
def list_currency():
    """Currency rates - demo accessible"""
    try:
        title = "Valutakurser"
        template = 'stocks/currency.html'
        stocks_data = DataService.get_currency_overview()
        current_app.logger.info(f"[DEBUG] /list/currency stocks_data keys: {list(stocks_data.keys())}")
        # Guarantee fallback data is always returned
        if not stocks_data or len(stocks_data) == 0:
            current_app.logger.warning("[DEBUG] Fallback currency data is empty, using enhanced fallback.")
            stocks_data = DataService._get_enhanced_fallback_currency()
        error_flag = False if stocks_data and len(stocks_data) > 0 else True
        return render_template(template,
                      stocks=stocks_data,
                      market=title,
                      market_type='currency',
                      category='currency',
                      base_currency='NOK',
                      error=error_flag)
    except Exception as e:
        logger.error(f"Error in currency listing: {e}")
        stocks_data = DataService._get_enhanced_fallback_currency()
        return render_template('stocks/currency.html', 
                             stocks=stocks_data, 
                             category='currency', 
                             title="Valutakurser", 
                             base_currency='NOK',
                             error=True)

@stocks.route('/<symbol>')
@demo_access
def stock_symbol(symbol):
    """Direct stock access via symbol - redirects to details"""
    return redirect(url_for('stocks.details', symbol=symbol))

@stocks.route('/details/<symbol>')
@demo_access
def details(symbol):
    """Stock details page with complete analysis data"""
    try:
        current_app.logger.info(f"Accessing details route for symbol: {symbol}")
        
        # Get stock data from DataService with fallback
        stock_info = DataService.get_stock_info(symbol)
        
        # Generate base hash for consistent demo data
        base_hash = hash(symbol) % 1000
        
        if not stock_info:
            logger.warning(f"No stock_info for {symbol}, creating fallback data")
            # Create basic fallback data instead of redirecting
            stock_info = {
                'ticker': symbol,
                'name': symbol.replace('.OL', '').replace('.', ' ').title(),
                'last_price': 100.0,
                'change': 0.0,
                'change_percent': 0.0,
                'volume': 0,
                'high': 100.0,
                'low': 100.0,
                'open': 100.0
            }
        
        # Get current price    
        current_price = stock_info.get('last_price', stock_info.get('price', 100.0))
        
        # Create technical data with fallback
        try:
            from ..services.technical_analysis import calculate_comprehensive_technical_data
            historical_data = DataService.get_historical_data(symbol, period='3mo')
            if historical_data is not None and not getattr(historical_data, 'empty', True):
                technical_data = calculate_comprehensive_technical_data(historical_data)
            else:
                technical_data = {
                    'rsi': 30.0 + (base_hash % 40),
                    'macd': -2.0 + (base_hash % 40) / 10,
                    'macd_signal': -1.5 + (base_hash % 30) / 10,
                    'bollinger_upper': current_price * (1.05 + (base_hash % 5) / 100),
                    'bollinger_middle': current_price,
                    'bollinger_lower': current_price * (0.95 - (base_hash % 5) / 100),
                    'sma_20': current_price * (0.98 + (base_hash % 6) / 100),
                    'sma_50': current_price * (0.95 + (base_hash % 8) / 100),
                    'ema_12': current_price * (0.99 + (base_hash % 4) / 100),
                    'stochastic_k': 20.0 + (base_hash % 60),
                    'stochastic_d': 25.0 + (base_hash % 50),
                    'signal': stock_info.get('signal', 'HOLD'),
                    'signal_strength': 'Medium',
                    'signal_reason': 'Demo data - historical data unavailable'
                }
        except Exception as e:
            logger.warning(f"Technical data assignment failed for {symbol}: {e}")
            technical_data = {
                'rsi': 30.0 + (base_hash % 40),
                'macd': -2.0 + (base_hash % 40) / 10,
                'macd_signal': -1.5 + (base_hash % 30) / 10,
                'bollinger_upper': current_price * (1.05 + (base_hash % 5) / 100),
                'bollinger_middle': current_price,
                'bollinger_lower': current_price * (0.95 - (base_hash % 5) / 100),
                'sma_20': current_price * (0.98 + (base_hash % 6) / 100),
                'sma_50': current_price * (0.95 + (base_hash % 8) / 100),
                'ema_12': current_price * (0.99 + (base_hash % 4) / 100),
                'stochastic_k': 20.0 + (base_hash % 60),
                'stochastic_d': 25.0 + (base_hash % 50),
                'signal': stock_info.get('signal', 'HOLD'),
                'signal_strength': 'Medium',
                'signal_reason': 'Demo data - historical data unavailable'
            }

        # Create stock info for template
        currency = 'NOK' if symbol.endswith('.OL') else 'USD'
        template_stock_info = {
            'longName': stock_info.get('name', symbol),
            'shortName': stock_info.get('name', symbol)[:20],
            'symbol': symbol,
            'regularMarketPrice': current_price,
            'regularMarketChange': stock_info.get('change', 0),
            'regularMarketChangePercent': stock_info.get('change_percent', 0),
            'regularMarketVolume': stock_info.get('volume', 1000000),
            'currency': currency,
            'sector': stock_info.get('sector', 'Technology' if not symbol.endswith('.OL') else 'Industrials'),
            'dayHigh': current_price * 1.03,
            'dayLow': current_price * 0.97,
        }
        
        stock = {
            'symbol': symbol,
            'name': stock_info.get('name', symbol),
            'ticker': symbol,
            'current_price': current_price,
            'price': current_price,
            'change': stock_info.get('change', 0),
            'change_percent': stock_info.get('change_percent', 0),
            'volume': stock_info.get('volume', 1000000),
            'sector': stock_info.get('sector', 'Technology'),
        }

        # Return the stock details template with all data
        return render_template('stocks/details_enhanced.html',
                             symbol=symbol,
                             ticker=symbol,  # CRITICAL: Pass ticker variable for template compatibility
                             stock=stock,
                             stock_info=template_stock_info,
                             technical_data=technical_data,
                             news=[],
                             earnings=[],
                             competitors=[],
                             error=None)
        
    except Exception as e:
        current_app.logger.error(f"Error loading stock details for {symbol}: {e}")
        current_app.logger.error(f"Full traceback: {traceback.format_exc()}")
        # Return the details template with error rather than redirect
        return render_template('stocks/details_enhanced.html',
                             symbol=symbol,
                             ticker=symbol,  # CRITICAL: Pass ticker variable for template compatibility
                             stock={'symbol': symbol, 'name': symbol},
                             stock_info={'symbol': symbol, 'longName': symbol},
                             technical_data={},
                             news=[],
                             earnings=[],
                             competitors=[],
                             error=f"Could not load data for {symbol}")

@stocks.route('/search')
@demo_access  
def search():
    """Search stocks page"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return render_template('stocks/search.html', results=[], query='')
    
    try:
        # Get search results from DataService
        results = DataService.search_stocks(query)
        
        # Add demo data for symbols that might not have full data
        all_results = []
        for result in results[:10]:  # Limit to 10 results
            symbol = result.get('symbol', result.get('ticker', ''))
            if symbol:
                all_results.append({
                    'symbol': symbol,
                    'name': result.get('name', symbol),
                    'market': result.get('market', 'Unknown'),
                    'price': result.get('price', 'N/A'),
                    'change_percent': result.get('change_percent', 0),
                    'category': result.get('category', 'other')
                })

        # Limit results
        all_results = all_results[:20]
        
        return render_template('stocks/search.html', 
                             results=all_results, 
                             query=query)
        
    except Exception as e:
        current_app.logger.error(f"Error in stock search: {e}")
        return render_template('stocks/search.html', 
                             results=[], 
                             query=query,
                             error="Søket kunne ikke fullføres. Prøv igjen senere.")

@stocks.route('/api/search')
@access_required
def api_search():
    """API endpoint for stock search"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    try:
        results = DataService.search_stocks(query)
        return jsonify({
            'success': True,
            'results': results,
            'query': query
        })
    except Exception as e:
        current_app.logger.error(f"Error in API stock search: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred during search',
            'query': query
        }), 500

@stocks.route('/api/stocks/search')
@access_required
def api_stocks_search():
    """API endpoint for stock search - alternate URL"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    try:
        # Search in all available stocks
        results = []
        
        # Search Oslo Børs
        oslo_stocks = DataService.get_oslo_bors_overview() or {}
        for ticker, data in oslo_stocks.items():
            if query.upper() in ticker.upper() or (data.get('name', '') and query.upper() in data.get('name', '').upper()):
                results.append({
                    'symbol': ticker,
                    'name': data.get('name', ticker),
                    'market': 'Oslo Børs',
                    'price': data.get('last_price', 'N/A'),
                    'change_percent': data.get('change_percent', 0),
                    'category': 'oslo'
                })

        # Search Global stocks
        global_stocks = DataService.get_global_stocks_overview() or {}
        if isinstance(global_stocks, dict):
            for ticker, data in global_stocks.items():
                if query.upper() in ticker.upper() or (data.get('name', '') and query.upper() in data.get('name', '').upper()):
                    results.append({
                        'symbol': ticker,
                        'name': data.get('name', ticker),
                        'market': 'Global',
                        'price': data.get('last_price', 'N/A'),
                        'change_percent': data.get('change_percent', 0),
                        'category': 'global'
                    })
        
        # Search Crypto
        crypto_data = DataService.get_crypto_overview() or {}
        for ticker, data in crypto_data.items():
            if query.upper() in ticker.upper() or (data.get('name', '') and query.upper() in data.get('name', '').upper()):
                results.append({
                    'symbol': ticker,
                    'name': data.get('name', ticker),
                    'market': 'Crypto',
                    'price': data.get('last_price', 'N/A'),
                    'change_percent': data.get('change_percent', 0),
                    'category': 'crypto'
                })
        
        # Limit results
        results = results[:10]
        
        return jsonify({
            'success': True,
            'results': results,
            'query': query
        })
    except Exception as e:
        current_app.logger.error(f"Error in API stock search: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred during search',
            'query': query
        }), 500

@stocks.route('/api/favorites/add', methods=['POST'])
@demo_access
def add_to_favorites():
    """Add stock to favorites"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        name = data.get('name', '')
        exchange = data.get('exchange', '')
        
        if not symbol:
            return jsonify({'error': 'Symbol required'}), 400
            
        if not current_user.is_authenticated:
            # Demo users - show success message but don't actually save
            return jsonify({'success': True, 'message': f'{symbol} lagt til i favoritter (demo-modus)'})
            
        # Check if already in favorites
        if Favorites.is_favorite(current_user.id, symbol):
            return jsonify({'success': False, 'message': f'{symbol} er allerede i favoritter'})
        # Add to favorites
        favorite = Favorites.add_favorite(
            user_id=current_user.id,
            symbol=symbol,
            name=name,
            exchange=exchange
        )
        
        # Track achievement for adding favorites
        try:
            from ..models.achievements import UserStats, check_user_achievements
            user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
            if not user_stats:
                user_stats = UserStats(user_id=current_user.id)
                db.session.add(user_stats)
            user_stats.favorites_added += 1
            db.session.commit()
            
            # Check for new achievements
            check_user_achievements(current_user.id, 'favorites', user_stats.favorites_added)
        except Exception:
            pass  # Don't fail favorites if achievement tracking fails
        
        # Update favorite_count and create activity
        try:
            current_user.favorite_count = Favorites.query.filter_by(user_id=current_user.id).count()
            from ..models.activity import UserActivity
            UserActivity.create_activity(
                user_id=current_user.id,
                activity_type='favorite_add',
                description=f'La til {symbol} i favoritter',
                details=f'Navn: {name}, Exchange: {exchange}'
            )
            from ..extensions import db
            db.session.commit()
        except Exception as e:
            logger.error(f"Error updating favorite_count or activity: {e}")
        return jsonify({
            'success': True, 
            'message': f'{symbol} lagt til i favoritter',
            'favorite': True
        })
        
    except Exception as e:
        logger.error(f"Error adding to favorites: {e}")
        return jsonify({'error': 'Failed to add to favorites'}), 500

@stocks.route('/api/favorites/remove', methods=['POST'])
@demo_access
def remove_from_favorites():
    """Remove stock from favorites"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        if not symbol:
            return jsonify({'error': 'Symbol required'}), 400
            
        if not current_user.is_authenticated:
            # Demo users - show success message but don't actually save
            return jsonify({'success': True, 'message': f'{symbol} fjernet fra favoritter (demo-modus)'})
            
        # Check if in favorites
        if not Favorites.is_favorite(current_user.id, symbol):
            return jsonify({'success': False, 'message': f'{symbol} er ikke i favoritter'})
        # Remove from favorites
        removed = Favorites.remove_favorite(current_user.id, symbol)
        if removed:
            try:
                current_user.favorite_count = Favorites.query.filter_by(user_id=current_user.id).count()
                from ..models.activity import UserActivity
                UserActivity.create_activity(
                    user_id=current_user.id,
                    activity_type='favorite_remove',
                    description=f'Fjernet {symbol} fra favoritter',
                    details=f''
                )
                from ..extensions import db
                db.session.commit()
            except Exception as e:
                logger.error(f"Error updating favorite_count or activity: {e}")
            return jsonify({
                'success': True, 
                'message': f'{symbol} fjernet fra favoritter',
                'favorite': False
            })
        else:
            return jsonify({'error': 'Failed to remove from favorites'}), 500
    except Exception as e:
        logger.error(f"Error removing from favorites: {e}")
        return jsonify({'error': 'Failed to remove from favorites'}), 500

@stocks.route('/api/favorites/check/<symbol>', methods=['GET'])
@demo_access
def check_favorite(symbol):
    """Check if stock is in favorites"""
    try:
        if not current_user.is_authenticated:
            # Demo users - return false (no favorites in demo)
            return jsonify({'favorited': False})
        is_favorited = Favorites.is_favorite(current_user.id, symbol)
        return jsonify({'favorited': is_favorited})
    except Exception as e:
        logger.error(f"Error checking favorite status: {e}")
        return jsonify({'favorited': False})

@stocks.route('/api/favorites/toggle/<symbol>', methods=['POST'])
@demo_access
def toggle_favorite(symbol):
    """Toggle stock in/out of favorites"""
    try:
        if not current_user.is_authenticated:
            # Demo users - show success message but don't actually save
            return jsonify({'success': True, 'favorited': True, 'message': f'{symbol} lagt til i favoritter (demo-modus)'})
            
        # Check current status
        is_favorited = Favorites.is_favorite(current_user.id, symbol)
        
        if is_favorited:
            # Remove from favorites
            removed = Favorites.remove_favorite(current_user.id, symbol)
            if removed:
                try:
                    current_user.favorite_count = Favorites.query.filter_by(user_id=current_user.id).count()
                    from ..models.activity import UserActivity
                    UserActivity.create_activity(
                        user_id=current_user.id,
                        activity_type='favorite_remove',
                        description=f'Fjernet {symbol} fra favoritter'
                    )
                    from ..extensions import db
                    db.session.commit()
                except Exception as e:
                    logger.error(f"Error updating activity: {e}")
                
                return jsonify({
                    'success': True,
                    'favorited': False,
                    'message': f'{symbol} fjernet fra favoritter'
                })
            else:
                return jsonify({'error': 'Failed to remove from favorites'}), 500
        else:
            # Add to favorites
            # Get stock info for name
            stock_info = DataService.get_stock_info(symbol)
            name = stock_info.get('name', symbol) if stock_info else symbol
            exchange = 'Oslo Børs' if symbol.endswith('.OL') else 'Global'
            
            favorite = Favorites.add_favorite(
                user_id=current_user.id,
                symbol=symbol,
                name=name,
                exchange=exchange
            )
            
            try:
                current_user.favorite_count = Favorites.query.filter_by(user_id=current_user.id).count()
                from ..models.activity import UserActivity
                UserActivity.create_activity(
                    user_id=current_user.id,
                    activity_type='favorite_add',
                    description=f'La til {symbol} i favoritter',
                    details=f'Navn: {name}, Exchange: {exchange}'
                )
                from ..extensions import db
                db.session.commit()
            except Exception as e:
                logger.error(f"Error updating activity: {e}")
            
            return jsonify({
                'success': True,
                'favorited': True,
                'message': f'{symbol} lagt til i favoritter'
            })
            
    except Exception as e:
        logger.error(f"Error toggling favorite: {e}")
        return jsonify({'error': 'Failed to toggle favorite'}), 500

@stocks.route('/compare')
@demo_access
def compare():
    """Stock comparison page - Enhanced with better error handling"""

    try:
        # Initialize all required dicts first
        ticker_names = {}
        current_prices = {}
        price_changes = {}
        volatility = {}
        volumes = {}
        correlations = {}
        betas = {}
        rsi = {}
        macd = {}
        bb = {}
        sma200 = {}
        sma50 = {}
        signals = {}
        chart_data = {}

        # Support both 'symbols' and 'tickers' parameters for backward compatibility
        symbols_param = request.args.get('symbols') or request.args.get('tickers')
        symbols_list = request.args.getlist('symbols') or request.args.getlist('tickers')

        # Handle both comma-separated string and multiple parameters
        if symbols_param and ',' in symbols_param:
            symbols = [s.strip().upper() for s in symbols_param.split(',') if s.strip()]
        else:
            symbols = symbols_list

        period = request.args.get('period', '6mo')
        interval = request.args.get('interval', '1d')
        normalize = request.args.get('normalize', '1') == '1'

        # Remove empty strings and filter valid symbols
        symbols = [s.strip().upper() for s in symbols if s.strip()][:4]  # Max 4 stocks

        logger.info(f"Stock comparison requested for symbols: {symbols}")

        if not symbols:
            logger.info("No symbols provided, showing empty comparison form")
            return render_template('stocks/compare.html', 
                                 tickers=[], 
                                 stocks=[], 
                                 comparison_data={},
                                 current_prices={},
                                 price_changes={},
                                 volatility={},
                                 volumes={},
                                 correlations={},
                                 betas={},
                                 rsi={},
                                 macd={},
                                 bb={},
                                 sma200={},
                                 sma50={},
                                 signals={},
                                 ticker_names={},
                                 period=period,
                                 interval=interval,
                                 normalize=normalize,
                                 chart_data={})

        logger.debug(f"Fetching comparative data for symbols: {symbols}")
        try:
            historical_data = DataService.get_comparative_data(symbols, period=period, interval=interval)
            logger.debug(f"Received historical data: {historical_data}")
            logger.debug(f"Historical data type: {type(historical_data)}")
            logger.debug(f"Historical data keys: {list(historical_data.keys()) if isinstance(historical_data, dict) else 'Not a dict'}")
            logger.debug(f"Historical data truthiness: {bool(historical_data)}")
            if isinstance(historical_data, dict):
                for symbol, df in historical_data.items():
                    logger.debug(f"Symbol {symbol}: type={type(df)}, empty={df.empty if hasattr(df, 'empty') else 'No empty attr'}, len={len(df) if hasattr(df, '__len__') else 'No len'}")
        except Exception as e:
            logger.error(f"Error getting comparative data: {e}")
            historical_data = {}

        if not historical_data:
            logger.warning("No data available for the provided symbols. Generating demo data for all symbols.")
            # Generate demo data for all symbols when no historical data is available
            for symbol in symbols:
                info = DataService.get_stock_info(symbol)
                ticker_names[symbol] = info.get('name', symbol) if info else symbol
                
                # Generate demo chart data for visualization
                import random
                from datetime import datetime, timedelta
                
                logger.info(f"Generating demo chart data for {symbol}")
                
                # Create demo data for 6 months
                base_price = 100.0 + (abs(hash(symbol)) % 500)  # Price between 100-600
                demo_data = []
                current_date = datetime.now() - timedelta(days=180)
                price = base_price
                
                for i in range(180):  # 6 months of daily data
                    # Simulate price movement with some volatility
                    change_percent = random.uniform(-0.05, 0.05)  # -5% to +5% daily change
                    price = price * (1 + change_percent)
                    
                    # Ensure price doesn't go negative
                    if price < 10:
                        price = 10
                    
                    demo_data.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'open': round(price * 0.99, 2),
                        'high': round(price * 1.02, 2),
                        'low': round(price * 0.98, 2),
                        'close': round(price, 2),
                        'volume': random.randint(100000, 2000000)
                    })
                    current_date += timedelta(days=1)
                
                chart_data[symbol] = demo_data
                current_prices[symbol] = price
                price_changes[symbol] = ((price - base_price) / base_price) * 100
                volatility[symbol] = 15.0 + (abs(hash(symbol)) % 20)  # Demo volatility
                volumes[symbol] = 500000 + (abs(hash(symbol)) % 1000000)
                betas[symbol] = 0.8 + (abs(hash(symbol)) % 8) / 10
                rsi[symbol] = 30 + (abs(hash(symbol)) % 40)
                macd[symbol] = {'macd': random.uniform(-2, 2), 'signal': random.uniform(-1.5, 1.5)}
                bb[symbol] = {
                    'upper': price * 1.1, 
                    'lower': price * 0.9, 
                    'middle': price, 
                    'position': 'middle'
                }
                sma200[symbol] = random.uniform(-10, 10)
                sma50[symbol] = random.uniform(-5, 8)
                signals[symbol] = random.choice(['BUY', 'HOLD', 'SELL'])
            
            # Return with demo data instead of empty error
            return render_template('stocks/compare.html', 
                                 tickers=symbols,
                                 stocks=[],
                                 ticker_names=ticker_names,
                                 comparison_data={},
                                 current_prices=current_prices,
                                 price_changes=price_changes,
                                 volatility=volatility,
                                 volumes=volumes,
                                 correlations={},
                                 betas=betas,
                                 rsi=rsi,
                                 macd=macd,
                                 bb=bb,
                                 sma200=sma200,
                                 sma50=sma50,
                                 signals=signals,
                                 chart_data=chart_data,
                                 period=period,
                                 interval=interval,
                                 normalize=normalize)

        # Helper for correlation matrix
        price_matrix = {}

        # Process each symbol

        from datetime import datetime, timedelta
        import random
        for symbol in symbols:
            df = historical_data.get(symbol)
            info = DataService.get_stock_info(symbol)
            ticker_names[symbol] = info.get('name', symbol) if info else symbol

            if df is None or df.empty:
                # Generate demo chart data for visualization when real data unavailable
                import random
                from datetime import datetime, timedelta
                
                logger.info(f"Generating demo chart data for {symbol}")
                
                # Create demo data for 6 months
                base_price = 100.0 + (abs(hash(symbol)) % 500)  # Price between 100-600
                demo_data = []
                current_date = datetime.now() - timedelta(days=180)
                price = base_price
                
                for i in range(180):  # 6 months of daily data
                    # Simulate price movement with some volatility
                    change_percent = random.uniform(-0.05, 0.05)  # -5% to +5% daily change
                    price = price * (1 + change_percent)
                    
                    # Ensure price doesn't go negative
                    if price < 10:
                        price = 10
                    
                    demo_data.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'open': round(price * 0.99, 2),
                        'high': round(price * 1.02, 2),
                        'low': round(price * 0.98, 2),
                        'close': round(price, 2),
                        'volume': random.randint(100000, 2000000)
                    })
                    current_date += timedelta(days=1)
                
                chart_data[symbol] = demo_data
                current_prices[symbol] = price
                price_changes[symbol] = ((price - base_price) / base_price) * 100
                volatility[symbol] = 15.0 + (abs(hash(symbol)) % 20)  # Demo volatility
                volumes[symbol] = 500000 + (abs(hash(symbol)) % 1000000)
                betas[symbol] = 0.8 + (abs(hash(symbol)) % 8) / 10
                rsi[symbol] = 30 + (abs(hash(symbol)) % 40)
                macd[symbol] = {'macd': random.uniform(-2, 2), 'signal': random.uniform(-1.5, 1.5)}
                bb[symbol] = {
                    'upper': price * 1.1, 
                    'lower': price * 0.9, 
                    'middle': price, 
                    'position': 'middle'
                }
                sma200[symbol] = random.uniform(-10, 10)
                sma50[symbol] = random.uniform(-5, 8)
                signals[symbol] = random.choice(['BUY', 'HOLD', 'SELL'])
                continue

            # Existing logic for real data
            # Ensure index is datetime
            if not hasattr(df.index, 'dtype') or 'datetime' not in str(df.index.dtype):
                try:
                    df.index = pd.to_datetime(df.index)
                except Exception:
                    pass

            chart_data[symbol] = []
            for idx, row in df.iterrows():
                chart_data[symbol].append({
                    'date': idx.strftime('%Y-%m-%d'),
                    'open': float(row.get('Open', 0)),
                    'high': float(row.get('High', 0)),
                    'low': float(row.get('Low', 0)),
                    'close': float(row.get('Close', 0)),
                    'volume': int(row.get('Volume', 0))
                })

            current_prices[symbol] = float(df['Close'].iloc[-1]) if 'Close' in df else 0
            try:
                start_price = float(df['Close'].iloc[0])
                end_price = float(df['Close'].iloc[-1])
                price_changes[symbol] = ((end_price - start_price) / start_price) * 100 if start_price else 0
            except Exception:
                price_changes[symbol] = 0
            try:
                returns = df['Close'].pct_change().dropna()
                volatility[symbol] = returns.std() * (252 ** 0.5) * 100 if not returns.empty else 0
            except Exception:
                volatility[symbol] = 0
            try:
                volumes[symbol] = df['Volume'].mean() if 'Volume' in df else 0
            except Exception:
                volumes[symbol] = 0
            price_matrix[symbol] = df['Close'] if 'Close' in df else pd.Series()
            try:
                if symbol != symbols[0] and symbols[0] in price_matrix:
                    returns1 = price_matrix[symbol].pct_change().dropna()
                    returns0 = price_matrix[symbols[0]].pct_change().dropna()
                    cov = returns1.cov(returns0)
                    var = returns0.var()
                    betas[symbol] = cov / var if var else 1.0
                else:
                    betas[symbol] = 1.0
            except Exception:
                betas[symbol] = 1.0
            try:
                close = df['Close']
                delta = close.diff()
                up = delta.clip(lower=0)
                down = -1 * delta.clip(upper=0)
                roll_up = up.rolling(14).mean()
                roll_down = down.rolling(14).mean()
                rs = roll_up / roll_down
                rsi[symbol] = 100 - (100 / (1 + rs.iloc[-1])) if rs.iloc[-1] else 50
            except Exception:
                rsi[symbol] = 50
            try:
                exp12 = df['Close'].ewm(span=12, adjust=False).mean()
                exp26 = df['Close'].ewm(span=26, adjust=False).mean()
                macd_val = exp12.iloc[-1] - exp26.iloc[-1]
                signal_val = df['Close'].ewm(span=9, adjust=False).mean().iloc[-1]
                macd[symbol] = {'macd': macd_val, 'signal': signal_val}
            except Exception:
                macd[symbol] = {'macd': 0, 'signal': 0}
            try:
                sma = df['Close'].rolling(window=20).mean()
                std = df['Close'].rolling(window=20).std()
                upper = sma.iloc[-1] + 2 * std.iloc[-1]
                lower = sma.iloc[-1] - 2 * std.iloc[-1]
                price = df['Close'].iloc[-1]
                position = 'middle'
                if price >= upper:
                    position = 'upper'
                elif price <= lower:
                    position = 'lower'
                bb[symbol] = {'upper': upper, 'lower': lower, 'middle': sma.iloc[-1], 'position': position}
            except Exception:
                bb[symbol] = {'upper': 0, 'lower': 0, 'middle': 0, 'position': 'middle'}
            try:
                sma200[symbol] = ((df['Close'].iloc[-1] - df['Close'].rolling(window=200).mean().iloc[-1]) / df['Close'].rolling(window=200).mean().iloc[-1]) * 100 if len(df) >= 200 else 0
            except Exception:
                sma200[symbol] = 0
            try:
                sma50[symbol] = ((df['Close'].iloc[-1] - df['Close'].rolling(window=50).mean().iloc[-1]) / df['Close'].rolling(window=50).mean().iloc[-1]) * 100 if len(df) >= 50 else 0
            except Exception:
                sma50[symbol] = 0
            try:
                if rsi[symbol] > 70:
                    signals[symbol] = 'SELL'
                elif rsi[symbol] < 30:
                    signals[symbol] = 'BUY'
                else:
                    signals[symbol] = 'HOLD'
            except Exception:
                signals[symbol] = 'HOLD'

        # Correlation matrix
        for symbol in symbols:
            correlations[symbol] = {}
            for other in symbols:
                try:
                    corr = price_matrix[symbol].corr(price_matrix[other]) if symbol in price_matrix and other in price_matrix else 1.0
                    correlations[symbol][other] = corr if corr is not None else 1.0
                except Exception:
                    correlations[symbol][other] = 1.0

        logger.info(f"Processed {len(symbols)} symbols successfully")
        logger.debug(f"Chart data keys: {list(chart_data.keys())}")
        logger.debug(f"Chart data lengths: {[(k, len(v)) for k, v in chart_data.items()]}")
        logger.debug(f"Current prices: {current_prices}")

        # Ensure all required template variables are present and valid
        template_data = {
            'tickers': symbols,
            'stocks': [],
            'ticker_names': ticker_names,
            'comparison_data': {},
            'current_prices': current_prices,
            'price_changes': price_changes,
            'volatility': volatility,
            'volumes': volumes,
            'correlations': correlations,
            'betas': betas,
            'rsi': rsi,
            'macd': macd,
            'bb': bb,
            'sma200': sma200,
            'sma50': sma50,
            'signals': signals,
            'chart_data': chart_data,
            'period': period,
            'interval': interval,
            'normalize': normalize
        }
        
        logger.info(f"Rendering template with data for {len(symbols)} symbols")
        return render_template('stocks/compare.html', **template_data)

    except Exception as e:
        logger.error(f"Critical error in stock comparison: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        # Create safe empty template data
        empty_data = {
            'tickers': [], 
            'stocks': [], 
            'ticker_names': {},
            'comparison_data': {},
            'current_prices': {},
            'price_changes': {},
            'volatility': {},
            'volumes': {},
            'correlations': {},
            'betas': {},
            'rsi': {},
            'macd': {},
            'bb': {},
            'sma200': {},
            'sma50': {},
            'signals': {},
            'chart_data': {},
            'period': '6mo',
            'interval': '1d',
            'normalize': True,
            'error_message': 'Det oppstod en teknisk feil ved sammenligning av aksjer.'
        }
        
        try:
            flash('Det oppstod en teknisk feil ved sammenligning av aksjer.', 'error')
        except:
            pass  # Flash might not be available in all contexts
            
        return render_template('stocks/compare.html', **empty_data)

@stocks.route('/prices')
@demo_access
def prices():
    """Stock prices overview"""
    try:
        oslo_stocks = DataService.get_oslo_bors_overview()
        global_stocks = DataService.get_global_stocks_overview()
        crypto_data = DataService.get_crypto_overview()
        currency_data = DataService.get_currency_overview()
        
        # Calculate statistics safely
        oslo_len = len(oslo_stocks) if oslo_stocks else 0
        global_len = len(global_stocks) if global_stocks else 0
        crypto_len = len(crypto_data) if crypto_data else 0
        currency_len = len(currency_data) if currency_data else 0
        
        stats = {
            'total_stocks': oslo_len + global_len,
            'total_crypto': crypto_len,
            'total_currency': currency_len,
            'total_instruments': oslo_len + global_len + crypto_len + currency_len
        }
        
        return render_template('stocks/prices.html',
                             market_data={
                                 'oslo_stocks': oslo_stocks or {},
                                 'global_stocks': global_stocks or {},
                                 'crypto': crypto_data or {},
                                 'currency': currency_data or {}
                             },
                             stats=stats,
                             error=False)
                             
    except Exception as e:
        logger.error(f"Error in prices overview: {e}")
        import traceback
        traceback.print_exc()
        flash('Kunne ikke laste prisdata.', 'error')
        return render_template('stocks/prices.html',
                             market_data={
                                 'oslo_stocks': {},
                                 'global_stocks': {},
                                 'crypto': {},
                                 'currency': {}
                             },
                             stats={'total_stocks': 0, 'total_crypto': 0, 'total_currency': 0, 'total_instruments': 0},
                             error=True)


@stocks.route('/api/chart-data/<symbol>')
@access_required
def api_chart_data(symbol):
    """API endpoint for stock chart data"""
    try:
        # Get historical data
        period = request.args.get('period', '30d')  # Default 30 days
        interval = request.args.get('interval', '1d')  # Default daily
        
        # Get data from DataService
        df = DataService.get_stock_data(symbol, period=period, interval=interval)
        
        if df is None or (hasattr(df, 'empty') and df.empty):
            # Ingen data tilgjengelig – ikke bruk mock chart-data
            chart_data = {
                'dates': [],
                'prices': [],
                'volumes': [],
                'currency': 'NOK' if 'OSL:' in symbol else 'USD'
            }
        else:
            # Convert DataFrame to chart format
            df = df.reset_index()
            dates = []
            prices = []
            volumes = []
            
            for index, row in df.iterrows():
                # Handle different date column names
                if 'Date' in row:
                    date_val = row['Date']
                elif 'Datetime' in row:
                    date_val = row['Datetime'] 
                else:
                    # Use index if no date column
                    date_val = row.name if hasattr(row, 'name') else index
                
                # Format date
                if hasattr(date_val, 'strftime'):
                    dates.append(date_val.strftime('%Y-%m-%d'))
                else:
                    dates.append(str(date_val))
                
                # Get price (prefer Close, then Open)
                price = row.get('Close', row.get('Open', 100))
                prices.append(float(price) if price else 100.0)
                
                # Get volume
                volume = row.get('Volume', 100000)
                volumes.append(int(volume) if volume else 100000)
            
            chart_data = {
                'dates': dates,
                'prices': prices,
                'volumes': volumes,
                'currency': 'USD' if not 'OSL:' in symbol else 'NOK'
            }
        
        return jsonify(chart_data)
        
    except Exception as e:
        logger.error(f"Error getting chart data for {symbol}: {e}")
        return jsonify({'error': 'Kunne ikke laste chart data'}), 500


@stocks.route('/api/technical-data/<symbol>')
@access_required
def api_technical_data(symbol):
    """API endpoint for technical analysis data - Optimized for performance"""
    try:
        # Hent teknisk data fra DataService
        technical_data = DataService.get_technical_data(symbol)
        if not technical_data:
            return jsonify({
                'success': False,
                'error': 'Kunne ikke laste teknisk data',
                'symbol': symbol.upper(),
                'message': 'Teknisk analyse er midlertidig utilgjengelig'
            }), 404
        return jsonify(technical_data)
    except Exception as e:
        logger.error(f"Error getting technical data for {symbol}: {e}")
        return jsonify({
            'success': False,
            'error': 'Kunne ikke laste teknisk data',
            'symbol': symbol.upper(),
            'message': 'Teknisk analyse er midlertidig utilgjengelig'
        }), 500

