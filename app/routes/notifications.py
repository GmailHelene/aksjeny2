"""
Notification routes for real-time user alerts
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.notifications import Notification
from ..models.user import User
from ..services.notification_service import notification_service
from ..extensions import db
from ..utils.access_control import access_required, demo_access
from datetime import datetime, timedelta
import logging

notifications_bp = Blueprint('notifications', __name__)
logger = logging.getLogger(__name__)

@notifications_bp.route('/')
@login_required
def index():
    """Main notifications page"""
    try:
        # Get filter parameters
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        # Build query
        query = Notification.query.filter_by(user_id=current_user.id)
        
        if unread_only:
            query = query.filter_by(read=False)
        
        # Order by newest first
        query = query.order_by(Notification.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        notifications = pagination.items
        
        # Get summary statistics
        total_count = Notification.query.filter_by(user_id=current_user.id).count()
        unread_count = Notification.query.filter_by(user_id=current_user.id, read=False).count()
        
        # Get counts by type
        type_counts = db.session.query(
            Notification.type, 
            db.func.count(Notification.id)
        ).filter_by(user_id=current_user.id).group_by(Notification.type).all()
        
        summary = {
            'total': total_count,
            'unread': unread_count,
            'types': dict(type_counts),
            'recent_activity': Notification.query.filter_by(user_id=current_user.id)\
                .filter(Notification.created_at >= datetime.utcnow() - timedelta(days=7)).count(),
            'priority_breakdown': {
                'high': Notification.query.filter_by(user_id=current_user.id, priority='high').count(),
                'medium': Notification.query.filter_by(user_id=current_user.id, priority='medium').count(),
                'low': Notification.query.filter_by(user_id=current_user.id, priority='low').count()
            }
        }
        
        return render_template('notifications/index.html',
                             notifications=notifications,
                             pagination=pagination,
                             unread_only=unread_only,
                             summary=summary)
    except Exception as e:
        logger.error(f"Error loading notifications: {str(e)}")
        flash('Error loading notifications. Please try again later.', 'error')
        return redirect(url_for('main.index'))

@notifications_bp.route('/api/mark-read/<int:notification_id>', methods=['POST'])
@login_required
def api_mark_read(notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.query.filter_by(
            id=notification_id, 
            user_id=current_user.id
        ).first()
        
        if not notification:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        notification.read = True
        notification.read_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error marking notification as read: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/api/mark-unread/<int:notification_id>', methods=['POST'])
@login_required
def api_mark_unread(notification_id):
    """Mark notification as unread"""
    try:
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=current_user.id
        ).first()

        if not notification:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404

        notification.read = False
        notification.read_at = None
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error marking notification as unread: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/api/mark-all-read', methods=['POST'])
@login_required
def api_mark_all_read():
    """Mark all notifications as read"""
    try:
        Notification.query.filter_by(
            user_id=current_user.id, 
            read=False
        ).update({
            'read': True,
            'read_at': datetime.utcnow()
        })
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/api/delete/<int:notification_id>', methods=['DELETE'])
@login_required
def api_delete(notification_id):
    """Delete a notification"""
    try:
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=current_user.id
        ).first()
        
        if not notification:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/api/unread-count')
@login_required
def api_unread_count():
    """Get unread notification count"""
    try:
        count = Notification.query.filter_by(
            user_id=current_user.id,
            read=False
        ).count()
        
        return jsonify({'success': True, 'count': count})
    except Exception as e:
        logger.error(f"Error getting unread count: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Notification settings page"""
    try:
        if request.method == 'POST':
            # Handle both form and JSON data submission
            if request.is_json:
                # Handle JSON request from JavaScript
                settings_data = request.get_json()
                if not settings_data:
                    return jsonify({'success': False, 'error': 'No data provided'}), 400
            else:
                # Handle form submission
                settings_data = {
                    'email_enabled': 'email_enabled' in request.form,
                    'push_enabled': 'push_enabled' in request.form,
                    'price_alerts': 'price_alerts' in request.form,
                    'insider_alerts': 'insider_alerts' in request.form,
                    'earnings_alerts': 'earnings_alerts' in request.form,
                    'analyst_alerts': 'analyst_alerts' in request.form,
                    'volume_alerts': 'volume_alerts' in request.form,
                    'daily_summary': 'daily_summary' in request.form,
                    'market_news': 'market_news' in request.form,
                    'system_updates': 'system_updates' in request.form
                }
            
            try:
                # Update user settings with error handling
                update_success = current_user.update_notification_settings(settings_data)
                if update_success:
                    db.session.commit()
                    logger.info(f"Successfully updated notification settings for user {current_user.id}")
                else:
                    db.session.rollback()
                    logger.error(f"Failed to update notification settings for user {current_user.id}")
                    raise Exception("Failed to update settings")
                    
            except Exception as update_error:
                logger.error(f"Error updating notification settings: {update_error}")
                db.session.rollback()
                if request.is_json:
                    return jsonify({'success': False, 'error': 'Failed to update settings'}), 500
                else:
                    flash('Failed to update notification settings. Please try again.', 'error')
                    return redirect(url_for('notifications.settings'))
            
            if request.is_json:
                return jsonify({'success': True, 'message': 'Settings updated successfully'})
            else:
                flash('Notification settings updated successfully!', 'success')
                return redirect(url_for('notifications.settings'))
        
        # GET request - show form
        try:
            # Get user's notification preferences using new methods with error handling
            user_settings = current_user.get_notification_settings()
            if not user_settings or not isinstance(user_settings, dict):
                logger.warning(f"Invalid user settings for user {current_user.id}, using defaults")
                user_settings = {}
                
        except Exception as settings_error:
            logger.error(f"Error getting notification settings for user {current_user.id}: {settings_error}")
            user_settings = {}
        
        preferences = {
            'email_enabled': user_settings.get('email_enabled', True),
            'push_enabled': user_settings.get('push_enabled', False),
            'price_alerts': user_settings.get('price_alerts', True),
            'insider_alerts': user_settings.get('insider_alerts', True),
            'earnings_alerts': user_settings.get('earnings_alerts', True),
            'analyst_alerts': user_settings.get('analyst_alerts', True),
            'volume_alerts': user_settings.get('volume_alerts', False),
            'daily_summary': user_settings.get('daily_summary', False),
            'market_news': user_settings.get('market_news', False),
            'system_updates': user_settings.get('system_updates', True)
        }
        
        return render_template('notifications/settings.html', preferences=preferences)
    except Exception as e:
        logger.error(f"Error with notification settings: {str(e)}")
        flash('Error with settings. Please try again later.', 'error')
        return redirect(url_for('notifications.index'))

