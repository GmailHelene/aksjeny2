from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, Response
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from io import BytesIO
import logging
import json
import os

from ..models import Portfolio, PortfolioStock, StockTip, Watchlist, WatchlistStock
from ..extensions import db
from ..utils.access_control import access_required, demo_access
from ..utils.error_handler import (
    handle_api_error, format_number_norwegian, format_currency_norwegian,
    format_percentage_norwegian, safe_api_call, validate_stock_symbol,
    validate_quantity, UserFriendlyError
)
from ..services.portfolio_optimization_service import PortfolioOptimizationService
from ..services.performance_tracking_service import PerformanceTrackingService

logger = logging.getLogger(__name__)

# Lazy import for DataService to avoid circular import
def get_data_service():
    """Lazy import DataService to avoid circular imports"""
    from ..services.data_service import DataService
    return DataService

# Lazy import for AnalysisService to avoid circular import
def get_analysis_service():
    """Lazy import AnalysisService to avoid circular imports"""
    try:
        from ..services.analysis_service import AnalysisService
        return AnalysisService
    except ImportError:
        return None

# Lazy import for reportlab to handle optional dependency
def get_reportlab():
    """Lazy import reportlab components for PDF generation"""
    try:
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        return {
            'SimpleDocTemplate': SimpleDocTemplate,
            'Table': Table, 
            'TableStyle': TableStyle,
            'A4': A4,
            'colors': colors
        }
    except ImportError:
        return None

portfolio = Blueprint('portfolio', __name__, url_prefix='/portfolio')
# Delete portfolio route
@portfolio.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_portfolio(id):
    """Delete a portfolio and all associated stocks"""
    try:
        portfolio_obj = Portfolio.query.filter_by(id=id, user_id=current_user.id).first()
        if not portfolio_obj:
            flash('Portefølje ikke funnet eller du har ikke tilgang.', 'danger')
            return redirect(url_for('portfolio.overview'))

        # Delete all stocks in the portfolio
        try:
            PortfolioStock.query.filter_by(portfolio_id=id).delete()
        except Exception as stock_delete_error:
            current_app.logger.error(f"Error deleting stocks for portfolio {id}: {stock_delete_error}")

        # Delete the portfolio itself
        db.session.delete(portfolio_obj)
        db.session.commit()
        flash('Porteføljen ble slettet.', 'success')
        return redirect(url_for('portfolio.overview'))
    except Exception as e:
        current_app.logger.error(f"Error deleting portfolio {id}: {e}")
        db.session.rollback()
        flash('Kunne ikke slette porteføljen. Prøv igjen senere.', 'danger')
        return redirect(url_for('portfolio.overview'))

@portfolio.route('/overview')
@login_required
def overview():
    """Portfolio overview page with enhanced error handling"""
    error = None
    try:
        # Get user portfolios with error handling
        try:
            user_portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
        except Exception as db_error:
            current_app.logger.error(f"Database error in portfolio overview: {str(db_error)}")
            user_portfolios = []
            error = 'Kunne ikke laste porteføljedata fra databasen.'
        
        # Initialize totals
        total_value = 0
        total_gain_loss = 0
        portfolio_data = []
        
        # Try to get data service with fallback
        try:
            data_service = get_data_service()()
        except Exception as data_service_error:
            current_app.logger.warning(f"Data service unavailable: {str(data_service_error)}")
            data_service = None
            error = 'Datatjenesten er utilgjengelig. Prøv igjen senere.'
        
        # Initialize sector distribution and performance data
        sector_distribution = {}
        performance_data = []

        # Process each portfolio

        for portfolio_obj in user_portfolios:
            try:
                portfolio_value = 0
                portfolio_gain_loss = 0
                stock_data = []

                # Process stocks in portfolio
                for stock in portfolio_obj.stocks:
                    try:
                        current_price = stock.purchase_price  # Default fallback
                        stock_data_service = None
                        if data_service:
                            stock_data_service = data_service.get_single_stock_data(stock.ticker)
                            if stock_data_service:
                                current_price = float(stock_data_service['last_price'])

                        current_value = current_price * stock.quantity
                        purchase_value = stock.purchase_price * stock.quantity
                        profit_loss = current_value - purchase_value

                        portfolio_value += current_value
                        portfolio_gain_loss += profit_loss
                        
                        # KRITISK FIX: Akkumuler totaler for alle porteføljer
                        total_value += current_value
                        total_gain_loss += profit_loss

                        sector = stock_data_service.get('sector', 'Annet') if stock_data_service else 'Annet'
                        if sector not in sector_distribution:
                            sector_distribution[sector] = 0
                        sector_distribution[sector] += current_value

                        performance_data.append({
                            'ticker': stock.ticker,
                            'current_value': current_value,
                            'profit_loss': profit_loss
                        })

                        stock_data.append({
                            'ticker': stock.ticker,
                            'shares': stock.quantity,
                            'value': current_value
                        })

                    except Exception as stock_error:
                        current_app.logger.warning(f"Error processing stock {stock.ticker}: {str(stock_error)}")

                portfolio_data.append({
                    'portfolio': portfolio_obj,
                    'value': portfolio_value,
                    'gain_loss': portfolio_gain_loss,
                    'stocks': stock_data
                })

            except Exception as portfolio_error:
                error = f'Feil ved behandling av portefølje {portfolio_obj.name}: {str(portfolio_error)}'

        # Hvis ingen porteføljer funnet, vis tomt og feilmelding
        if not user_portfolios or not portfolio_data:
            error = error or 'Ingen porteføljer funnet.'
            portfolio_data = []
            total_value = 0
            total_gain_loss = 0
            sector_distribution = {}
            performance_data = []

        if total_value > 0:
            total_gain_loss_percent = (total_gain_loss / total_value) * 100
        else:
            total_gain_loss_percent = 0
        return render_template('portfolio/overview.html',
            portfolios=portfolio_data,
            total_value=total_value,
            total_gain_loss=total_gain_loss,
            total_gain_loss_percent=total_gain_loss_percent,
            sector_distribution=sector_distribution,
            performance_data=performance_data,
            error=bool(error),
            message=error if error else None)
    except Exception as e:
        current_app.logger.error(f"Critical error in portfolio overview: {str(e)}")
        flash('Det oppstod en teknisk feil ved lasting av porteføljer. Vennligst prøv igjen senere.', 'error')
        return render_template('portfolio/overview.html',
                             portfolios=[],
                             total_value=0,
                             total_gain_loss=0,
                             total_gain_loss_percent=0,
                             error=True,
                             message='Kunne ikke laste porteføljedata.')

