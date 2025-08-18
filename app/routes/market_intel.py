"""
Market Intelligence Routes - for insider trading, institutional ownership, and market data
"""
import logging
from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..utils.access_control import access_required, demo_access

# Import service here to avoid issues
try:
    from ..services.external_apis import ExternalAPIService
except ImportError as e:
    print(f"Warning: Could not import ExternalAPIService: {e}")
    ExternalAPIService = None

logger = logging.getLogger(__name__)
market_intel = Blueprint('market_intel', __name__, url_prefix='/market-intel')

def generate_demo_insider_data(ticker):
    """Generate realistic demo insider trading data for a specific ticker"""
    import random
    from datetime import datetime, timedelta
    
    # Generate 5-15 transactions for the last 3 months
    transactions = []
    num_transactions = random.randint(5, 15)
    
    # Ticker-specific insider data
    company_data = {
        'EQNR.OL': {
            'name': 'Equinor ASA',
            'insiders': [
                ('Anders Opedal', 'CEO'),
                ('Lars Christian Bacher', 'CFO'),
                ('Pål Eitrheim', 'EVP'),
                ('Al Cook', 'EVP Technology'),
                ('Irene Rummelhoff', 'EVP Marketing'),
                ('Geir Tungesvik', 'EVP Operations')
            ],
            'price_range': (250, 320)
        },
        'DNB.OL': {
            'name': 'DNB Bank ASA',
            'insiders': [
                ('Kjerstin Braathen', 'CEO'),
                ('Ottar Ertzeid', 'CFO'),
                ('Harald Serck-Hanssen', 'Chairman'),
                ('Ida Lerner', 'EVP'),
                ('Ingjerd Blekeli Spiten', 'EVP'),
                ('Thomas Midteide', 'EVP')
            ],
            'price_range': (180, 240)
        },
        'TEL.OL': {
            'name': 'Telenor ASA',
            'insiders': [
                ('Sigve Brekke', 'CEO'),
                ('Tone H. Bachke', 'CFO'),
                ('Gunn Wærsted', 'Chairman'),
                ('Ruza Sabanovic', 'EVP'),
                ('Amina Hodzic', 'EVP'),
                ('Abdulmajeed Alkhereiji', 'EVP')
            ],
            'price_range': (120, 160)
        },
        'NHY.OL': {
            'name': 'Norsk Hydro ASA',
            'insiders': [
                ('Hilde Merete Aasheim', 'CEO'),
                ('Pål Kildemo', 'CFO'),
                ('Dag Mejdell', 'Chairman'),
                ('Arvid Moss', 'EVP'),
                ('Eivind Kallevik', 'EVP'),
                ('Kjetil Ebbesberg', 'EVP')
            ],
            'price_range': (60, 85)
        },
        # Default for unknown tickers
        'DEFAULT': {
            'name': f'Company {ticker}',
            'insiders': [
                ('John Anderson', 'CEO'),
                ('Sarah Johnson', 'CFO'),
                ('Michael Brown', 'Chairman'),
                ('Emily Davis', 'EVP Operations'),
                ('Robert Wilson', 'EVP Technology'),
                ('Lisa Thompson', 'EVP Marketing')
            ],
            'price_range': (50, 200)
        }
    }
    
    # Get company-specific data or use default
    company_info = company_data.get(ticker, company_data['DEFAULT'])
    company_name = company_info['name']
    insiders = company_info['insiders']
    price_min, price_max = company_info['price_range']
    
    for i in range(num_transactions):
        days_back = random.randint(1, 90)
        transaction_date = datetime.now() - timedelta(days=days_back)
        
        insider_name, title = random.choice(insiders)
        transaction_type = random.choice(['Purchase', 'Sale', 'Sale', 'Purchase'])  # More sales than purchases
        shares = random.randint(1000, 50000)
        price = random.uniform(price_min, price_max)
        
        transactions.append({
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'insider_name': insider_name,
            'title': title,
            'transaction_type': transaction_type,
            'shares': shares,
            'price': round(price, 2),
            'value': round(shares * price, 2),
            'symbol': ticker,
            'company': company_name
        })
    
    # Sort by date (newest first)
    transactions.sort(key=lambda x: x['transaction_date'], reverse=True)
    return transactions

