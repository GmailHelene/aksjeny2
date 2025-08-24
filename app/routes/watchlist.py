from flask import Blueprint, jsonify, current_app, render_template
from flask_login import login_required, current_user
from ..models.watchlist import Watchlist
from ..extensions import db
from ..utils.access_control import access_required

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
            default_watchlist = {
                'id': 0,
                'name': 'Demo Watchlist',
                'description': 'Eksempel på watchlist. Logg inn for å opprette din egen.',
                'items': [],
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'price_alerts_enabled': True,
                'technical_alerts_enabled': True
            }
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
