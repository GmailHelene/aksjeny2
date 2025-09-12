from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from ..utils.access_control import access_required, pro_required, demo_access
from datetime import datetime, timedelta
import logging
from types import SimpleNamespace
import math

# Numerical libs (already project-wide dependencies)
try:
    import numpy as np  # type: ignore
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover - if unavailable we degrade gracefully
    np = None  # type: ignore
    pd = None  # type: ignore

# Import services safely
try:
    from ..services.data_service import DataService
except ImportError:
    DataService = None

try:
    # from ..services.analysis_service import AnalysisService
    AnalysisService = None  # Temporarily disabled
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
        from ..services.alert_service import list_user_alerts, create_alert as svc_create
        if request.method == 'POST':
            ticker = (request.form.get('ticker') or '').strip().upper()
            alert_type = request.form.get('alert_type') or 'above'
            target_value = request.form.get('target_value')
            email_alert = request.form.get('email_alert') == 'on'
            browser_alert = request.form.get('browser_alert') == 'on'
            if not (ticker and target_value):
                flash('Alle felt må fylles ut.', 'error')
                return redirect(url_for('pro_tools.price_alerts'))
            try:
                svc_create(current_user.id, ticker, alert_type, float(target_value), email_alert, browser_alert)
                flash(f'Prisvarsel opprettet for {ticker} ({alert_type} {target_value})', 'success')
            except Exception as e:
                logger.error(f"Create alert via service failed: {e}")
                flash(f'Kunne ikke opprette varsel: {e}', 'error')
            return redirect(url_for('pro_tools.price_alerts'))
        user_alerts = list_user_alerts(current_user.id)
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
    """Avansert porteføljeanalyse med reelle porteføljer og sikre fallbacks."""
    try:
        from ..models.portfolio import Portfolio
        # Hent porteføljer (utelat watchlister)
        try:
            portfolios = Portfolio.query.filter_by(user_id=current_user.id, is_watchlist=False).order_by(Portfolio.created_at.asc()).all()
        except Exception as q_err:
            logger.error(f"Feil ved henting av porteføljer: {q_err}")
            portfolios = []

        analysis = None
        portfolio_id = request.args.get('portfolio_id')
        selected_portfolio = None
        if portfolio_id:
            try:
                selected_portfolio = Portfolio.query.filter_by(id=portfolio_id, user_id=current_user.id).first()
            except Exception as sel_err:
                logger.error(f"Feil ved henting av valgt portefølje: {sel_err}")
                selected_portfolio = None

        if selected_portfolio:
            # 1. Grunnleggende verdier og allokasjon
            try:
                total_value = selected_portfolio.calculate_total_value()
            except Exception:
                total_value = 0.0
            try:
                allocation_raw = selected_portfolio.get_stock_allocation()
            except Exception:
                allocation_raw = []

            holdings = []
            # Pre-calc weights as fraction (not percentage)
            for alloc in allocation_raw:
                ticker = alloc['ticker']
                value = alloc.get('value', 0.0)
                weight_pct = alloc.get('percentage', 0.0)
                weight_fraction = (weight_pct / 100.0) if weight_pct else 0.0
                try:
                    stock_obj = selected_portfolio.stocks.filter_by(ticker=ticker).first()
                    ret_pct = stock_obj.calculate_return() if stock_obj else 0.0
                except Exception:
                    ret_pct = 0.0
                holdings.append({
                    'ticker': ticker,
                    'name': ticker,
                    'weight': weight_pct,      # keep original percentage for UI
                    'weight_fraction': weight_fraction,
                    'value': value,
                    'return': ret_pct,
                    'spread': None,            # real spread not implemented yet
                    'risk_contribution': 0.0   # placeholder until computed
                })

            # Default metrics
            total_return_pct = selected_portfolio.return_percentage or 0.0
            volatility = 0.0
            sharpe_ratio = 0.0
            beta = 0.0
            var_95 = 0.0
            correlation = 0.0
            benchmark_symbol = '^GSPC'  # S&P 500 som benchmark
            risk_free_rate = 0.02

            # 2. Hent historiske priser hvis mulig
            historical_closes = {}
            min_length_required = 30  # minimum dager for meningsfull beregning
            end_date = datetime.utcnow().date()
            start_date = end_date - timedelta(days=180)

            def fetch_history(ticker: str):
                """Returnerer DataFrame med 'Date' index og 'Close' kolonne."""
                # Forsøk DataService først hvis API eksisterer med samme signatur (period/interval)
                df = None
                if DataService and hasattr(DataService, 'get_historical_data'):
                    try:
                        # DataService variant bruker (symbol, period, interval)
                        df = DataService.get_historical_data(ticker, period='6mo', interval='1d')  # type: ignore
                    except Exception:
                        df = None
                if (df is None or getattr(df, 'empty', True)) and 'YahooFinanceService' in globals():
                    try:  # type: ignore
                        from ..services.yahoo_finance_service import YahooFinanceService
                        df2 = YahooFinanceService.get_historical_data(ticker, start_date.isoformat(), end_date.isoformat())
                        if df2 is not None and not df2.empty:
                            df = df2
                    except Exception:
                        pass
                return df

            if pd is not None and np is not None and holdings:
                price_frames = []
                tickers_for_calc = []
                for h in holdings:
                    t = h['ticker']
                    df = fetch_history(t)
                    if df is not None and not df.empty:
                        # Normalize columns (yfinance returns 'Close')
                        if 'Close' in df.columns:
                            series = df['Close'].copy()
                        elif 'close' in df.columns:
                            series = df['close'].copy()
                        else:
                            continue
                        series.name = t
                        price_frames.append(series)
                        tickers_for_calc.append(t)
                if len(price_frames) >= 1:
                    try:
                        prices_df = pd.concat(price_frames, axis=1).dropna(how='all')
                        # Daglige log- eller prosent avkastninger
                        returns_df = prices_df.pct_change().dropna(how='any')
                        if len(returns_df) >= min_length_required:
                            # Map weights to fraction
                            weight_map = {h['ticker']: h['weight_fraction'] for h in holdings if h['weight_fraction'] > 0}
                            # Re-normalize weights to sum 1 for included tickers
                            total_w = sum(weight_map.values())
                            if total_w > 0:
                                for k in list(weight_map.keys()):
                                    weight_map[k] = weight_map[k] / total_w
                            # Align returns to weight map
                            available = [t for t in returns_df.columns if t in weight_map]
                            if available:
                                weights_vec = np.array([weight_map[t] for t in available], dtype=float)
                                sub_returns = returns_df[available].to_numpy(dtype=float)
                                portfolio_returns = np.dot(sub_returns, weights_vec)
                                # Annualiseringsfaktor
                                trading_days = 252
                                mean_daily = float(np.mean(portfolio_returns))
                                std_daily = float(np.std(portfolio_returns))
                                volatility = std_daily * math.sqrt(trading_days)
                                if volatility > 0:
                                    sharpe_ratio = ((mean_daily * trading_days) - risk_free_rate) / volatility
                                # Historisk VaR (95%) – positiv verdi som representerer forventet tapsgrense
                                try:
                                    var_raw = np.percentile(portfolio_returns, 5)
                                    var_95 = -float(var_raw)
                                except Exception:
                                    var_95 = 0.0
                                # Beta & korrelasjon mot benchmark
                                try:
                                    bench_df = fetch_history(benchmark_symbol)
                                    if bench_df is not None and not bench_df.empty:
                                        bench_prices = bench_df['Close'] if 'Close' in bench_df.columns else None
                                        if bench_prices is not None:
                                            bench_returns = bench_prices.pct_change().dropna()
                                            # Align index
                                            pr_series = pd.Series(portfolio_returns, index=returns_df.index)
                                            merged = pd.concat([pr_series, bench_returns], axis=1, join='inner')
                                            merged.columns = ['portfolio', 'benchmark']
                                            if len(merged) >= min_length_required:
                                                cov = np.cov(merged['portfolio'], merged['benchmark'])[0][1]
                                                var_b = np.var(merged['benchmark'])
                                                if var_b > 0:
                                                    beta = float(cov / var_b)
                                                correlation = float(merged.corr().iloc[0,1])
                                except Exception:
                                    beta = beta or 0.0
                                # Risk contributions (approx = weight * asset_std / portfolio_std)
                                try:
                                    asset_stds = returns_df[available].std().to_dict()
                                    if std_daily > 0:
                                        for h in holdings:
                                            t = h['ticker']
                                            if t in asset_stds and t in weight_map:
                                                contrib = (weight_map[t] * asset_stds[t]) / std_daily
                                                h['risk_contribution'] = round(float(contrib * 100), 2)  # prosent av total risiko
                                except Exception:
                                    pass
                    except Exception as calc_err:
                        logger.warning(f"Kunne ikke beregne avanserte risikometrics: {calc_err}")

            # 3. Sektorfordeling
            sector_totals = {}
            if DataService:
                for h in holdings:
                    try:
                        info = DataService.get_stock_info(h['ticker'])
                        sector = info.get('sector', 'Ukjent') if info else 'Ukjent'
                    except Exception:
                        sector = 'Ukjent'
                    sector_totals.setdefault(sector, 0.0)
                    sector_totals[sector] += h.get('value', 0.0)
                    h['sector'] = sector
            # Konverter sektorfordeling til labels/data
            sector_labels = []
            sector_data = []
            if total_value > 0 and sector_totals:
                for sec, val in sector_totals.items():
                    sector_labels.append(sec)
                    sector_data.append(round((val / total_value) * 100.0, 2))

            # 4. Over-/undervekt
            allocation_labels = [h['ticker'] for h in holdings]
            allocation_data = [round(h['weight'], 2) for h in holdings]
            overweight_stock = 'N/A'
            overweight_percentage = 0.0
            if allocation_data:
                mx_idx = int(np.argmax(allocation_data)) if np and allocation_data else 0
                overweight_stock = allocation_labels[mx_idx]
                overweight_percentage = allocation_data[mx_idx]
            underweight_sector = 'N/A'
            if sector_data:
                # Finn laveste sektorvekt > 0
                min_idx = int(np.argmin(sector_data)) if np else 0
                underweight_sector = sector_labels[min_idx]

            analysis = SimpleNamespace(
                total_value=total_value,
                currency=getattr(selected_portfolio, 'currency', 'NOK'),
                total_return=total_return_pct,
                sharpe_ratio=round(sharpe_ratio, 3) if sharpe_ratio else 0.0,
                volatility=round(volatility, 3) if volatility else 0.0,
                var_95=round(var_95, 4) if var_95 else 0.0,
                beta=round(beta, 3) if beta else 0.0,
                correlation=round(correlation, 3) if correlation else 0.0,
                holdings=holdings,
                overweight_stock=overweight_stock,
                overweight_percentage=overweight_percentage,
                underweight_sector=underweight_sector,
                allocation_labels=allocation_labels,
                allocation_data=allocation_data,
                sector_labels=sector_labels,
                sector_data=sector_data
            )

        return render_template('pro/portfolio_analyzer.html', portfolios=portfolios, analysis=analysis)
    except Exception as e:
        logger.error(f"Error in portfolio analyzer: {e}")
        flash('Feil ved porteføljeanalyse.', 'error')
        return render_template('pro/portfolio_analyzer.html', portfolios=[], analysis=None)

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
    """Hent brukerens prisvarsler fra databasen."""
    try:
        from ..services.alert_service import list_user_alerts
        alerts = list_user_alerts(current_user.id)
        return jsonify({'success': True, 'alerts': alerts, 'count': len(alerts)})
    except Exception as e:
        logger.error(f"API get alerts error: {e}")
        return jsonify({'success': False, 'error': 'Kunne ikke hente varsler'}), 500

