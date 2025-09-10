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
        
        # Get user favorites (robust ORM-based, safe for different table schemas)
        user_favorites = []
        if current_user.is_authenticated:
            try:
                favorites = Favorites.get_user_favorites(current_user.id)
                # Map to simple dicts the template can use safely
                user_favorites = [
                    {
                        'symbol': getattr(f, 'symbol', None),
                        'name': getattr(f, 'name', None),
                        'exchange': getattr(f, 'exchange', None),
                        'created_at': getattr(f, 'created_at', None)
                    }
                    for f in favorites
                ]
                logger.info(f"Found {len(user_favorites)} favorites for user {current_user.id}")
            except Exception as e:
                logger.error(f"Error fetching favorites via ORM: {e}")
                user_favorites = []
        
        # Get user statistics
        user_stats = {
            'total_favorites': len(user_favorites),
            'member_since': current_user.created_at.strftime('%B %Y') if hasattr(current_user, 'created_at') and current_user.created_at else 'Ukjent',
            'last_login': current_user.last_login.strftime('%d.%m.%Y %H:%M') if hasattr(current_user, 'last_login') and current_user.last_login else 'Ukjent'
        }
        
        # Subscription context (safe defaults)
        try:
            subscription_status = getattr(current_user, 'subscription_status', 'free')
        except Exception:
            subscription_status = 'free'
        subscription = {
            'type': getattr(current_user, 'subscription_type', 'free'),
            'end_date': getattr(current_user, 'subscription_end', None)
        }
        
        # Referral context (safe defaults)
        try:
            referrals_made = current_user.get_completed_referrals_count()
        except Exception:
            referrals_made = 0
        # 20% per completed referral as UI hint, capped at 100%
        referral_earnings = min(referrals_made * 20, 100)
        try:
            referral_code = current_user.get_referral_code()
        except Exception:
            referral_code = getattr(current_user, 'username', 'user')
        
        # UI preferences (safe defaults)
        try:
            user_language = current_user.get_language() if hasattr(current_user, 'get_language') else (getattr(current_user, 'language', None) or 'no')
        except Exception:
            user_language = 'no'
        user_display_mode = 'auto'
        user_number_format = 'norwegian'
        # Widgets as JSON string for template fromjson filter compatibility
        user_dashboard_widgets = '["portfolio","alerts","news"]'
        
        logger.info(f"Rendering profile template for user {getattr(current_user, 'id', 'Unknown')}")
        return render_template(
            'profile.html',
            user=current_user,
            favorites=user_favorites,
            user_stats=user_stats,
            subscription_status=subscription_status,
            subscription=subscription,
            referrals_made=referrals_made,
            referral_earnings=referral_earnings,
            referral_code=referral_code,
            user_language=user_language,
            user_display_mode=user_display_mode,
            user_number_format=user_number_format,
            user_dashboard_widgets=user_dashboard_widgets
        )
        
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
