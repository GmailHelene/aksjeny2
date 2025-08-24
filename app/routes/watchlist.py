from flask import Blueprint, jsonify, current_app, render_template
from flask_login import login_required, current_user
from ..models.watchlist import Watchlist
from ..extensions import db
from ..utils.access_control import access_required

watchlist = Blueprint('watchlist', __name__, url_prefix='/watchlist')

@watchlist.route('/')
@access_required
def index():
    """Main watchlist page - Test version"""
    try:
        # Ultra-simple version with basic template
        return render_template('watchlist/index.html', 
                             watchlists=[],
                             title="Mine Watchlists")
                             
    except Exception as e:
        current_app.logger.error(f"Error loading watchlist page: {e}")
        # Ultra-safe fallback with plain HTML
        return "<h1>Watchlist</h1><p>Watchlist-siden er midlertidig utilgjengelig. Prøv igjen senere.</p>", 200

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
