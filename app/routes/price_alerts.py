"""
Price Alerts Blueprint for managing user stock price alerts
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models.price_alert import PriceAlert, AlertNotificationSettings
from ..services.price_monitor_service import price_monitor
from ..services.data_service import DataService
from ..utils.access_control import access_required
import logging

logger = logging.getLogger(__name__)

price_alerts = Blueprint('price_alerts', __name__, url_prefix='/price-alerts')

@price_alerts.route('/')
@access_required
def index():
    """Price alerts dashboard with fallback data"""
    try:
        # Get user's alerts
        user_alerts = []
        try:
            user_alerts = price_monitor.get_user_alerts(current_user.id)
        except Exception as e:
            logger.warning(f"Could not get user alerts: {e}")
        
        # Get alert settings
        settings = None
        try:
            settings = AlertNotificationSettings.get_or_create_for_user(current_user.id)
        except Exception as e:
            logger.warning(f"Could not get user settings: {e}")
        
        # Get monitoring service status
        service_status = None
        try:
            service_status = price_monitor.get_service_status()
        except Exception as e:
            logger.warning(f"Could not get service status: {e}")
        
        # Check subscription status for alert limits
        has_subscription = getattr(current_user, 'has_subscription', False)
        active_alerts_count = len([a for a in user_alerts if a.get('is_active', False)])
        alert_limit_reached = not has_subscription and active_alerts_count >= 3
        
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
    """Create new price alert"""
    if request.method == 'POST':
        try:
            # Get form data
            symbol = request.form.get('symbol', '').upper().strip()
            target_price = float(request.form.get('target_price', 0))
            alert_type = request.form.get('alert_type', 'above')
            company_name = request.form.get('company_name', '').strip()
            notes = request.form.get('notes', '').strip()
            
            # Validate input
            if not symbol:
                flash('Aksjesymbol er påkrevd.', 'error')
                return redirect(request.url)
            
            if target_price <= 0:
                flash('Målpris må være større enn 0.', 'error')
                return redirect(request.url)
            
            if alert_type not in ['above', 'below']:
                flash('Ugyldig varseltype.', 'error')
                return redirect(request.url)
            
            # Create the alert
            alert = price_monitor.create_alert(
                user_id=current_user.id,
                symbol=symbol,
                target_price=target_price,
                alert_type=alert_type,
                company_name=company_name or None,
                notes=notes or None
            )
            
            flash(f'Prisvarsel opprettet for {symbol}!', 'success')
            return redirect(url_for('price_alerts.index'))
            
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(request.url)
        except Exception as e:
            logger.error(f"Error creating price alert: {e}")
            flash('Kunne ikke opprette prisvarsel. Prøv igjen.', 'error')
            return redirect(request.url)
    
    # GET request - show create form
    try:
        # Get popular stocks for suggestions
        popular_stocks = []
        if DataService:
            try:
                oslo_data = DataService.get_oslo_bors_overview()
                if oslo_data and isinstance(oslo_data, dict):
                    # Convert dict to list format for template
                    popular_stocks = [
                        {
                            'symbol': ticker,
                            'name': data.get('name', ticker),
                            'last_price': data.get('last_price', 0)
                        }
                        for ticker, data in list(oslo_data.items())[:10]  # Top 10
                    ]
            except Exception as e:
                logger.warning(f"Could not load popular stocks: {e}")
                pass
        
        return render_template('price_alerts/create.html',
                             popular_stocks=popular_stocks)
                             
    except Exception as e:
        logger.error(f"Error loading create alert form: {e}")
        flash('Kunne ikke laste skjema. Prøv igjen senere.', 'error')
        return redirect(url_for('price_alerts.index'))

@price_alerts.route('/delete/<int:alert_id>', methods=['POST'])
@access_required
def delete(alert_id):
    """Delete a price alert"""
    try:
        success = price_monitor.delete_alert(alert_id, current_user.id)
        if success:
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
    """Manage alert notification settings"""
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
        alerts = price_monitor.get_user_alerts(current_user.id)
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
        
        alert = price_monitor.create_alert(
            user_id=current_user.id,
            symbol=data['symbol'],
            target_price=float(data['target_price']),
            alert_type=data['alert_type'],
            company_name=data.get('company_name'),
            notes=data.get('notes')
        )
        
        return jsonify({
            'success': True,
            'alert': alert.to_dict(),
            'message': f'Alert created for {alert.symbol}'
        })
        
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
        success = price_monitor.delete_alert(alert_id, current_user.id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Alert deleted'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
            
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