@portfolio.route('/watchlist')
@login_required
def watchlist():
    """User's watchlist"""
    try:
        # Import models with fallback handling
        try:
            from ..models.watchlist import Watchlist, WatchlistItem
        except ImportError:
            # Fallback if watchlist model is not available
            current_app.logger.warning("Watchlist model not available")
            return render_template('portfolio/watchlist.html', watchlist=[], error=True)
        
        # Get user's watchlist items - check both old and new models
        watchlist_items = []
        try:
            # Try new watchlist structure first
            watchlists = Watchlist.query.filter_by(user_id=current_user.id).all()
            for wl in watchlists:
                watchlist_items.extend(wl.items)
        except Exception:
            # Try alternative approach - direct items
            try:
                watchlist_items = WatchlistItem.query.join(Watchlist).filter(
                    Watchlist.user_id == current_user.id
                ).all()
            except Exception as e:
                current_app.logger.warning(f"No watchlist items found: {e}")
                watchlist_items = []
        
        # Also get favorites and add them to watchlist_items
        try:
            from ..models.favorites import Favorites
            favorites = Favorites.get_user_favorites(current_user.id)
            # Convert favorites to watchlist item format
            for fav in favorites:
                # Create a mock watchlist item object for favorites
                class MockWatchlistItem:
                    def __init__(self, symbol, name=None):
                        self.symbol = symbol
                        self.ticker = symbol
                        self.name = name or symbol
                        
                watchlist_items.append(MockWatchlistItem(fav.symbol, fav.name))
        except Exception as e:
            current_app.logger.warning(f"Could not get favorites: {e}")
        
        # Get current prices for watchlist items
        watchlist_data = []
        for item in watchlist_items:
            try:
                symbol = getattr(item, 'symbol', getattr(item, 'ticker', 'UNKNOWN'))
                stock_data = get_data_service().get_stock_info(symbol)
                
                # KRITISK FIX: Sikre at alle verdier er numeriske
                current_price = float(stock_data.get('regularMarketPrice', 0)) if stock_data.get('regularMarketPrice') is not None else 0.0
                change = float(stock_data.get('regularMarketChange', 0)) if stock_data.get('regularMarketChange') is not None else 0.0
                change_percent = float(stock_data.get('regularMarketChangePercent', 0)) if stock_data.get('regularMarketChangePercent') is not None else 0.0
                
                watchlist_data.append({
                    'item': item,
                    'ticker': symbol,
                    'current_price': current_price,
                    'change': change,
                    'change_percent': change_percent,
                    'name': stock_data.get('shortName', symbol) if stock_data else symbol
                })
            except Exception as e:
                current_app.logger.warning(f"Could not get data for watchlist item {symbol}: {e}")
                # KRITISK FIX: Alltid bruk numeriske fallback-verdier
                watchlist_data.append({
                    'item': item,
                    'ticker': symbol,
                    'current_price': 0.0,
                    'change': 0.0,
                    'change_percent': 0.0,
                    'name': symbol
                })
        
        # If no watchlist data, create sample data for demo
        if not watchlist_data:
            sample_stocks = [
                {'ticker': 'EQNR.OL', 'name': 'Equinor', 'last_price': 280.50, 'change_percent': 2.1},
                {'ticker': 'DNB.OL', 'name': 'DNB Bank', 'last_price': 220.30, 'change_percent': -0.8},
                {'ticker': 'AAPL', 'name': 'Apple Inc.', 'last_price': 175.40, 'change_percent': 1.2}
            ]
            return render_template('portfolio/watchlist.html', stocks=sample_stocks, watchlist=[], demo_mode=True)
        
        return render_template('portfolio/watchlist.html', watchlist=watchlist_data, stocks=watchlist_data)
    except Exception as e:
        current_app.logger.error(f"Error in watchlist: {str(e)}")
        # Provide fallback data instead of error
        sample_stocks = [
            {'ticker': 'EQNR.OL', 'name': 'Equinor', 'last_price': 280.50, 'change_percent': 2.1},
            {'ticker': 'DNB.OL', 'name': 'DNB Bank', 'last_price': 220.30, 'change_percent': -0.8}
        ]
        return render_template('portfolio/watchlist.html', stocks=sample_stocks, error_message="Watchlist midlertidig utilgjengelig")

