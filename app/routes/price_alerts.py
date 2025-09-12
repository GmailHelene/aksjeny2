"""
Price Alerts Blueprint for managing user stock price alerts
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models.price_alert import PriceAlert, AlertNotificationSettings
from ..services.price_monitor_service import price_monitor  # still used for status & settings
from ..services.data_service import DataService
from ..services.alert_service import list_user_alerts, create_alert as svc_create_alert, delete_alert as svc_delete_alert
from ..utils.access_control import access_required
import logging
import traceback  # Added for detailed error logging

logger = logging.getLogger(__name__)

price_alerts = Blueprint('price_alerts', __name__, url_prefix='/price-alerts')

@price_alerts.route('/')
@access_required
def index():
    """Price alerts dashboard with enhanced error handling and fallback data"""
    try:
        # Get user's alerts with enhanced error handling
        user_alerts = []
        try:
            logger.info(f"(alert_service) Fetching alerts for user {current_user.id}")
            user_alerts = list_user_alerts(current_user.id)
        except Exception as e:
            logger.error(f"alert_service list_user_alerts failed: {e}")
            user_alerts = []
        
        # Get alert settings with fallback
        settings = None
        try:
            settings = AlertNotificationSettings.get_or_create_for_user(current_user.id)
        except Exception as e:
            logger.warning(f"Could not get user settings: {e}")
            # Create minimal settings object
            settings = type('Settings', (), {
                'email_enabled': True,
                'email_instant': True,
                'email_daily_summary': False
            })()
        
        # Get monitoring service status with fallback
        service_status = None
        try:
            service_status = price_monitor.get_service_status()
        except Exception as e:
            logger.warning(f"Could not get service status: {e}")
            service_status = {
                'status': 'running',
                'last_check': 'Unknown',
                'alerts_processed': 0
            }
        
        # Check subscription status for alert limits
        has_subscription = getattr(current_user, 'has_subscription', False)
        active_alerts_count = len([a for a in user_alerts if a.get('is_active', False)])
        alert_limit_reached = not has_subscription and active_alerts_count >= 3
        
        logger.info(f"Rendering price alerts page with {len(user_alerts)} alerts for user {current_user.id}")
        
        return render_template('price_alerts/index.html',
                             alerts=user_alerts,
                             settings=settings,
                             service_status=service_status,
                             has_subscription=has_subscription,
                             alert_limit_reached=alert_limit_reached,
                             active_alerts_count=active_alerts_count)
                             
    except Exception as e:
        logger.error(f"Error loading price alerts dashboard: {e}")
        flash('Kunne ikke laste prisvarsler. Prøv igjen senere.', 'error')
        return redirect(url_for('main.index'))

@price_alerts.route('/create', methods=['GET', 'POST'])
@access_required
def create():
    """Create new price alert with comprehensive error handling"""
    if request.method == 'POST':
        try:
            # Validate CSRF token first
            try:
                from flask_wtf.csrf import validate_csrf
                csrf_token = request.form.get('csrf_token')
                if csrf_token:
                    validate_csrf(csrf_token)
            except Exception as csrf_error:
                logger.warning(f"CSRF validation failed: {csrf_error}")
                flash('Sikkerhetsfeil: Vennligst prøv igjen.', 'error')
                return render_template('price_alerts/create.html')
            
            # Get form data with validation
            symbol = request.form.get('symbol', '').upper().strip()
            target_price_str = request.form.get('target_price', '').strip()
            alert_type = request.form.get('alert_type', 'above') or 'above'
            company_name = request.form.get('company_name', '').strip()
            notes = request.form.get('notes', '').strip()
            
            logger.info(f"Creating price alert for user {current_user.id}: {symbol} at {target_price_str}")
            
            # Enhanced validation
            if not symbol:
                flash('Aksjesymbol er påkrevd.', 'error')
                return render_template('price_alerts/create.html')
            
            if len(symbol) > 10:
                flash('Aksjesymbol er for langt.', 'error')
                return render_template('price_alerts/create.html')
            
            # Parse and validate target price
            try:
                target_price = float(target_price_str.replace(',', '.'))
                if target_price <= 0:
                    raise ValueError("Målpris må være større enn 0")
                if target_price > 1000000:
                    raise ValueError("Målpris er for høy")
            except (ValueError, TypeError) as e:
                flash(f'Ugyldig målpris: {str(e)}. Vennligst skriv inn et gyldig tall.', 'error')
                return render_template('price_alerts/create.html')
            
            if alert_type not in ['above', 'below']:
                flash('Ugyldig varseltype.', 'error')
                return render_template('price_alerts/create.html')
            
            # Check subscription limits with better error handling
            try:
                if not getattr(current_user, 'has_subscription', False):
                    from ..models.price_alert import PriceAlert
                    active_count = PriceAlert.query.filter_by(
                        user_id=current_user.id, 
                        is_active=True
                    ).count()
                    
                    if active_count >= 3:
                        flash('Du har nådd grensen for gratis prisvarsler (3 aktive). Oppgrader til Pro for ubegrenset tilgang.', 'warning')
                        return render_template('price_alerts/create.html')
            except Exception as e:
                logger.warning(f"Could not check subscription limits: {e}")
                # Continue anyway for better user experience
            
            # Enhanced alert creation with simplified, working approach + granular error reporting
            try:
                # Use centralized alert_service
                browser_enabled_raw = request.form.get('browser_enabled')
                browser_enabled_flag = browser_enabled_raw in ['on', 'true', '1', 'True']
                try:
                    svc_create_alert(
                        current_user.id,
                        symbol,
                        alert_type,
                        target_price,
                        email_enabled=True,
                        browser_enabled=browser_enabled_flag,
                        notes=notes or company_name
                    )
                    flash(f'✅ Prisvarsel opprettet for {symbol} ved {target_price} NOK!', 'success')
                except Exception as svc_err:
                    logger.error(f"alert_service create failed: {svc_err}")
                    flash('❌ Kunne ikke opprette prisvarsel (tjenestefeil).', 'error')
                    return render_template('price_alerts/create.html')
                return redirect(url_for('price_alerts.index'))

            except Exception as e:
                logger.error(f"Error creating price alert: {e}")
                db.session.rollback()
                tech_msg = str(e)
                if 'browser_enabled' in tech_msg:
                    flash('❌ Kolonnen browser_enabled mangler i databasen – kjør migrasjon eller oppdater tabellen.', 'error')
                elif 'UNIQUE' in tech_msg or 'unique constraint' in tech_msg.lower():
                    flash('❌ Du har allerede et aktivt prisvarsel for dette symbolet.', 'error')
                else:
                    flash('❌ Kunne ikke opprette prisvarsel. Teknisk feil - kontakt support hvis problemet vedvarer.', 'error')
                return render_template('price_alerts/create.html')
                
        except Exception as e:
            logger.error(f"Unexpected error in alert creation: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            flash('❌ Uventet feil ved opprettelse av prisvarsel.', 'error')
            return render_template('price_alerts/create.html')
    
    # GET request - show the form
    return render_template('price_alerts/create.html')

@price_alerts.route('/delete/<int:alert_id>', methods=['POST'])
@access_required
def delete(alert_id):
    """Delete a price alert"""
    try:
        if svc_delete_alert(current_user.id, alert_id):
            flash('Prisvarsel slettet.', 'success')
        else:
            flash('Kunne ikke slette prisvarsel.', 'error')
    except Exception as e:
        logger.error(f"Error deleting alert {alert_id}: {e}")
        flash('Feil ved sletting av prisvarsel.', 'error')
    
    return redirect(url_for('price_alerts.index'))

@price_alerts.route('/settings', methods=['GET', 'POST'])
@access_required
def settings():
    """Manage alert notification settings with enhanced error handling"""
    if request.method == 'POST':
        try:
            settings_data = {
                'email_enabled': request.form.get('email_enabled') == 'on',
                'email_instant': request.form.get('email_instant') == 'on',
                'email_daily_summary': request.form.get('email_daily_summary') == 'on',
                'language': request.form.get('language', 'no')
            }
            
            success = price_monitor.update_alert_settings(current_user.id, settings_data)
            if success:
                flash('Innstillinger oppdatert.', 'success')
            else:
                flash('Kunne ikke oppdatere innstillinger.', 'error')
                
        except Exception as e:
            logger.error(f"Error updating alert settings: {e}")
            flash('Feil ved oppdatering av innstillinger.', 'error')
        
        return redirect(url_for('price_alerts.settings'))
    
    # GET request
    try:
        settings = AlertNotificationSettings.get_or_create_for_user(current_user.id)
        return render_template('price_alerts/settings.html', settings=settings)
    except Exception as e:
        logger.error(f"Error loading alert settings: {e}")
        flash('Kunne ikke laste innstillinger.', 'error')
        return redirect(url_for('price_alerts.index'))

# API Endpoints
@price_alerts.route('/api/alerts')
@access_required
def api_get_alerts():
    """API endpoint to get user alerts"""
    try:
        alerts = list_user_alerts(current_user.id)
        return jsonify({
            'success': True,
            'alerts': alerts,
            'count': len(alerts)
        })
    except Exception as e:
        logger.error(f"Error in API get alerts: {e}")
        return jsonify({
            'success': False,
            'error': 'Could not load alerts'
        }), 500

@price_alerts.route('/api/create', methods=['POST'])
@access_required
def api_create_alert():
    """API endpoint to create alert"""
    try:
        data = request.get_json()
        
        alert_dict = svc_create_alert(
            current_user.id,
            data['symbol'],
            data['alert_type'],
            float(data['target_price']),
            email_enabled=True,
            browser_enabled=bool(data.get('browser_enabled', False)),
            notes=data.get('notes')
        )
        return jsonify({'success': True, 'alert': alert_dict, 'message': f"Alert created for {alert_dict.get('symbol')}"})
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error in API create alert: {e}")
        return jsonify({
            'success': False,
            'error': 'Could not create alert'
        }), 500

@price_alerts.route('/api/delete/<int:alert_id>', methods=['DELETE'])
@access_required
def api_delete_alert(alert_id):
    """API endpoint to delete alert"""
    try:
        if svc_delete_alert(current_user.id, alert_id):
            return jsonify({'success': True, 'message': 'Alert deleted'})
        return jsonify({'success': False, 'error': 'Alert not found'}), 404
            
    except Exception as e:
        logger.error(f"Error in API delete alert: {e}")
        return jsonify({
            'success': False,
            'error': 'Could not delete alert'
        }), 500

@price_alerts.route('/api/status')
@access_required
def api_service_status():
    """API endpoint to get monitoring service status"""
    try:
        status = price_monitor.get_service_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        logger.error(f"Error in API service status: {e}")
        return jsonify({
            'success': False,
            'error': 'Could not get service status'
        }), 500

@price_alerts.route('/api/quote/<symbol>')
@access_required
def api_get_quote(symbol):
    """API endpoint to get current quote for symbol"""
    try:
        if not DataService:
            return jsonify({
                'success': False,
                'error': 'Data service not available'
            }), 503
        
        quote_data = DataService.get_live_quote(symbol.upper())
        if quote_data:
            return jsonify({
                'success': True,
                'quote': quote_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Quote not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error getting quote for {symbol}: {e}")
        return jsonify({
            'success': False,
            'error': 'Could not get quote'
        }), 500
