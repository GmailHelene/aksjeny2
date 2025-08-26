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
    """Price alerts dashboard with enhanced error handling and fallback data"""
    try:
        # Get user's alerts with enhanced error handling
        user_alerts = []
        try:
            logger.info(f"Fetching alerts for user {current_user.id}")
            user_alerts = price_monitor.get_user_alerts(current_user.id)
            logger.info(f"Successfully retrieved {len(user_alerts)} alerts")
        except Exception as e:
            logger.error(f"Could not get user alerts: {e}")
            # Try direct database query as fallback
            try:
                from ..models.price_alert import PriceAlert
                alerts_query = PriceAlert.query.filter_by(user_id=current_user.id).order_by(
                    PriceAlert.is_active.desc(),
                    PriceAlert.created_at.desc()
                ).all()
                user_alerts = [alert.to_dict() for alert in alerts_query]
                logger.info(f"Fallback query retrieved {len(user_alerts)} alerts")
            except Exception as fallback_error:
                logger.error(f"Fallback query also failed: {fallback_error}")
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
    """Create new price alert with improved error handling"""
    if request.method == 'POST':
        try:
            # Get form data
            symbol = request.form.get('symbol', '').upper().strip()
            target_price_str = request.form.get('target_price', '').strip()
            alert_type = request.form.get('alert_type', 'above')
            company_name = request.form.get('company_name', '').strip()
            notes = request.form.get('notes', '').strip()
            
            # Validate input
            if not symbol:
                flash('Aksjesymbol er påkrevd.', 'error')
                return render_template('price_alerts/create.html')
            
            # Parse target price
            try:
                target_price = float(target_price_str)
                if target_price <= 0:
                    raise ValueError("Målpris må være større enn 0")
            except (ValueError, TypeError):
                flash('Ugyldig målpris. Vennligst skriv inn et gyldig tall.', 'error')
                return render_template('price_alerts/create.html')
            
            if alert_type not in ['above', 'below']:
                flash('Ugyldig varseltype.', 'error')
                return render_template('price_alerts/create.html')
            
            # Check subscription limits
            try:
                if not getattr(current_user, 'has_subscription', False):
                    from ..models.price_alert import PriceAlert
                    active_count = PriceAlert.query.filter_by(
                        user_id=current_user.id, 
                        is_active=True
                    ).count()
                    
                    if active_count >= 3:
                        flash('Du har nådd grensen for gratis prisvarsler. Oppgrader til Pro for ubegrenset tilgang.', 'warning')
                        return render_template('price_alerts/create.html')
            except Exception as e:
                logger.warning(f"Could not check subscription limits: {e}")
            
            # Create the alert with improved fallback handling
            try:
                # Try the price monitor service first
                alert = None
                try:
                    alert = price_monitor.create_alert(
                        user_id=current_user.id,
                        symbol=symbol,
                        target_price=target_price,
                        alert_type=alert_type,
                        company_name=company_name or None,
                        notes=notes or None
                    )
                except Exception as monitor_error:
                    logger.warning(f"Price monitor service failed: {monitor_error}")
                    alert = None
                
                # If price monitor failed, create alert directly with proper transaction handling
                if not alert:
                    try:
                        from ..models.price_alert import PriceAlert
                        from .. import db
                        
                        # Ensure we have a fresh session for the transaction
                        if db.session.is_active:
                            db.session.rollback()
                        
                        alert = PriceAlert(
                            user_id=current_user.id,
                            symbol=symbol,
                            target_price=target_price,
                            alert_type=alert_type,
                            company_name=company_name or f"Stock {symbol}",
                            notes=notes,
                            is_active=True
                        )
                        
                        db.session.add(alert)
                        db.session.flush()  # Flush before commit to catch any errors early
                        db.session.commit()
                        
                        logger.info(f"Created price alert directly for user {current_user.id}: {symbol} at {target_price}")
                        
                    except Exception as db_error:
                        logger.error(f"Direct database alert creation failed: {db_error}")
                        db.session.rollback()  # Ensure rollback on error
                        alert = None
                
                if alert:
                    flash(f'Prisvarsel opprettet for {symbol} ved {target_price}!', 'success')
                    return redirect(url_for('price_alerts.index'))
                else:
                    flash('Kunne ikke opprette prisvarsel. Prøv igjen.', 'error')
                    return render_template('price_alerts/create.html')
                    
            except ValueError as ve:
                flash(str(ve), 'error')
                return render_template('price_alerts/create.html')
            except Exception as e:
                logger.error(f"Error creating price alert: {e}")
                flash('Teknisk feil ved opprettelse av prisvarsel. Kontakt support hvis problemet vedvarer.', 'error')
                return render_template('price_alerts/create.html')
            
        except Exception as e:
            logger.error(f"Critical error in price alert creation: {e}")
            flash('En uventet feil oppsto. Vennligst prøv igjen.', 'error')
            return render_template('price_alerts/create.html')
    
    # GET request - show create form
    try:
        # Get popular stocks for suggestions with fallback
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
        
        # Fallback popular stocks if DataService failed
        if not popular_stocks:
            popular_stocks = [
                {'symbol': 'EQNR.OL', 'name': 'Equinor ASA', 'last_price': 278.50},
                {'symbol': 'DNB.OL', 'name': 'DNB Bank ASA', 'last_price': 215.20},
                {'symbol': 'TEL.OL', 'name': 'Telenor ASA', 'last_price': 145.80},
                {'symbol': 'MOWI.OL', 'name': 'Mowi ASA', 'last_price': 189.50},
                {'symbol': 'NHY.OL', 'name': 'Norsk Hydro ASA', 'last_price': 64.82},
                {'symbol': 'AAPL', 'name': 'Apple Inc.', 'last_price': 195.89},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'last_price': 140.93},
                {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'last_price': 384.52},
                {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'last_price': 248.50},
                {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'last_price': 485.20},
            ]
        
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