@portfolio.route('/')
@login_required
def index():
    """Portfolio main page with better error handling"""
    try:
        # Get user's portfolios with proper error handling
        portfolios = []
        if current_user and current_user.is_authenticated:
            try:
                # Safely get portfolios with database connection check
                from ..models.portfolio import Portfolio
                portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
            except Exception as db_error:
                logger.error(f"Database error getting portfolios for user {current_user.id}: {db_error}")
                portfolios = []
        
        # Calculate total portfolio value safely
        total_value = 0
        total_profit_loss = 0  # KRITISK FIX: Legg til manglende total_profit_loss
        portfolio_data = []
        
        for p in portfolios:
            try:
                portfolio_value = p.calculate_total_value() if hasattr(p, 'calculate_total_value') else 0
                total_value += portfolio_value
                portfolio_data.append({
                    'id': p.id,
                    'name': p.name,
                    'value': portfolio_value,
                    'created_at': p.created_at
                })
            except Exception as calc_error:
                logger.error(f"Error calculating portfolio value for {p.name}: {calc_error}")
                portfolio_data.append({
                    'id': p.id,
                    'name': p.name,
                    'value': 0,
                    'created_at': p.created_at
                })
        
        # Initialize data service for stock prices
        try:
            data_service = get_data_service()
        except Exception as data_service_error:
            logger.warning(f"Data service unavailable: {str(data_service_error)}")
            data_service = None

        # Process each portfolio
        for p in portfolios:
            try:
                portfolio_value = 0
                portfolio_gain_loss = 0
                stock_data = []

                # Process stocks in portfolio
                for stock in p.stocks:
                    try:
                        # Get current price with fallback to purchase price
                        current_price = stock.purchase_price  # Default to purchase price
                        if data_service:
                            try:
                                current_data = data_service.get_stock_info(stock.ticker)
                                if current_data and 'regularMarketPrice' in current_data:
                                    current_price = current_data.get('regularMarketPrice', stock.purchase_price)
                                elif current_data and 'last_price' in current_data:
                                    current_price = current_data.get('last_price', stock.purchase_price)
                            except Exception as price_error:
                                logger.warning(f"Price fetch error for {stock.ticker}: {str(price_error)}")
                                current_price = stock.purchase_price

                        # Calculate gain/loss
                        gain_loss = (current_price - stock.purchase_price) * stock.quantity
                        portfolio_gain_loss += gain_loss

                        stock_data.append({
                            'ticker': stock.ticker,
                            'quantity': stock.quantity,
                            'purchase_price': stock.purchase_price,
                            'current_price': current_price,
                            'gain_loss': gain_loss
                        })

                        portfolio_value += current_price * stock.quantity
                    except Exception as stock_error:
                        logger.error(f"Error processing stock {stock.ticker}: {stock_error}")

                total_value += portfolio_value
                total_profit_loss += portfolio_gain_loss  # KRITISK FIX: Akkumuler total profit/loss
                portfolio_data.append({
                    'id': p.id,
                    'name': p.name,
                    'value': portfolio_value,
                    'gain_loss': portfolio_gain_loss,
                    'stocks': stock_data,
                    'created_at': p.created_at
                })
            except Exception as calc_error:
                logger.error(f"Error calculating portfolio data for {p.name}: {calc_error}")
                portfolio_data.append({
                    'id': p.id,
                    'name': p.name,
                    'value': 0,
                    'gain_loss': 0,
                    'stocks': [],
                    'created_at': p.created_at
                })
        
        return render_template('portfolio/index.html',
                             portfolios=portfolio_data,
                             total_value=total_value,
                             total_profit_loss=total_profit_loss)  # KRITISK FIX: Send total_profit_loss til template
                             
    except Exception as e:
        logger.error(f"Error in portfolio index: {e}")
        flash('Det oppstod en feil ved lasting av porteføljer.', 'error')
        return render_template('portfolio/index.html',
                             portfolios=[],
                             total_value=0,
                             error="Det oppstod en feil ved lasting av porteføljer.")

@portfolio.route('/tips', methods=['GET', 'POST'])
@access_required
def stock_tips():
    """Stock tips page with enhanced error handling"""
    try:
        if request.method == 'POST':
            try:
                ticker = request.form.get('ticker', '').strip().upper()
                tip_type = request.form.get('tip_type', '').strip()
                confidence = request.form.get('confidence', '').strip()
                analysis = request.form.get('analysis', '').strip()

                # Validate inputs
                if not all([ticker, tip_type, confidence, analysis]):
                    flash('Alle felt må fylles ut.', 'warning')
                    return redirect(url_for('portfolio.stock_tips'))

                # Validate ticker format
                if not ticker or len(ticker) < 2:
                    flash('Ugyldig ticker-symbol.', 'warning')
                    return redirect(url_for('portfolio.stock_tips'))

                # Create new tip
                tip = StockTip(
                    ticker=ticker,
                    tip_type=tip_type,
                    confidence=confidence,
                    analysis=analysis,
                    user_id=current_user.id
                )
                
                db.session.add(tip)
                db.session.commit()
                flash('Aksjetips er lagt til!', 'success')
                return redirect(url_for('portfolio.stock_tips'))
                
            except Exception as post_error:
                current_app.logger.error(f"Error creating stock tip: {post_error}")
                db.session.rollback()
                flash('Feil ved lagring av tips. Prøv igjen.', 'error')
        
        # GET request - load tips
        try:
            tips = StockTip.query.order_by(StockTip.created_at.desc()).limit(10).all()
        except Exception as db_error:
            current_app.logger.error(f"Database error loading tips: {db_error}")
            tips = []
            flash('Kunne ikke laste aksjetips fra databasen.', 'warning')
        
        return render_template('portfolio/tips.html', tips=tips)
        
    except Exception as e:
        current_app.logger.error(f"Critical error in stock_tips route: {e}")
        flash('Siden kunne ikke lastes. Prøv igjen senere.', 'error')
        return render_template('portfolio/tips.html', tips=[], error="Feil ved lasting av siden")