@notifications_bp.route('/api/settings', methods=['GET', 'POST']) 
@demo_access
def api_update_settings():
    """API endpoint for notification settings"""
    try:
        # Check if user is authenticated
        if not current_user.is_authenticated:
            return jsonify({
                'success': False, 
                'error': 'Authentication required for notification settings'
            }), 401
            
        if request.method == 'GET':
            # Return current settings
            user_settings = current_user.get_notification_settings()
            return jsonify({
                'success': True,
                'settings': user_settings
            })
        
        elif request.method == 'POST':
            # Update settings from JSON data
            settings_data = request.get_json()
            
            if not settings_data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
            
            # Make sure all checkbox values are boolean
            for key, value in settings_data.items():
                if key.endswith('_enabled') or key in ['email_price_alerts', 'email_news_alerts', 
                                                     'push_price_alerts', 'push_news_alerts']:
                    settings_data[key] = bool(value)
            
            # Update user settings
            try:
                success = current_user.update_notification_settings(settings_data)
                if not success:
                    return jsonify({'success': False, 'error': 'Failed to save settings in database'}), 500
                    
                db.session.commit()
                return jsonify({'success': True, 'message': 'Settings updated successfully'})
            except Exception as db_error:
                db.session.rollback()
                logger.error(f"Database error saving notification settings: {str(db_error)}")
                return jsonify({'success': False, 'error': str(db_error)}), 500
            
    except Exception as e:
        logger.error(f"Error in API settings: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/api/test', methods=['POST'])
@login_required
def api_test_notification():
    """Send a test notification"""
    try:
        notification_service.create_notification(
            user_id=current_user.id,
            notification_type='SYSTEM_UPDATE',
            title='Test Varsel',
            message='Dette er et testvarsel for å verifisere at innstillingene dine fungerer korrekt.',
            priority='medium'
        )
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error sending test notification: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/api/push_subscription', methods=['POST'])
@login_required
def save_push_subscription():
    """Save push notification subscription with enhanced error handling"""
    try:
        subscription_data = request.get_json()
        
        if not subscription_data:
            return jsonify({
                'success': False, 
                'error': 'Push notifications krever HTTPS og brukerens samtykke. Kontroller at nettleseren støtter push notifications.'
            }), 400
        
        # Store the push subscription data
        import json
        if hasattr(current_user, 'push_subscription'):
            current_user.push_subscription = json.dumps(subscription_data)
            current_user.push_notifications = True
            db.session.commit()
            logger.info(f"✅ Push subscription saved for user {current_user.id}")
        else:
            # Graceful fallback - user can still use other notification methods
            logger.warning(f"User model doesn't support push subscriptions, using fallback for user {current_user.id}")
            return jsonify({
                'success': True,
                'fallback': True,
                'message': 'Push notifications er ikke tilgjengelig, men e-post og in-app notifications fungerer.'
            })
        
        return jsonify({'success': True, 'message': 'Push notifications aktivert!'})
    except Exception as e:
        logger.error(f"Error saving push subscription: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'Push notifications kan ikke aktiveres. Dette kan skyldes nettleserinnstillinger eller at siden ikke er tilgjengelig via HTTPS.',
            'fallback_available': True,
            'fallback_message': 'E-post og in-app notifications er fortsatt tilgjengelig.'
        }), 500

