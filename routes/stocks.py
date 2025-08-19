from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from services import data_service
from ..models import Favorite, db

stocks_bp = Blueprint('stocks', __name__)

@stocks_bp.route('/list/<market>')
@login_required
def list_stocks(market):
    try:
        current_app.logger.info(f"Loading {market} stocks")
        
        stocks_data = None
        
        if market == 'oslo':
            stocks_data = data_service.get_oslo_stocks()
        elif market == 'global':
            stocks_data = data_service.get_global_stocks()
        elif market == 'currency':
            stocks_data = data_service.get_currency_pairs()
        elif market == 'crypto':
            stocks_data = data_service.get_crypto_overview()
        else:
            flash('Ugyldig marked', 'error')
            return redirect(url_for('stocks.overview'))
        
        # Validate and filter stocks_data
        if stocks_data:
            filtered_stocks = {}
            for symbol, stock in stocks_data.items():
                # Make sure we have a valid stock object, not a string
                if hasattr(stock, 'change_percent') and hasattr(stock, 'current_price'):
                    filtered_stocks[symbol] = stock
                else:
                    current_app.logger.warning(f"Invalid stock data for {symbol}: {type(stock)}")
            stocks_data = filtered_stocks
        
        current_app.logger.info(f"Loaded {len(stocks_data) if stocks_data else 0} valid items for {market}")
        
        return render_template(f'stocks/{market}.html', 
                             stocks_data=stocks_data,
                             market=market)
                             
    except Exception as e:
        current_app.logger.error(f"Critical error in {market} route: {str(e)}")
        # Use fallback data
        if market == 'oslo':
            stocks_data = data_service._generate_fallback_oslo_stocks()
        elif market == 'global':
            stocks_data = data_service._generate_fallback_global_stocks()
        elif market == 'crypto':
            stocks_data = data_service._generate_fallback_crypto()
        elif market == 'currency':
            stocks_data = data_service._generate_fallback_currencies()
        else:
            stocks_data = {}
            
        return render_template(f'stocks/{market}.html', 
                             stocks_data=stocks_data,
                             market=market)

@stocks_bp.route('/details/<symbol>')
@login_required
def stock_details(symbol):
    try:
        current_app.logger.info(f"Loading details for {symbol}")
        
        # Get stock data with better error handling
        stock_data = data_service.get_stock_data(symbol)
        
        if not stock_data:
            # Create minimal fallback data
            from ..services.data_models import Stock
            stock_data = Stock(
                symbol=symbol,
                name=symbol,
                current_price=100.0,
                change_percent=0.0,
                previous_close=100.0,
                market_cap=1000000000,
                volume=1000000,
                sector='Unknown'
            )
        
        # Get historical data
        historical_data = data_service.get_historical_data(symbol, period='1mo')
        
        # Prepare chart data
        chart_data = []
        if historical_data is not None and not historical_data.empty:
            for date, row in historical_data.iterrows():
                chart_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'close': float(row.get('Close', 0))
                })
        
        # Get ticker-specific insider trading data
        insider_trades = data_service.get_insider_trades(symbol)
        
        return render_template('stocks/details.html',
                             stock=stock_data,
                             symbol=symbol,
                             chart_data=chart_data,
                             insider_trades=insider_trades)
                             
    except Exception as e:
        current_app.logger.error(f"Error loading details for {symbol}: {str(e)}")
        flash(f'Kunne ikke laste detaljer for {symbol}', 'error')
        return redirect(url_for('stocks.overview'))

@stocks_bp.route('/compare')
@login_required
def compare():
    symbols = request.args.getlist('symbols')
    
    if not symbols or len(symbols) < 2:
        flash('Velg minst to aksjer for sammenligning', 'info')
        return redirect(url_for('stocks.overview'))
    
    try:
        comparison_data = {}
        dates = None
        
        for symbol in symbols[:4]:  # Max 4 stocks
            stock = data_service.get_stock_data(symbol)
            if stock:
                historical = data_service.get_historical_data(symbol, period='3mo')
                
                if historical is not None and not historical.empty:
                    # Normalize prices to percentage change from first day
                    prices = historical['Close'].values
                    if len(prices) > 0:
                        normalized_prices = ((prices / prices[0]) - 1) * 100
                        
                        comparison_data[symbol] = {
                            'name': stock.name,
                            'current_price': stock.current_price,
                            'change_percent': stock.change_percent,
                            'prices': normalized_prices.tolist()
                        }
                        
                        if dates is None:
                            dates = [d.strftime('%Y-%m-%d') for d in historical.index]
        
        return render_template('stocks/compare.html',
                             comparison_data=comparison_data,
                             dates=dates or [],
                             symbols=symbols)
                             
    except Exception as e:
        current_app.logger.error(f"Error in stock comparison: {str(e)}")
        flash('Feil ved sammenligning av aksjer', 'error')
        return redirect(url_for('stocks.overview'))

@stocks_bp.route('/api/favorites/toggle/<symbol>', methods=['POST'])
@login_required
def toggle_favorite(symbol):
    try:
        favorite = Favorite.query.filter_by(
            user_id=current_user.id,
            symbol=symbol
        ).first()
        
        if favorite:
            db.session.delete(favorite)
            favorited = False
        else:
            favorite = Favorite(
                user_id=current_user.id,
                symbol=symbol
            )
            db.session.add(favorite)
            favorited = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'favorited': favorited
        })
    except Exception as e:
        current_app.logger.error(f"Error toggling favorite: {str(e)}")
        return jsonify({'success': False}), 500

@stocks_bp.route('/api/favorites/check/<symbol>')
@login_required
def check_favorite(symbol):
    try:
        favorite = Favorite.query.filter_by(
            user_id=current_user.id,
            symbol=symbol
        ).first()
        
        return jsonify({
            'favorited': favorite is not None
        })
    except Exception as e:
        current_app.logger.error(f"Error checking favorite: {str(e)}")
        return jsonify({'favorited': False}), 500