@portfolio.route('/tips/feedback/<int:tip_id>', methods=['POST'])
@access_required
def stock_tips_feedback(tip_id):
    """Handle feedback on stock tips"""
    try:
        # Get the tip
        tip = StockTip.query.get_or_404(tip_id)
        
        # Get feedback data
        rating = request.form.get('rating')
        comment = request.form.get('comment', '').strip()
        
        if rating:
            # Here you could save the feedback to a separate table if needed
            # For now, just flash a success message
            flash('Takk for tilbakemeldingen!', 'success')
        else:
            flash('Vennligst gi en vurdering.', 'warning')
            
    except Exception as e:
        logger.error(f"Error processing tip feedback: {e}")
        flash('Kunne ikke lagre tilbakemelding.', 'error')
    
    return redirect(url_for('portfolio.stock_tips'))


@portfolio.route('/create', methods=['GET', 'POST'])
@login_required
@access_required
def create_portfolio():
    """Create a new portfolio with robust error handling"""
    try:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            initial_value = request.form.get('initial_value', '0')
            currency = request.form.get('currency', 'NOK')
            
            if not name:
                flash('Du må gi porteføljen et navn.', 'danger')
                return render_template('portfolio/create.html')
            
            # Opprett og lagre portefølje
            try:
                # Ensure we have the Portfolio model
                if Portfolio is None:
                    flash('Portfolio-funksjonen er ikke tilgjengelig for øyeblikket.', 'warning')
                    return render_template('portfolio/create.html', error="Portfolio-tjeneste ikke tilgjengelig")
                    
                new_portfolio = Portfolio(
                    name=name, 
                    description=description, 
                    user_id=current_user.id
                )
                db.session.add(new_portfolio)
                db.session.commit()
                flash(f'Porteføljen "{name}" ble opprettet!', 'success')
                return redirect(url_for('portfolio.view_portfolio', id=new_portfolio.id))
                
            except Exception as db_error:
                logger.error(f"Database error creating portfolio: {db_error}")
                db.session.rollback()
                flash('Kunne ikke opprette portefølje i databasen. Prøv igjen.', 'error')
                return render_template('portfolio/create.html', error=str(db_error))
                
        # GET request - show form
        return render_template('portfolio/create.html')
        
    except Exception as e:
        logger.error(f"Critical error in create_portfolio: {e}")
        flash('En teknisk feil oppstod. Prøv igjen senere.', 'error')
        return render_template('portfolio/create.html', error=f"Teknisk feil: {str(e)}")

@portfolio.route('/view/<int:id>')
@login_required
def view_portfolio(id):
    """View a specific portfolio - primary function"""
    try:
        portfolio_obj = Portfolio.query.filter_by(id=id, user_id=current_user.id).first()
        if not portfolio_obj:
            flash('Portefølje ikke funnet', 'error')
            return redirect(url_for('portfolio.index'))
        
        # Get portfolio stocks
        portfolio_stocks = PortfolioStock.query.filter_by(portfolio_id=id).all()
        
        # Calculate portfolio metrics
        total_value = 0
        total_cost = 0
        portfolio_data = []
        
        # Lazy import DataService to avoid circular imports
        DataService = get_data_service()
        for stock in portfolio_stocks:
            try:
                # Get current stock data
                current_data = DataService.get_stock_data(stock.ticker)
                if current_data:
                    current_price = current_data.get('last_price', stock.purchase_price)
                    current_value = current_price * stock.quantity
                    cost_value = stock.purchase_price * stock.quantity
                    gain_loss = current_value - cost_value
                    gain_loss_percent = (gain_loss / cost_value * 100) if cost_value > 0 else 0
                    
                    portfolio_data.append({
                        'stock': stock,
                        'current_price': current_price,
                        'current_value': current_value,
                        'cost_value': cost_value,
                        'gain_loss': gain_loss,
                        'gain_loss_percent': gain_loss_percent
                    })
                    
                    total_value += current_value
                    total_cost += cost_value
                    
            except Exception as e:
                current_app.logger.error(f"Error getting data for {stock.ticker}: {e}")
                # Use stored values as fallback
                cost_value = stock.purchase_price * stock.quantity
                portfolio_data.append({
                    'stock': stock,
                    'current_price': stock.purchase_price,
                    'current_value': cost_value,
                    'cost_value': cost_value,
                    'gain_loss': 0,
                    'gain_loss_percent': 0
                })
                total_value += cost_value
                total_cost += cost_value
        
        # Calculate total metrics
        total_gain_loss = total_value - total_cost
        total_gain_loss_percent = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0
        
        return render_template('portfolio/view.html',
                             portfolio=portfolio_obj,
                             portfolio_data=portfolio_data,
                             total_value=total_value,
                             total_cost=total_cost,
                             total_gain_loss=total_gain_loss,
                             total_gain_loss_percent=total_gain_loss_percent)
                             
    except Exception as e:
        current_app.logger.error(f"Error viewing portfolio {id}: {e}")
        flash('Feil ved lasting av portefølje', 'error')
        return redirect(url_for('portfolio.index'))

@portfolio.route('/portfolio/<int:id>/add', methods=['GET', 'POST'])
@demo_access
def add_stock_to_portfolio(id):
    """Add a stock to a specific portfolio"""
    # For demo users, provide a simulated experience
    if not current_user.is_authenticated:
        if request.method == 'POST':
            return jsonify({
                'success': True,
                'message': 'Demo: Stock addition simulated'
            })
        # Return a demo template or redirect
        return render_template('portfolio/add_stock_demo.html', portfolio_id=id)
    
    portfolio = Portfolio.query.get_or_404(id)

    # Sjekk eierskap
    if portfolio.user_id != current_user.id:
        flash('Du har ikke tilgang til denne porteføljen', 'danger')
        return redirect(url_for('portfolio.index'))

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if not ticker or not quantity or not price:
            flash('Alle felt er påkrevd', 'danger')
            return redirect(url_for('portfolio.add_stock_to_portfolio', id=id))

        try: 
            quantity = float(quantity)
            price = float(price)
        except ValueError:
            flash('Antall og pris må være tall', 'danger')
            return redirect(url_for('portfolio.add_stock_to_portfolio', id=id))

        existing_stock = PortfolioStock.query.filter_by(portfolio_id=id, ticker=ticker).first()

        if existing_stock:
            total_value = (existing_stock.shares * existing_stock.purchase_price) + (quantity * price)
            total_quantity = existing_stock.shares + quantity
            existing_stock.purchase_price = total_value / total_quantity if total_quantity > 0 else 0
            existing_stock.shares = total_quantity
        else:
            stock = PortfolioStock(
                portfolio_id=id,
                ticker=ticker,
                shares=quantity,
                purchase_price=price
            )
            db.session.add(stock)
 
        db.session.commit()
        flash('Aksje lagt til i porteføljen', 'success')
        return redirect(url_for('portfolio.view_portfolio', id=id))

    return render_template('portfolio/add_stock_to_portfolio.html', portfolio=portfolio)

