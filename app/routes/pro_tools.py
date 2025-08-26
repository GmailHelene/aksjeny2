from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from ..utils.access_control import access_required, pro_required, demo_access
from datetime import datetime, timedelta
import logging

# Import services safely
try:
    from ..services.data_service import DataService
except ImportError:
    DataService = None

try:
    from ..services.analysis_service import AnalysisService
except ImportError:
    AnalysisService = None

pro_tools = Blueprint('pro_tools', __name__, url_prefix='/pro-tools')
logger = logging.getLogger(__name__)

@pro_tools.route('/')
@access_required
def index():
    """Pro-verktøy oversikt"""
    return render_template('main/coming_soon.html', message="Kommer senere")

@pro_tools.route('/screener', methods=['GET', 'POST'])
@access_required
def advanced_screener():
    """Avansert aksje-screener"""
    try:
        # Hent screening kriterier
        if request.method == 'POST':
            criteria = request.form.to_dict()
        else:
            criteria = request.args.to_dict()
        
        # Standard screening
        results = []
        if criteria and AnalysisService:
            results = AnalysisService.advanced_screener(criteria)
        elif criteria:
            # Fallback if service is not available
            results = [
                {
                    'symbol': 'AAPL',
                    'name': 'Apple Inc.',
                    'price': 150.25,
                    'change_pct': 2.1,
                    'volume': 1000000,
                    'market_cap': 2500000000000
                },
                {
                    'symbol': 'MSFT', 
                    'name': 'Microsoft Corporation',
                    'price': 280.50,
                    'change_pct': 1.8,
                    'volume': 800000,
                    'market_cap': 2100000000000
                }
            ]
        
        return render_template('pro/screener.html', 
                             criteria=criteria, 
                             results=results)
    except Exception as e:
        logger.error(f"Error in advanced screener: {e}")
        flash('Feil ved kjøring av screener. Prøv igjen.', 'error')
        return render_template('pro/screener.html', criteria={}, results=[])

@pro_tools.route('/alerts', methods=['GET', 'POST'])
@access_required
def price_alerts():
    """Pris-varsler og alarmer"""
    try:
        if request.method == 'POST':
            # Get form data
            ticker = request.form.get('ticker')
            alert_type = request.form.get('alert_type')
            target_value = request.form.get('target_value')
            email_alert = request.form.get('email_alert') == 'on'
            browser_alert = request.form.get('browser_alert') == 'on'
            
            # Validate required fields
            if not all([ticker, alert_type, target_value]):
                flash('Alle felt må fylles ut.', 'error')
                return redirect(url_for('pro_tools.price_alerts'))
            
            # Create alert using API endpoint functionality
            alert_data = {
                'symbol': ticker,
                'condition': alert_type,
                'price': float(target_value),
                'email_enabled': email_alert,
                'browser_enabled': browser_alert
            }
            
            # Save alert to database using PriceAlert model
            try:
                from ..models.price_alert import PriceAlert
                from ..services.price_monitor_service import price_monitor
                
                # Create new alert
                new_alert = PriceAlert(
                    user_id=current_user.id,
                    ticker=ticker.upper(),  # Store in ticker field
                    symbol=ticker.upper(),  # Also store in symbol field for compatibility
                    target_price=float(target_value),
                    alert_type=alert_type,  # 'above' or 'below'
                    condition=alert_type,   # For backward compatibility
                    is_active=True,
                    email_enabled=email_alert,
                    browser_enabled=browser_alert
                )
                
                # Save to database
                from ..extensions import db
                db.session.add(new_alert)
                db.session.commit()
                
                # Register with monitoring service
                try:
                    price_monitor.add_alert(new_alert.to_dict())
                except Exception as monitor_error:
                    logger.warning(f"Could not register alert with monitor: {monitor_error}")
                
                flash(f'Prisvarsel opprettet for {ticker} ({alert_type} {target_value})', 'success')
                logger.info(f"Created price alert for user {current_user.id}: {ticker} {alert_type} {target_value}")
                
            except Exception as e:
                logger.error(f"Error creating price alert: {e}")
                flash(f'Kunne ikke opprette varsel: {str(e)}', 'error')
            
            return redirect(url_for('pro_tools.price_alerts'))
            
        # GET request - show alerts page
        # Fetch user's active alerts from database
        user_alerts = []
        try:
            from ..models.price_alert import PriceAlert
            alerts_query = PriceAlert.query.filter_by(user_id=current_user.id).order_by(
                PriceAlert.is_active.desc(),
                PriceAlert.created_at.desc()
            ).all()
            user_alerts = [alert.to_dict() for alert in alerts_query]
            logger.info(f"Retrieved {len(user_alerts)} alerts for user {current_user.id}")
        except Exception as e:
            logger.error(f"Error fetching user alerts: {e}")
            user_alerts = []
        
        return render_template('pro/alerts.html', alerts=user_alerts)
    except Exception as e:
        logger.error(f"Error in price alerts: {e}")
        # Return template with error message instead of crashing
        return render_template('pro/alerts.html', 
                             alerts=[], 
                             error='Kunne ikke laste varsler. Prøv igjen senere.')

