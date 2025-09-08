from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_login import current_user, login_required
from sqlalchemy import text
from ..models import User
from ..models.favorites import Favorites
from ..extensions import db
from ..utils.access_control_unified import unified_access_required
import logging
from datetime import datetime

profile = Blueprint('profile', __name__)
logger = logging.getLogger(__name__)

@profile.route('/')
@login_required
@unified_access_required
def profile_page():
    """User profile page"""
    try:
        logger.info(f"Loading profile page for user ID: {getattr(current_user, 'id', 'Unknown')}")
        
        # Get user favorites
        user_favorites = []
        if current_user.is_authenticated:
            try:
                favorites_query = text("""
                    SELECT symbol, company_name, price, change, change_percent, date_added 
                    FROM favorites 
                    WHERE user_id = :user_id 
                    ORDER BY date_added DESC
                """)
                favorites_result = db.session.execute(favorites_query, {'user_id': current_user.id})
                user_favorites = [dict(row._mapping) for row in favorites_result]
                logger.info(f"Found {len(user_favorites)} favorites for user {current_user.id}")
            except Exception as e:
                logger.error(f"Error fetching favorites: {e}")
                user_favorites = []
        
        # Get user statistics
        user_stats = {
            'total_favorites': len(user_favorites),
            'member_since': current_user.created_at.strftime('%B %Y') if hasattr(current_user, 'created_at') and current_user.created_at else 'Ukjent',
            'last_login': current_user.last_login.strftime('%d.%m.%Y %H:%M') if hasattr(current_user, 'last_login') and current_user.last_login else 'Ukjent'
        }
        
        logger.info(f"Rendering profile template for user {getattr(current_user, 'id', 'Unknown')}")
        return render_template('profile.html', 
                             user=current_user,
                             favorites=user_favorites,
                             user_stats=user_stats)
        
    except Exception as e:
        import traceback
        logger.error(f"Error in profile page for user {getattr(current_user, 'id', 'Unknown')}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        flash('Det oppstod en teknisk feil under lasting av profilen', 'error')
        return render_template('errors/500.html', 
                             error_message="Det oppstod en teknisk feil under lasting av profilen. Vennligst prøv igjen senere."), 500
        return redirect(url_for('main.index'))

@profile.route('/profile/update', methods=['POST'])
@login_required
@unified_access_required
def update_profile():
    """Update user profile"""
    try:
        # Get form data
        display_name = request.form.get('display_name', '').strip()
        email = request.form.get('email', '').strip()
        
        # Basic validation
        if not display_name:
            flash('Visningsnavn er påkrevd', 'error')
            return redirect(url_for('profile.profile_page'))
        
        if not email:
            flash('E-post er påkrevd', 'error') 
            return redirect(url_for('profile.profile_page'))
        
        # Update user
        current_user.display_name = display_name
        current_user.email = email
        
        db.session.commit()
        flash('Profil oppdatert!', 'success')
        
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        flash('Kunne ikke oppdatere profil', 'error')
        
    return redirect(url_for('profile.profile_page'))

@profile.route('/profile/favorites/remove/<symbol>', methods=['POST'])
@login_required
@unified_access_required
def remove_favorite(symbol):
    """Remove stock from favorites"""
    try:
        delete_query = text("DELETE FROM favorites WHERE user_id = :user_id AND symbol = :symbol")
        db.session.execute(delete_query, {'user_id': current_user.id, 'symbol': symbol})
        db.session.commit()
        flash(f'{symbol} fjernet fra favoritter', 'success')
    except Exception as e:
        logger.error(f"Error removing favorite {symbol}: {e}")
        flash('Kunne ikke fjerne fra favoritter', 'error')
        
    return redirect(url_for('profile.profile_page'))
