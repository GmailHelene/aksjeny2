from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from ..services.data_service import DataService
from ..services.analysis_service import AnalysisService
from ..utils.access_control import access_required, pro_required, demo_access
from datetime import datetime, timedelta
import logging

pro_tools = Blueprint('pro_tools', __name__, url_prefix='/pro-tools')
logger = logging.getLogger(__name__)

@pro_tools.route('/')
@access_required
def index():
    """Pro-verktøy oversikt"""
    return render_template('main/coming_soon.html', message="Kommer senere")

@pro_tools.route('/screener')
@access_required
def advanced_screener():
    """Avansert aksje-screener"""
    try:
        # Hent screening kriterier
        criteria = request.args.to_dict()
        
        # Standard screening
        results = []
        if criteria:
            results = AnalysisService.advanced_screener(criteria)
        
        return render_template('pro/screener.html', 
                             criteria=criteria, 
                             results=results)
    except Exception as e:
        logger.error(f"Error in advanced screener: {e}")
        flash('Feil ved kjøring av screener. Prøv igjen.', 'error')
        return render_template('pro/screener.html', criteria={}, results=[])

@pro_tools.route('/alerts')
@access_required
def price_alerts():
    """Pris-varsler og alarmer"""
    try:
        # Hent brukerens aktive varsler
        user_alerts = []  # TODO: Implementer database henting
        
        return render_template('pro/alerts.html', alerts=user_alerts)
    except Exception as e:
        logger.error(f"Error loading alerts: {e}")
        flash('Kunne ikke laste varsler.', 'error')
        return render_template('pro/alerts.html', alerts=[])

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
        return jsonify({'success': False, 'error': str(e)}), 500

@pro_tools.route('/api/create-alert', methods=['POST'])
@access_required
def create_alert():
    """Opprett nytt pris-varsel"""
    try:
        data = request.get_json()
        # TODO: Implementer database lagring
        return jsonify({'success': True, 'alert_id': 'mock_id'})
    except Exception as e:
        logger.error(f"Create alert error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

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