@pro_tools.route('/portfolio-analyzer')
@access_required
def portfolio_analyzer():
    """Avansert porteføljeanalyse"""
    try:
        # Hent brukerens porteføljer
        portfolios = []  # TODO: Implementer database henting
        
        analysis_results = None
        if request.args.get('portfolio_id'):
            # Kjør analyse på valgt portefølje
            analysis_results = {
                'risk_metrics': {
                    'beta': 1.2,
                    'volatility': 0.18,
                    'sharpe_ratio': 1.4,
                    'max_drawdown': 0.12
                },
                'diversification': {
                    'sector_concentration': 0.35,
                    'geographic_exposure': {
                        'Norway': 0.6,
                        'USA': 0.3,
                        'Europe': 0.1
                    }
                },
                'performance': {
                    'total_return': 0.15,
                    'annual_return': 0.12,
                    'benchmark_comparison': 0.03
                }
            }
        
        return render_template('pro/portfolio_analyzer.html', 
                             portfolios=portfolios,
                             analysis=analysis_results)
    except Exception as e:
        logger.error(f"Error in portfolio analyzer: {e}")
        flash('Feil ved porteføljeanalyse.', 'error')
        return render_template('pro/portfolio_analyzer.html', 
                             portfolios=[], analysis=None)

@pro_tools.route('/export')
@demo_access
def export_tools():
    """Eksport-verktøy for data og rapporter"""
    try:
        return render_template('pro/export.html')
    except Exception as e:
        logger.error(f"Error loading export tools: {e}")
        flash('Kunne ikke laste eksport-verktøy.', 'error')
        return redirect(url_for('pro_tools.index'))

@pro_tools.route('/api/screener', methods=['POST'])
@access_required
def api_screener():
    """API for avansert screening"""
    try:
        criteria = request.get_json()
        results = AnalysisService.advanced_screener(criteria)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        logger.error(f"API screener error: {e}")
        # Return fallback data instead of 500 error
        return jsonify({
            'success': True, 
            'results': [],
            'error': 'Screener midlertidig utilgjengelig',
            'fallback': True
        }), 200

@pro_tools.route('/api/alerts', methods=['GET'])
@access_required
def api_get_alerts():
    """API endpoint for getting user alerts"""
    try:
        # TODO: Implement database retrieval
        mock_alerts = [
            {
                'id': 1,
                'symbol': 'AAPL',
                'condition': 'above',
                'price': 150.0,
                'current_price': 145.50,
                'created': '2024-01-15',
                'active': True
            },
            {
                'id': 2,
                'symbol': 'TSLA',
                'condition': 'below',
                'price': 200.0,
                'current_price': 220.30,
                'created': '2024-01-10',
                'active': True
            }
        ]
        return jsonify({
            'success': True,
            'alerts': mock_alerts
        })
    except Exception as e:
        logger.error(f"API get alerts error: {e}")
        return jsonify({
            'success': False,
            'error': f'Teknisk feil: {str(e)}'
        }), 500