@portfolio.route('/portfolio/<int:id>/remove/<int:stock_id>', methods=['POST'])
@access_required
def remove_stock_from_portfolio(id, stock_id):
    """Remove a stock from a specific portfolio"""
    portfolio = Portfolio.query.get_or_404(id)

    # Sjekk eierskap
    if portfolio.user_id != current_user.id:
        flash('Du har ikke tilgang til denne porteføljen', 'danger')
        return redirect(url_for('portfolio.index'))

    stock = PortfolioStock.query.get_or_404(stock_id)

    if stock.portfolio_id != id:
        flash('Aksjen tilhører ikke denne porteføljen', 'danger')
        return redirect(url_for('portfolio.view_portfolio', id=id))

    db.session.delete(stock)
    db.session.commit()

    flash('Aksje fjernet fra porteføljen', 'success')
    return redirect(url_for('portfolio.view_portfolio', id=id))

@portfolio.route('/watchlist/create', methods=['GET', 'POST'])
@access_required
def create_watchlist():
    """Create a new watchlist"""
    if request.method == 'POST':
        name = request.form.get('name')
        user_id = current_user.id
        watchlist = Watchlist(name=name, user_id=user_id)
        db.session.add(watchlist)
        db.session.commit()
        flash('Favorittliste opprettet!', 'success')
        return redirect(url_for('portfolio.watchlist'))
    return render_template('portfolio/create_watchlist.html')

@portfolio.route('/watchlist/<int:id>/add', methods=['GET', 'POST'])
@access_required
def add_to_watchlist(id):
    """Add a stock to a watchlist"""
    watchlist = Watchlist.query.get_or_404(id)

    # Sjekk eierskap
    if watchlist.user_id != current_user.id:
        flash('Du har ikke tilgang til denne favorittlisten', 'danger')
        return redirect(url_for('portfolio.watchlist'))

    if request.method == 'POST':
        ticker = request.form.get('ticker')

        if not ticker:
            flash('Ticker er påkrevd', 'danger')
            return redirect(url_for('portfolio.add_to_watchlist', id=id))

        existing = WatchlistStock.query.filter_by(watchlist_id=id, ticker=ticker).first()

        if existing:
            flash('Aksjen er allerede i favorittlisten', 'warning')
        else:
            stock = WatchlistStock(watchlist_id=id, ticker=ticker)
            db.session.add(stock)
            db.session.commit()
            flash('Aksje lagt til i favorittlisten', 'success')

        return redirect(url_for('portfolio.watchlist'))

    return render_template('portfolio/add_to_watchlist.html', watchlist=watchlist)

@portfolio.route('/tips/add', methods=['GET', 'POST'])
@access_required
def add_tip():
    """Add a stock tip"""
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        tip_type = request.form.get('tip_type')
        confidence = request.form.get('confidence')
        analysis = request.form.get('analysis')
        tip = StockTip(
            ticker=ticker,
            tip_type=tip_type,
            confidence=confidence,
            analysis=analysis,
            user_id=current_user.id
        )
        db.session.add(tip)
        db.session.commit()
        flash('Aksjetips lagt til', 'success')
        return redirect(url_for('portfolio.stock_tips'))
    ticker = request.args.get('ticker', '')
    return render_template('portfolio/add_tip.html', ticker=ticker)

@portfolio.route('/tips/feedback/<int:tip_id>', methods=['POST'])
@access_required
def tip_feedback(tip_id):
    """Submit feedback for a stock tip"""
    tip = StockTip.query.get_or_404(tip_id)
    feedback = request.form.get('feedback')
    tip.feedback = feedback
    db.session.commit()
    flash('Tilbakemelding lagret!', 'success')
    return redirect(url_for('portfolio.stock_tips'))

@portfolio.route('/add/<ticker>')
@access_required
def quick_add_stock(ticker):
    """Quickly add a stock to the user's portfolio"""
    # Check if user is authenticated
    if not current_user.is_authenticated:
        flash("Du må logge inn for å legge til aksjer i porteføljen.", "warning")
        return redirect(url_for('main.login'))
    
    stock_info = get_data_service().get_stock_info(ticker)
    if not stock_info:
        flash(f"Aksje {ticker} ble ikke funnet.", "danger")
        return redirect(url_for('main.index'))

    # Finn eller opprett brukerens første portefølje
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    if not portfolio:
        portfolio = Portfolio(name="Min portefølje", user_id=current_user.id)
        db.session.add(portfolio)
        db.session.commit()

    # Sjekk om aksjen allerede finnes i porteføljen
    existing_stock = PortfolioStock.query.filter_by(portfolio_id=portfolio.id, ticker=ticker).first()
    if existing_stock:
        # Øk antall aksjer med 1
        existing_stock.shares += 1
    else:
        # Legg til ny aksje med 1 aksje og dagens pris som snittpris
        avg_price = stock_info.get('last_price') or stock_info.get('regularMarketPrice') or 100.0
        stock = PortfolioStock(
            portfolio_id=portfolio.id,
            ticker=ticker,
            shares=1,
            purchase_price=avg_price
        )
        db.session.add(stock)

    db.session.commit()
    flash(f"Aksje {ticker} lagt til i din portefølje!", "success")
    return redirect(url_for('portfolio.index'))

