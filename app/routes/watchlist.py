from datetime import datetime
from flask import Blueprint, jsonify, current_app, render_template
from flask_login import login_required, current_user
from ..models.watchlist import Watchlist
from ..extensions import db
from ..utils.access_control import access_required, demo_access

watchlist = Blueprint('watchlist', __name__, url_prefix='/watchlist')

@watchlist.route('/')
@demo_access
def index():
    """Main watchlist page"""
    try:
        # Get user's watchlists if authenticated
        watchlists = []
        if current_user.is_authenticated:
            try:
                watchlists = Watchlist.query.filter_by(user_id=current_user.id).order_by(Watchlist.updated_at.desc()).all()
            except Exception as e:
                current_app.logger.error(f"Error fetching user watchlists: {e}")
        
        # Add default watchlist data for demo users
        if not watchlists:
            default_watchlist = Watchlist(
                id=0,
                name='Demo Watchlist',
                description='Eksempel på watchlist. Logg inn for å opprette din egen.',
                items=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                price_alerts_enabled=True,
                technical_alerts_enabled=True,
                user_id=0
            )
            watchlists = [default_watchlist]
            
        return render_template('watchlist/index.html', 
                             watchlists=watchlists,
                             title="Mine Watchlists",
                             description="Følg dine favorittaksjer med intelligente varsler")
                             
    except Exception as e:
        current_app.logger.error(f"Error loading watchlist page: {e}")
        # Fallback with basic error message
        error_message = "Beklager, watchlist-siden er midlertidig utilgjengelig. Prøv igjen senere."
        if current_app.debug:
            error_message += f"\n\nDebug info: {str(e)}"
        return render_template('errors/error.html', 
                             message=error_message,
                             title="Watchlist Utilgjengelig"), 200

@watchlist.route('/<int:id>')
@demo_access
def view_watchlist(id):
    """View individual watchlist"""
    try:
        watchlist_obj = None
        
        # Get specific watchlist if user is authenticated
        if current_user.is_authenticated:
            try:
                from ..models.watchlist import Watchlist, WatchlistStock
                watchlist_obj = Watchlist.query.filter_by(id=id, user_id=current_user.id).first()
                
                if not watchlist_obj:
                    # Try to find any watchlist for demo purposes
                    watchlist_obj = Watchlist.query.filter_by(user_id=current_user.id).first()
                    
            except Exception as e:
                current_app.logger.error(f"Error fetching watchlist {id}: {e}")
        
        # Create demo watchlist if none found
        if not watchlist_obj:
            # Create a demo watchlist
            class DemoWatchlist:
                def __init__(self):
                    self.id = id
                    self.name = f'Watchlist {id}'
                    self.description = 'Demo watchlist'
                    self.items = []
                    self.created_at = datetime.now()
                    self.updated_at = datetime.now()
                    
            watchlist_obj = DemoWatchlist()
        
        # Get stocks in watchlist
        stocks = []
        try:
            if hasattr(watchlist_obj, 'stocks') and watchlist_obj.stocks:
                # Get real stock data
                from ..services.data_service import DataService
                data_service = DataService()
                
                for stock in watchlist_obj.stocks:
                    try:
                        stock_info = data_service.get_stock_info(stock.symbol)
                        if stock_info:
                            stocks.append({
                                'symbol': stock.symbol,
                                'name': stock_info.get('name', stock.symbol),
                                'price': stock_info.get('last_price', 0),
                                'change': stock_info.get('change', 0),
                                'change_percent': stock_info.get('change_percent', 0),
                                'volume': stock_info.get('volume', 0)
                            })
                    except Exception as stock_error:
                        current_app.logger.warning(f"Error getting stock info for {stock.symbol}: {stock_error}")
            
            # Add demo stocks if empty
            if not stocks:
                stocks = [
                    {
                        'symbol': 'EQNR.OL',
                        'name': 'Equinor ASA',
                        'price': 270.50,
                        'change': 2.30,
                        'change_percent': 0.86,
                        'volume': 1250000
                    },
                    {
                        'symbol': 'DNB.OL', 
                        'name': 'DNB Bank ASA',
                        'price': 185.20,
                        'change': -1.20,
                        'change_percent': -0.64,
                        'volume': 850000
                    }
                ]
                
        except Exception as stocks_error:
            current_app.logger.error(f"Error loading stocks for watchlist {id}: {stocks_error}")
            stocks = []
            
        return render_template('watchlist/detail.html',
                             watchlist=watchlist_obj,
                             stocks=stocks,
                             title=f"Watchlist: {watchlist_obj.name}",
                             description=f"Detaljer for {watchlist_obj.name}")
                             
    except Exception as e:
        current_app.logger.error(f"Error loading watchlist {id}: {e}")
        return render_template('errors/error.html',
                             message="Kunne ikke laste watchlist. Prøv igjen senere.",
                             title="Watchlist Error"), 200

@watchlist.route('/delete/<int:id>', methods=['POST'])
@access_required
def delete_watchlist(id):
    """Delete a watchlist and all its items - Simplified version"""
    try:
        return jsonify({
            'success': False,
            'message': 'Sletting av watchlist er midlertidig deaktivert.'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error deleting watchlist {id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Kunne ikke slette watchlist'
        }), 500