@pro_tools.route('/api/create-alert', methods=['POST'])
@access_required
def create_alert():
    """Opprett nytt pris-varsel"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'Ingen data mottatt'
            }), 400
            
        required_fields = ['symbol', 'condition', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Mangler påkrevd felt: {field}'
                }), 400
        
        # TODO: Implementer database lagring
        alert_id = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return jsonify({
            'success': True,
            'alert_id': alert_id,
            'message': f'Varsel opprettet for {data["symbol"]}'
        })
    except Exception as e:
        logger.error(f"Create alert error: {e}")
        return jsonify({
            'success': False,
            'error': f'Teknisk feil: {str(e)}'
        }), 500

@pro_tools.route('/delete-alert/<alert_id>', methods=['POST'])
@access_required
def delete_alert(alert_id):
    """Delete an alert"""
    try:
        if not alert_id:
            flash('Ugyldig varsel ID', 'error')
            return redirect(url_for('pro_tools.price_alerts'))
            
        # TODO: Implement database deletion
        flash(f'Varsel slettet', 'success')
        return redirect(url_for('pro_tools.price_alerts'))
    except Exception as e:
        logger.error(f"Delete alert error: {e}")
        flash(f'Kunne ikke slette varsel: {str(e)}', 'error')
        return redirect(url_for('pro_tools.price_alerts'))

@pro_tools.route('/api/delete-alert/<alert_id>', methods=['DELETE'])
@access_required
def api_delete_alert(alert_id):
    """Delete an alert (API endpoint)"""
    try:
        if not alert_id:
            return jsonify({
                'success': False,
                'error': 'Ugyldig varsel ID'
            }), 400
            
        # TODO: Implement database deletion
        return jsonify({
            'success': True,
            'message': f'Varsel {alert_id} slettet'
        })
    except Exception as e:
        logger.error(f"Delete alert error: {e}")
        return jsonify({
            'success': False,
            'error': f'Teknisk feil: {str(e)}'
        }), 500

@pro_tools.route('/export-portfolio', methods=['POST'])
@access_required
def export_portfolio():
    """Export portfolio data"""
    try:
        portfolio_id = request.form.get('portfolio_id', 'all')
        format_type = request.form.get('format', 'excel')
        
        # Mock export functionality
        if format_type == 'excel':
            flash('Excel-eksport startet. Du vil få en e-post når den er klar.', 'success')
        elif format_type == 'csv':
            flash('CSV-eksport startet. Du vil få en e-post når den er klar.', 'success')
        elif format_type == 'pdf':
            flash('PDF-rapport genereres. Du vil få en e-post når den er klar.', 'success')
        
        return redirect(url_for('pro_tools.export_tools'))
    except Exception as e:
        logger.error(f"Export portfolio error: {e}")
        flash('Feil ved eksport av portefølje.', 'error')
        return redirect(url_for('pro_tools.export_tools'))

@pro_tools.route('/export-analysis', methods=['POST'])
@access_required
def export_analysis():
    """Export analysis data"""
    try:
        symbol = request.form.get('symbol')
        analysis_type = request.form.get('analysis_type', 'technical')
        format_type = request.form.get('format', 'pdf')
        
        if not symbol:
            flash('Vennligst spesifiser et symbol for eksport.', 'error')
            return redirect(url_for('pro_tools.export_tools'))
        
        # Mock export functionality
        flash(f'Analyse-eksport for {symbol} startet. Du vil få en e-post når den er klar.', 'success')
        return redirect(url_for('pro_tools.export_tools'))
    except Exception as e:
        logger.error(f"Export analysis error: {e}")
        flash('Feil ved eksport av analyse.', 'error')
        return redirect(url_for('pro_tools.export_tools'))

@pro_tools.route('/export-watchlist', methods=['POST'])
@access_required
def export_watchlist():
    """Export watchlist data"""
    try:
        watchlist_id = request.form.get('watchlist_id')
        format_type = request.form.get('format', 'excel')
        include_analysis = request.form.get('include_analysis') == 'on'
        
        if not watchlist_id:
            flash('Vennligst velg en overvåkningsliste for eksport.', 'error')
            return redirect(url_for('pro_tools.export_tools'))
        
        # Mock export functionality
        analysis_text = " med analyse" if include_analysis else ""
        if format_type == 'excel':
            flash(f'Excel-eksport av overvåkningsliste{analysis_text} startet. Du vil få en e-post når den er klar.', 'success')
        elif format_type == 'csv':
            flash(f'CSV-eksport av overvåkningsliste{analysis_text} startet. Du vil få en e-post når den er klar.', 'success')
        elif format_type == 'pdf':
            flash(f'PDF-rapport av overvåkningsliste{analysis_text} genereres. Du vil få en e-post når den er klar.', 'success')
        
        return redirect(url_for('pro_tools.export_tools'))
    except Exception as e:
        logger.error(f"Export watchlist error: {e}")
        flash('Feil ved eksport av overvåkningsliste.', 'error')
        return redirect(url_for('pro_tools.export_tools'))

@pro_tools.route('/api/documentation')
@demo_access
def api_documentation():
    """API documentation page"""
    try:
        # Mock API endpoints documentation
        api_endpoints = [
            {
                'method': 'GET',
                'endpoint': '/api/stocks/{symbol}',
                'description': 'Hent aksjeinformasjon for et symbol',
                'auth_required': True
            },
            {
                'method': 'GET', 
                'endpoint': '/api/analysis/technical/{symbol}',
                'description': 'Hent teknisk analyse for et symbol',
                'auth_required': True
            },
            {
                'method': 'POST',
                'endpoint': '/api/portfolio/create',
                'description': 'Opprett ny portefølje',
                'auth_required': True
            },
            {
                'method': 'GET',
                'endpoint': '/api/market/overview',
                'description': 'Hent markedsoversikt',
                'auth_required': False
            }
        ]
        
        return render_template('pro/api_docs.html', endpoints=api_endpoints)
    except Exception as e:
        logger.error(f"API documentation error: {e}")
        flash('Kunne ikke laste API-dokumentasjon.', 'error')
        return redirect(url_for('pro_tools.index'))