@portfolio.route('/add', methods=['GET', 'POST'])
@access_required
def add_stock():
    """Add a stock to the user's default portfolio"""
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        quantity = float(request.form.get('quantity', 0))
        purchase_price = float(request.form.get('purchase_price', 0))
        
        if not ticker or quantity <= 0 or purchase_price <= 0:
            flash('Alle felt må fylles ut korrekt.', 'danger')
            return redirect(url_for('portfolio.add_stock'))
        
        # Hent brukerens portefølje
        user_portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
        if not user_portfolio:
            user_portfolio = Portfolio(name="Min portefølje", user_id=current_user.id)
            db.session.add(user_portfolio)
            db.session.commit()
        
        # Sjekk om aksjen allerede finnes i porteføljen
        existing_stock = PortfolioStock.query.filter_by(portfolio_id=user_portfolio.id, ticker=ticker).first()
        if existing_stock:
            # Beregn ny gjennomsnittspris
            total_value = (existing_stock.shares * existing_stock.purchase_price) + (quantity * purchase_price)
            total_quantity = existing_stock.shares + quantity
            existing_stock.purchase_price = total_value / total_quantity
            existing_stock.shares = total_quantity
        else:
            # Legg til ny aksje
            portfolio_stock = PortfolioStock(
                portfolio_id=user_portfolio.id,
                ticker=ticker,
                shares=quantity,
                purchase_price=purchase_price
            )
            db.session.add(portfolio_stock)
        
        db.session.commit()
        flash(f'{ticker} lagt til i porteføljen.', 'success')
        return redirect(url_for('portfolio.index'))
    
    return render_template('portfolio/add_stock.html')

@portfolio.route('/edit/<ticker>', methods=['GET', 'POST'])
@access_required
def edit_stock(ticker):
    """Edit a stock in the user's portfolio"""
    # Hent brukerens portefølje
    user_portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    if not user_portfolio:
        flash('Du har ingen portefølje ennå.', 'warning')
        return redirect(url_for('portfolio.index'))
    
    # Finn aksjen
    portfolio_stock = PortfolioStock.query.filter_by(
        portfolio_id=user_portfolio.id,
        ticker=ticker
    ).first_or_404()
    
    if request.method == 'POST':
        quantity = float(request.form.get('quantity', 0))
        purchase_price = float(request.form.get('purchase_price', 0))
        
        if quantity <= 0 or purchase_price <= 0:
            flash('Alle felt må fylles ut korrekt.', 'danger')
            return redirect(url_for('portfolio.edit_stock', ticker=ticker))
        
        # Oppdater aksjen
        portfolio_stock.shares = quantity
        portfolio_stock.purchase_price = purchase_price
        db.session.commit()
        
        flash(f'{ticker} oppdatert i porteføljen.', 'success')
        return redirect(url_for('portfolio.index'))
    
    return render_template('portfolio/edit_stock.html', stock=portfolio_stock)

@portfolio.route('/remove/<ticker>')
@access_required
def remove_stock(ticker):
    """Remove a stock from the user's portfolio"""
    # Hent brukerens portefølje
    user_portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    if not user_portfolio:
        flash('Du har ingen portefølje ennå.', 'warning')
        return redirect(url_for('portfolio.index'))
    
    # Finn aksjen
    portfolio_stock = PortfolioStock.query.filter_by(
        portfolio_id=user_portfolio.id,
        ticker=ticker
    ).first_or_404()
    
    # Slett aksjen
    db.session.delete(portfolio_stock)
    db.session.commit()
    
    flash(f'{ticker} fjernet fra porteføljen.', 'success')
    return redirect(url_for('portfolio.index'))

@portfolio.route('/transactions')
@access_required
def transactions():
    """Show transaction history"""
    return render_template('main/coming_soon.html', message="Kommer senere")

@portfolio.route('/advanced')
@portfolio.route('/advanced/')
@access_required
def advanced():
    """Advanced portfolio analysis page"""
    try:
        # Provide sample data for the advanced portfolio page
        sample_data = {
            'expected_return': 8.5,
            'volatility': 12.3,
            'sharpe_ratio': 0.69,
            'max_drawdown': -15.2,
            'portfolio_value': 500000,
            'total_return': 12.4
        }
        return render_template('portfolio/advanced.html', **sample_data)
    except Exception as e:
        current_app.logger.error(f"Error loading advanced portfolio page: {e}")
        # Provide a basic fallback instead of redirect to avoid loops
        return render_template('portfolio/advanced.html', 
                             error=True, 
                             error_message="Avansert analyse midlertidig utilgjengelig")