@market_intel.route('/')
@access_required
def index():
    """Market intelligence dashboard"""
    try:
        # Check if service is available
        if not ExternalAPIService:
            return render_template('market_intel/index.html',
                                 insider_data={},
                                 sector_performance={},
                                 earnings_calendar=[],
                                 crypto_fear_greed={},
                                 economic_indicators={},
                                 market_news=[],
                                 error="Ekstern data-service er ikke tilgjengelig.")
        
        # Get recent insider trading for popular stocks
        popular_tickers = ['EQNR.OL', 'DNB.OL', 'AAPL', 'MSFT', 'TSLA']
        insider_data = {}
        
        for ticker in popular_tickers[:3]:  # Limit to avoid API rate limits
            try:
                insider_data[ticker] = ExternalAPIService.get_insider_trading(ticker, limit=5) or []
            except:
                insider_data[ticker] = []
        
        # Get sector performance with fallback
        try:
            sector_performance = ExternalAPIService.get_sector_performance() or {}
        except:
            sector_performance = {}
        
        # Get earnings calendar with fallback
        try:
            earnings_calendar = ExternalAPIService.get_earnings_calendar(days_ahead=14) or []
        except:
            earnings_calendar = []
        
        # Get crypto fear & greed index with fallback
        try:
            crypto_fear_greed = ExternalAPIService.get_crypto_fear_greed_index() or {}
        except:
            crypto_fear_greed = {}
        
        # Get economic indicators with fallback
        try:
            economic_indicators = ExternalAPIService.get_economic_indicators() or {}
        except:
            economic_indicators = {}
        
        # Get market news with fallback
        try:
            market_news = ExternalAPIService.get_market_news(limit=10) or []
        except:
            market_news = []
        
        return render_template('market_intel/index.html',
                             insider_data=insider_data,
                             sector_performance=sector_performance,
                             earnings_calendar=earnings_calendar,
                             crypto_fear_greed=crypto_fear_greed,
                             economic_indicators=economic_indicators,
                             market_news=market_news)
    except Exception as e:
        print(f"Error in market_intel index: {e}")
        # Return basic template with empty data instead of error page
        return render_template('market_intel/index.html',
                             insider_data={},
                             sector_performance={},
                             earnings_calendar=[],
                             crypto_fear_greed={},
                             economic_indicators={},
                             market_news=[],
                             error="Kunne ikke hente alle markedsdata. Viser tilgjengelig informasjon.")

@market_intel.route('/insider-trading')
@demo_access
def insider_trading():
    """Redirect to the new insider trading page"""
    ticker = request.args.get('ticker', '').strip().upper()
    
    # Redirect to the new insider trading URL
    if ticker:
        return redirect(url_for('insider_trading.index', ticker=ticker), code=301)
    else:
        return redirect(url_for('insider_trading.index'), code=301)

@market_intel.route('/earnings-calendar')
@access_required
def earnings_calendar():
    """Earnings calendar page"""
    days_ahead = request.args.get('days', 30, type=int)
    
    try:
        earnings_data = ExternalAPIService.get_earnings_calendar(days_ahead=days_ahead)
        
        return render_template('market_intel/earnings_calendar.html',
                             earnings_data=earnings_data,
                             days_ahead=days_ahead)
    except Exception as e:
        return render_template('error.html', error="Kunne ikke hente resultatkalender.")

@market_intel.route('/sector-analysis')
@access_required
def sector_analysis():
    """Sector performance analysis"""
    try:
        sector_data = ExternalAPIService.get_sector_performance()
        screener_data = ExternalAPIService.get_stock_screener(
            market_cap_min=1000000000,  # 1B+ market cap
            volume_min=1000000          # 1M+ volume
        )
        
        return render_template('market_intel/sector_analysis.html',
                             sector_data=sector_data,
                             screener_data=screener_data[:20])  # Top 20
    except Exception as e:
        return render_template('error.html', error="Kunne ikke hente sektoranalyse.")

@market_intel.route('/economic-indicators')
@access_required
def economic_indicators():
    """Economic indicators and market overview"""
    try:
        economic_data = ExternalAPIService.get_economic_indicators()
        crypto_fear_greed = ExternalAPIService.get_crypto_fear_greed_index()
        
        return render_template('market_intel/economic_indicators.html',
                             economic_data=economic_data,
                             crypto_fear_greed=crypto_fear_greed)
    except Exception as e:
        return render_template('error.html', error="Kunne ikke hente økonomiske indikatorer.")

# API endpoints for AJAX requests
@market_intel.route('/api/insider-trading/<ticker>')
@access_required
def api_insider_trading(ticker):
    """API endpoint for insider trading data"""
    try:
        limit = request.args.get('limit', 10, type=int)
        data = ExternalAPIService.get_insider_trading(ticker, limit=limit)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/institutional-ownership/<ticker>')
@access_required
def api_institutional_ownership(ticker):
    """API endpoint for institutional ownership data"""
    try:
        data = ExternalAPIService.get_institutional_ownership(ticker)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/sector-performance')
@access_required
def api_sector_performance():
    """API endpoint for sector performance"""
    try:
        data = ExternalAPIService.get_sector_performance()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/earnings-calendar')
@access_required
def api_earnings_calendar():
    """API endpoint for earnings calendar"""
    try:
        days_ahead = request.args.get('days', 30, type=int)
        data = ExternalAPIService.get_earnings_calendar(days_ahead=days_ahead)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_intel.route('/api/crypto-fear-greed')
@access_required
def api_crypto_fear_greed():
    """API endpoint for crypto fear & greed index"""
    try:
        data = ExternalAPIService.get_crypto_fear_greed_index()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
