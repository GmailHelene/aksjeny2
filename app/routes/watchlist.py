from flask import Blueprint, jsonify, current_app
from flask_login import login_required, current_user
from app.models import Watchlist, WatchlistItem, db
from app.utils.access_control import access_required

watchlist = Blueprint('watchlist', __name__, url_prefix='/watchlist')

@watchlist.route('/delete/<int:id>', methods=['POST'])
@access_required
def delete_watchlist(id):
    """Delete a watchlist and all its items"""
    try:
        # Get watchlist and verify ownership
        watchlist_obj = Watchlist.query.filter_by(id=id, user_id=current_user.id).first()
        if not watchlist_obj:
            return jsonify({
                'success': False,
                'error': 'Watchlist ikke funnet eller du har ikke tilgang'
            }), 404
            
        # Delete all items in the watchlist
        try:
            WatchlistItem.query.filter_by(watchlist_id=id).delete()
        except Exception as e:
            current_app.logger.error(f"Error deleting watchlist items for watchlist {id}: {e}")
            
        # Delete the watchlist itself
        db.session.delete(watchlist_obj)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Watchlist slettet'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error deleting watchlist {id}: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Kunne ikke slette watchlist'
        }), 500