# Helper method to get stock data
def get_single_stock_data(ticker):
    """Get data for a single stock"""
    try:
        # Hent gjeldende data
        stock_data = get_data_service().get_stock_data(ticker, period='1d')
        if stock_data.empty:
            return None
            
        # Teknisk analyse
        AnalysisService = get_analysis_service()
        ta_data = AnalysisService.get_technical_analysis(ticker) if AnalysisService else None
        
        # Sett sammen data
        last_price = stock_data['Close'].iloc[-1]
        change = 0
        change_percent = 0
        
        if len(stock_data) > 1:
            prev_price = stock_data['Close'].iloc[-2]
            change = last_price - prev_price
            change_percent = (change / prev_price) * 100 if prev_price > 0 else 0
        
        return {
            'ticker': ticker,
            'last_price': round(last_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'signal': ta_data.get('signal', 'Hold') if ta_data else 'Hold',
            'rsi': ta_data.get('rsi', 50) if ta_data else 50,
            'volume': ta_data.get('volume', 100000) if ta_data else 100000
        }
    except Exception as e:
        print(f"Error getting data for {ticker}: {str(e)}")
        return None

@portfolio.route('/api/export', methods=['GET'])
@login_required
@access_required
def export_portfolio():
    """Eksporter portefølje til CSV eller PDF"""
    try:
        import pandas as pd
        from flask import Response
        format = request.args.get('format', 'csv')
        
        # Hent porteføljedata for bruker
        portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
        data = []
        
        for p in portfolios:
            for stock in p.stocks:
                data.append({
                    'Portefølje': p.name,
                    'Ticker': stock.ticker,
                    'Antall': format_number_norwegian(stock.quantity),
                    'Kjøpspris': format_currency_norwegian(stock.purchase_price),
                    'Nåverdi': format_currency_norwegian(stock.current_value),
                    'Kjøpsdato': stock.purchase_date.strftime('%d.%m.%Y') if stock.purchase_date else ''
                })
        
        if not data:
            raise UserFriendlyError('portfolio_not_found')
        
        df = pd.DataFrame(data)
        
        if format == 'csv':
            csv_data = df.to_csv(index=False, sep=';', decimal=',')
            return Response(
                csv_data,
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment;filename=portefolje.csv'}
            )
        elif format == 'pdf':
            # Try to use reportlab for PDF generation
            reportlab_components = get_reportlab()
            if not reportlab_components:
                # Fallback to CSV if reportlab is not available
                csv_data = df.to_csv(index=False, sep=';', decimal=',')
                return Response(
                    csv_data,
                    mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment;filename=portefolje.csv'}
                )
            
            try:
                buffer = BytesIO()
                doc = reportlab_components['SimpleDocTemplate'](buffer, pagesize=reportlab_components['A4'])
                table_data = [df.columns.tolist()] + df.values.tolist()
                table = reportlab_components['Table'](table_data)
                table.setStyle(reportlab_components['TableStyle']([
                    ('BACKGROUND', (0, 0), (-1, 0), reportlab_components['colors'].lightgrey),
                    ('GRID', (0, 0), (-1, -1), 0.5, reportlab_components['colors'].grey),
                ]))
                doc.build([table])
                
                buffer.seek(0)
                return Response(
                    buffer.read(),
                    mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=portefolje.pdf'}
                )
            except Exception:
                # Fallback to CSV if PDF generation fails
                csv_data = df.to_csv(index=False, sep=';', decimal=',')
                return Response(
                    csv_data,
                    mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment;filename=portefolje.csv'}
                )
        else:
            raise UserFriendlyError('invalid_file_type')
            
    except UserFriendlyError as e:
        return handle_api_error(e, 'export_portfolio')
    except Exception as e:
        current_app.logger.error(f"Export error: {e}")
        return handle_api_error(
            UserFriendlyError('export_failed'), 
            'export_portfolio'
        )

# =============================================================================
# ADVANCED PORTFOLIO OPTIMIZATION AND ANALYTICS API ENDPOINTS
# =============================================================================

@portfolio.route('/optimization')
@access_required  
def optimization_page():
    """Portfolio optimization interface"""
    try:
        return render_template('portfolio/optimization.html',
                             title='Portfolio Optimization')
    except Exception as e:
        logger.error(f"Optimization page error: {e}")
        return render_template('error.html', error=str(e)), 500

@portfolio.route('/performance-analytics')
@access_required
def performance_page():
    """Performance analytics interface"""
    try:
        return render_template('portfolio/performance.html',
                             title='Performance Analytics')
    except Exception as e:
        logger.error(f"Performance page error: {e}")
        return render_template('error.html', error=str(e)), 500

@portfolio.route('/api/optimization', methods=['POST'])
@access_required
def api_portfolio_optimization():
    """API endpoint for portfolio optimization"""
    try:
        data = request.get_json()
        
        # Extract parameters
        holdings = data.get('holdings', [])
        risk_tolerance = data.get('risk_tolerance', 'moderate')
        target_return = data.get('target_return')
        
        # Validate holdings data
        if not holdings:
            return jsonify({
                'success': False,
                'error': 'Holdings data is required'
            }), 400
        
        # Perform optimization
        optimization_result = PortfolioOptimizationService.optimize_portfolio(
            holdings=holdings,
            risk_tolerance=risk_tolerance,
            target_return=target_return
        )
        
        return jsonify(optimization_result)
        
    except Exception as e:
        logger.error(f"Portfolio optimization API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@portfolio.route('/api/risk-metrics', methods=['POST'])
@access_required
def api_risk_metrics():
    """API endpoint for comprehensive risk analysis"""
    try:
        data = request.get_json()
        
        holdings = data.get('holdings', [])
        timeframe_days = data.get('timeframe_days', 252)
        
        if not holdings:
            return jsonify({
                'success': False,
                'error': 'Holdings data is required'
            }), 400
        
        # Calculate risk metrics
        risk_analysis = PortfolioOptimizationService.calculate_risk_metrics(
            holdings=holdings,
            timeframe_days=timeframe_days
        )
        
        return jsonify(risk_analysis)
        
    except Exception as e:
        logger.error(f"Risk metrics API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@portfolio.route('/api/scenario-analysis', methods=['POST'])
@access_required
def api_scenario_analysis():
    """API endpoint for Monte Carlo scenario analysis"""
    try:
        data = request.get_json()
        
        holdings = data.get('holdings', [])
        scenarios = data.get('scenarios', None)
        
        if not holdings:
            return jsonify({
                'success': False,
                'error': 'Holdings data is required'
            }), 400
        
        # Generate scenario analysis
        scenario_results = PortfolioOptimizationService.generate_scenario_analysis(
            holdings=holdings,
            scenarios=scenarios
        )
        
        return jsonify(scenario_results)
        
    except Exception as e:
        logger.error(f"Scenario analysis API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@portfolio.route('/api/performance-attribution', methods=['POST'])
@access_required
def api_performance_attribution():
    """API endpoint for performance attribution analysis"""
    try:
        data = request.get_json()
        
        holdings = data.get('holdings', [])
        benchmark = data.get('benchmark', 'OSEBX')
        periods = data.get('periods', None)
        
        if not holdings:
            return jsonify({
                'success': False,
                'error': 'Holdings data is required'
            }), 400
        
        # Calculate performance attribution
        attribution_results = PerformanceTrackingService.calculate_performance_attribution(
            holdings=holdings,
            benchmark=benchmark,
            periods=periods
        )
        
        return jsonify(attribution_results)
        
    except Exception as e:
        logger.error(f"Performance attribution API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@portfolio.route('/api/benchmark-comparison', methods=['POST'])
@access_required
def api_benchmark_comparison():
    """API endpoint for benchmark comparison analysis"""
    try:
        data = request.get_json()
        
        holdings = data.get('holdings', [])
        benchmarks = data.get('benchmarks', None)
        
        if not holdings:
            return jsonify({
                'success': False,
                'error': 'Holdings data is required'
            }), 400
        
        # Generate benchmark comparison
        comparison_results = PerformanceTrackingService.generate_benchmark_comparison(
            holdings=holdings,
            benchmarks=benchmarks
        )
        
        return jsonify(comparison_results)
        
    except Exception as e:
        logger.error(f"Benchmark comparison API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@portfolio.route('/api/factor-exposure', methods=['POST'])
@access_required
def api_factor_exposure():
    """API endpoint for factor exposure analysis"""
    try:
        data = request.get_json()
        
        holdings = data.get('holdings', [])
        
        if not holdings:
            return jsonify({
                'success': False,
                'error': 'Holdings data is required'
            }), 400
        
        # Calculate factor exposures
        factor_results = PerformanceTrackingService.calculate_factor_exposure(
            holdings=holdings
        )
        
        return jsonify(factor_results)
        
    except Exception as e:
        logger.error(f"Factor exposure API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@portfolio.route('/api/portfolio-health', methods=['POST'])
@access_required
def api_portfolio_health():
    """API endpoint for comprehensive portfolio health check"""
    try:
        data = request.get_json()
        
        holdings = data.get('holdings', [])
        
        if not holdings:
            return jsonify({
                'success': False,
                'error': 'Holdings data is required'
            }), 400
        
        # Comprehensive health analysis
        health_analysis = _generate_portfolio_health_analysis(holdings)
        
        return jsonify(health_analysis)
        
    except Exception as e:
        logger.error(f"Portfolio health API error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _generate_portfolio_health_analysis(holdings):
    """Generate comprehensive portfolio health analysis"""
    try:
        # Basic portfolio statistics
        total_positions = len(holdings)
        total_value = sum(holding.get('value', 0) for holding in holdings)
        
        # Concentration analysis
        largest_position = max(holding.get('weight', 0) for holding in holdings) if holdings else 0
        top_5_concentration = sum(sorted([h.get('weight', 0) for h in holdings], reverse=True)[:5])
        
        # Diversification metrics
        hhi_index = sum(h.get('weight', 0)**2 for h in holdings)  # Herfindahl-Hirschman Index
        effective_positions = 1 / hhi_index if hhi_index > 0 else 0
        
        # Risk indicators
        risk_indicators = []
        if largest_position > 0.20:
            risk_indicators.append("High concentration in single position")
        if top_5_concentration > 0.60:
            risk_indicators.append("High concentration in top 5 positions")
        if total_positions < 10:
            risk_indicators.append("Limited diversification - consider more positions")
        if effective_positions < 5:
            risk_indicators.append("Low effective diversification")
        
        # Health score calculation
        health_score = 100
        health_score -= min(largest_position * 200, 40)  # Concentration penalty
        health_score -= max(0, (0.60 - top_5_concentration) * -50)  # Diversification bonus
        health_score -= max(0, (10 - total_positions) * 2)  # Position count penalty
        health_score = max(0, min(100, health_score))
        
        # Health grade
        if health_score >= 80:
            health_grade = 'Excellent'
        elif health_score >= 65:
            health_grade = 'Good'
        elif health_score >= 50:
            health_grade = 'Fair'
        else:
            health_grade = 'Poor'
        
        # Recommendations
        recommendations = []
        if largest_position > 0.15:
            recommendations.append("Consider reducing largest position concentration")
        if total_positions < 15:
            recommendations.append("Add more positions for better diversification")
        if len(risk_indicators) == 0:
            recommendations.append("Portfolio shows good diversification characteristics")
        
        return {
            'success': True,
            'health_metrics': {
                'total_positions': total_positions,
                'total_value': round(total_value, 2),
                'largest_position_weight': round(largest_position, 4),
                'top_5_concentration': round(top_5_concentration, 4),
                'hhi_index': round(hhi_index, 4),
                'effective_positions': round(effective_positions, 2),
                'health_score': round(health_score, 1),
                'health_grade': health_grade
            },
            'risk_indicators': risk_indicators,
            'recommendations': recommendations,
            'diversification_analysis': {
                'concentration_risk': 'High' if largest_position > 0.20 else 'Low',
                'diversification_level': 'Good' if effective_positions > 10 else 'Needs Improvement',
                'position_sizing': 'Balanced' if largest_position < 0.15 else 'Concentrated'
            },
            'timestamp': 'datetime.utcnow().isoformat()'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
        return jsonify({'error': 'Ugyldig format'}), 400