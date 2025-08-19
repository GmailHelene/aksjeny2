from flask import Blueprint, request, jsonify, current_app, session
from flask_login import login_required, current_user
from .. import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/settings/notifications', methods=['POST'])
@login_required
def update_notifications():
    try:
        data = request.get_json()
        
        # Update user notification preferences
        if hasattr(current_user, 'email_notifications'):
            current_user.email_notifications = data.get('email_notifications', False)
        if hasattr(current_user, 'price_alerts'):
            current_user.price_alerts = data.get('price_alerts', False)
        if hasattr(current_user, 'market_news'):
            current_user.market_news = data.get('market_news', False)
        
        # If user model doesn't have these fields, store in session for now
        if not hasattr(current_user, 'email_notifications'):
            session['email_notifications'] = data.get('email_notifications', False)
            session['price_alerts'] = data.get('price_alerts', False)
            session['market_news'] = data.get('market_news', False)
        else:
            db.session.commit()
        
        return jsonify({'success': True, 'message': 'Varselinnstillinger oppdatert'})
        
    except Exception as e:
        current_app.logger.error(f"Error updating notifications: {str(e)}")
        if hasattr(db, 'session'):
            db.session.rollback()
        return jsonify({'success': False, 'message': 'Feil ved oppdatering av varselinnstillinger'}), 500