@notifications_bp.route('/api/clear-read', methods=['POST'])
@login_required
def api_clear_read():
    """Clear all read notifications"""
    try:
        Notification.query.filter_by(
            user_id=current_user.id,
            read=True
        ).delete()
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error clearing read notifications: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Web interface routes
notifications_web_bp = Blueprint('notifications_web', __name__, url_prefix='/notifications')

@notifications_web_bp.route('/')
@login_required
def notifications_page():
    """Notifications page"""
    return render_template('notifications/index.html')

@notifications_web_bp.route('/settings')
@login_required
def settings_page():
    """Notification settings page"""
    return render_template('notifications/settings.html')

@notifications_bp.route('/api/notifications', methods=['GET'])
@login_required
def api_get_notifications():
    """Get all notifications for the user"""
    try:
        notifications = Notification.query.filter_by(user_id=current_user.id).all()
        return jsonify({'success': True, 'notifications': [n.to_dict() for n in notifications]})
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@notifications_bp.route('/api/user/preferences', methods=['GET', 'POST'])
@login_required
def user_preferences():
    """User notification preferences API"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            
            # Update user's language setting
            if 'language' in data:
                current_user.set_language(data['language'])
            
            # Update notification settings using the new notification_settings column
            current_settings = current_user.get_notification_settings()
            
            # Update settings from request data
            if 'display_mode' in data:
                current_settings['display_mode'] = data['display_mode']
            if 'number_format' in data:
                current_settings['number_format'] = data['number_format']
            if 'dashboard_widgets' in data:
                current_settings['dashboard_widgets'] = data['dashboard_widgets']
            if 'email_enabled' in data:
                current_settings['email_enabled'] = data['email_enabled']
            if 'push_enabled' in data:
                current_settings['push_enabled'] = data['push_enabled']
            
            # Save updated settings
            success = current_user.update_notification_settings(current_settings)
            
            if success:
                return jsonify({'success': True, 'message': 'Preferanser oppdatert'})
            else:
                return jsonify({'success': False, 'error': 'Kunne ikke lagre preferanser'})
        
        # GET request - return current preferences
        current_settings = current_user.get_notification_settings()
        
        # Return preferences with safe defaults
        preferences = {
            'language': current_user.get_language(),
            'display_mode': current_settings.get('display_mode', 'light'),
            'number_format': current_settings.get('number_format', 'norwegian'),
            'dashboard_widgets': current_settings.get('dashboard_widgets', 'default'),
            'email_enabled': current_settings.get('email_enabled', True),
            'push_enabled': current_settings.get('push_enabled', False)
        }
        
        return jsonify(preferences)
        
    except Exception as e:
        logger.error(f"Error in user preferences: {e}")
        return jsonify({'success': False, 'error': 'Kunne ikke hente preferanser'})