@pro_tools.route('/api/create-alert', methods=['POST'])
@access_required
def create_alert():
    """Opprett nytt pris-varsel (DB)."""
    try:
        data = request.get_json() or {}
        required = ['symbol', 'condition', 'price']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({'success': False, 'error': 'Mangler felt: ' + ', '.join(missing)}), 400
        from ..services.alert_service import create_alert as svc_create
        alert = svc_create(
            current_user.id,
            data['symbol'],
            data['condition'],
            float(data['price']),
            bool(data.get('email_enabled', True)),
            bool(data.get('browser_enabled', False)),
            data.get('notes')
        )
        return jsonify({'success': True, 'alert': alert, 'message': f"Varsel opprettet for {alert.get('symbol')}"})
    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)}), 400
    except Exception as e:
        logger.error(f"Create alert error: {e}")
        from ..extensions import db
        try:
            db.session.rollback()
        except Exception:
            pass
        return jsonify({'success': False, 'error': 'Teknisk feil ved opprettelse'}), 500

@pro_tools.route('/delete-alert/<alert_id>', methods=['POST'])
@access_required
def delete_alert(alert_id):
    """Slett prisvarsel (HTML)."""
    try:
        if not alert_id:
            flash('Ugyldig varsel ID', 'error')
            return redirect(url_for('pro_tools.price_alerts'))
        from ..models.price_alert import PriceAlert
        from ..extensions import db
        alert = PriceAlert.query.filter_by(id=alert_id, user_id=current_user.id).first()
        if not alert:
            flash('Varsel ikke funnet', 'error')
            return redirect(url_for('pro_tools.price_alerts'))
        db.session.delete(alert)
        db.session.commit()
        flash('Varsel slettet', 'success')
    except Exception as e:
        logger.error(f"Delete alert error: {e}")
        from ..extensions import db
        try:
            db.session.rollback()
        except Exception:
            pass
        flash('Kunne ikke slette varsel', 'error')
    return redirect(url_for('pro_tools.price_alerts'))

@pro_tools.route('/api/delete-alert/<alert_id>', methods=['DELETE'])
@access_required
def api_delete_alert(alert_id):
    """Slett prisvarsel (API)."""
    try:
        if not alert_id:
            return jsonify({'success': False, 'error': 'Ugyldig varsel ID'}), 400
        from ..services.alert_service import delete_alert as svc_delete
        if svc_delete(current_user.id, int(alert_id)):
            return jsonify({'success': True, 'message': f'Varsel {alert_id} slettet'})
        return jsonify({'success': False, 'error': 'Varsel ikke funnet'}), 404
    except Exception as e:
        logger.error(f"Delete alert error: {e}")
        from ..extensions import db
        try:
            db.session.rollback()
        except Exception:
            pass
        return jsonify({'success': False, 'error': 'Teknisk feil ved sletting'}), 500

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
            },
            {
                'method': 'GET',
                'endpoint': '/pro-tools/api/alerts',
                'description': 'List prisvarsler for innlogget bruker',
                'auth_required': True
            },
            {
                'method': 'POST',
                'endpoint': '/pro-tools/api/create-alert',
                'description': 'Opprett nytt prisvarsel',
                'auth_required': True
            },
            {
                'method': 'DELETE',
                'endpoint': '/pro-tools/api/delete-alert/{alert_id}',
                'description': 'Slett et prisvarsel',
                'auth_required': True
            }
        ]
        
        return render_template('pro/api_docs.html', endpoints=api_endpoints)
    except Exception as e:
        logger.error(f"API documentation error: {e}")
        flash('Kunne ikke laste API-dokumentasjon.', 'error')
        return redirect(url_for('pro_tools.index'))
