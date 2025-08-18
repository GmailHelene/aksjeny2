from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, send_from_directory, session
from flask_login import current_user, login_required
from ..utils.access_control import access_required, demo_access, premium_required
from ..models.user import User
from ..models.portfolio import Portfolio, PortfolioStock
from ..extensions import cache
from datetime import datetime, timedelta
import logging
import requests
import traceback

# Safe imports for services that might not exist
try:
    from ..services.analysis_service import AnalysisService
except ImportError:
    AnalysisService = None

try:
    from ..services.advanced_technical_service import AdvancedTechnicalService
except ImportError:
    AdvancedTechnicalService = None

try:
    from ..services.ai_service import AIService
except ImportError:
    AIService = None

try:
    from ..services.data_service import DataService, OSLO_BORS_TICKERS, GLOBAL_TICKERS
except ImportError:
    DataService = None
    OSLO_BORS_TICKERS = ['EQNR.OL', 'DNB.OL', 'TEL.OL', 'YAR.OL', 'MOWI.OL']
    GLOBAL_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']

# Set up logger
logger = logging.getLogger(__name__)

analysis = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis.route('/')
@access_required
def index():
    """Analysis main page - prevent redirect loops"""
    try:
        # Use real market summary data
        market_summary = DataService.get_market_summary() if DataService and hasattr(DataService, 'get_market_summary') else {}
        return render_template('analysis/index.html',
                             page_title="Analyse",
                             market_summary=market_summary)
    except Exception as e:
        logger.error(f"Error in analysis index: {str(e)}")
        return render_template('error.html',
                             error="Analyse siden er midlertidig utilgjengelig. Prøv igjen senere.")

@analysis.route('/<symbol>')
@access_required
def stock_analysis(symbol):
    """Redirect /analysis/<symbol> to short analysis for better UX"""
    try:
        # Redirect to the correct analysis page
        return redirect(url_for('analysis.short_analysis', ticker=symbol))
    except Exception as e:
        logger.error(f"Error redirecting analysis for {symbol}: {str(e)}")
        # Fallback to short analysis
        return redirect(url_for('analysis.short_analysis', ticker=symbol))

@analysis.route('/technical', methods=['GET', 'POST'])
@analysis.route('/technical/', methods=['GET', 'POST'])
@access_required  # Changed from @demo_access to require subscription
def technical():
    """Advanced Technical analysis with comprehensive indicators and patterns"""
    try:
        symbol = request.args.get('symbol') or request.form.get('symbol')
        if not symbol or not symbol.strip():
            return render_template('analysis/technical.html',
                                 symbol='',
                                 show_search_prompt=True,
                                 error_message=None)
        symbol = symbol.strip().upper()
        try:
            # Use real technical data from DataService
            technical_data = DataService.get_technical_data(symbol) if DataService else None
            if technical_data:
                return render_template('analysis/technical.html',
                                     symbol=symbol,
                                     technical_data=technical_data,
                                     show_analysis=True)
            else:
                return render_template('analysis/technical.html',
                                     symbol=symbol,
                                     technical_data=None,
                                     show_analysis=False,
                                     error_message="Ingen teknisk data tilgjengelig for valgt symbol.")
        except Exception as e:
            logger.error(f"Error in technical analysis for {symbol}: {e}")
            return render_template('analysis/technical.html',
                                 symbol=symbol,
                                 technical_data=None,
                                 show_analysis=False,
                                 error_message="Teknisk analyse er midlertidig utilgjengelig.")
                                 
    except Exception as e:
        logger.error(f"Error in technical analysis: {e}")
        # Return fallback page
        return render_template('analysis/technical.html',
                             symbol=request.args.get('symbol', ''),
                             show_analysis=bool(request.args.get('symbol')),
                             error="Teknisk analyse er midlertidig utilgjengelig")

@analysis.route('/warren-buffett', methods=['GET', 'POST'])
@access_required  # Changed from @demo_access to require subscription
def warren_buffett():
    """Warren Buffett analysis with real market data"""
    ticker = request.args.get('ticker') or request.form.get('ticker')

    if ticker and request.method in ['GET', 'POST']:
        ticker = ticker.strip().upper()
        try:
            from ..services.buffett_analyzer import BuffettAnalyzer
            analysis_data = BuffettAnalyzer.analyze_stock(ticker)
            if analysis_data:
                return render_template('analysis/warren_buffett.html',
                                     analysis=analysis_data,
                                     ticker=ticker)
            else:
                return render_template('analysis/warren_buffett.html',
                                     analysis=None,
                                     ticker=ticker,
                                     error="Ingen Buffett-analyse tilgjengelig for valgt ticker.")
        except Exception as analyzer_error:
            logger.error(f"BuffettAnalyzer failed for {ticker}: {analyzer_error}")
            return render_template('analysis/warren_buffett.html',
                                 analysis=None,
                                 ticker=ticker,
                                 error="Feil ved visning av Buffett-analyse. Kontakt support.")

    # Show selection page
    try:
        oslo_stocks = {
            'EQNR.OL': {'name': 'Equinor ASA', 'last_price': 270.50, 'change_percent': 1.2},
            'DNB.OL': {'name': 'DNB Bank ASA', 'last_price': 185.20, 'change_percent': -0.8},
            'TEL.OL': {'name': 'Telenor ASA', 'last_price': 125.30, 'change_percent': 0.5},
            'YAR.OL': {'name': 'Yara International', 'last_price': 350.80, 'change_percent': 2.1},
            'MOWI.OL': {'name': 'Mowi ASA', 'last_price': 198.40, 'change_percent': -1.3}
        }
        global_stocks = {
            'AAPL': {'name': 'Apple Inc.', 'last_price': 185.00, 'change_percent': 0.9},
            'MSFT': {'name': 'Microsoft Corporation', 'last_price': 420.50, 'change_percent': 1.5},
            'GOOGL': {'name': 'Alphabet Inc.', 'last_price': 140.20, 'change_percent': -0.3},
            'TSLA': {'name': 'Tesla Inc.', 'last_price': 220.80, 'change_percent': 3.2},
            'AMZN': {'name': 'Amazon.com Inc.', 'last_price': 155.90, 'change_percent': 0.7}
        }

        return render_template('analysis/warren_buffett.html',
                              oslo_stocks=oslo_stocks,
                              global_stocks=global_stocks,
                              analysis=None)
    except Exception as e:
        logger.error(f"Error loading Buffett selection page: {e}")
        flash('Kunne ikke laste aksjeoversikt. Prøv igjen senere.', 'error')
        return render_template('analysis/warren_buffett.html',
                              oslo_stocks={},
                              global_stocks={},
                              analysis=None)

@analysis.route('/market-overview')
@analysis.route('/market_overview')
@access_required
def market_overview():
    """Market overview page with simplified error handling"""
    try:
        # Use real market overview data
        oslo_data = DataService.get_oslo_stocks() if DataService else {}
        global_data = DataService.get_global_stocks() if DataService else {}
        crypto_data = DataService.get_crypto_data() if DataService else {}
        currency_data = DataService.get_currency_overview() if DataService else {}
        market_summaries = DataService.get_market_summary() if DataService else {}
        return render_template('analysis/market_overview.html',
                             oslo_stocks=oslo_data,
                             global_stocks=global_data,
                             crypto_data=crypto_data,
                             currency=currency_data,
                             currency_data=currency_data,
                             market_summaries=market_summaries)
    except Exception as e:
        logger.error(f"Critical error in market overview: {e}", exc_info=True)
        return render_template('error.html',
                             error="Markedsoversikt er midlertidig utilgjengelig. Prøv igjen senere.")

@analysis.route('/sentiment')
@demo_access
def sentiment():
    """Market sentiment analysis"""
    try:
        selected_symbol = request.args.get('symbol', '').strip().upper()

        # Validate the selected symbol
        if selected_symbol and not selected_symbol.replace('.', '').replace('-', '').isalnum():
            flash('Ugyldig aksjesymbol. Vennligst prøv igjen.', 'warning')
            return redirect(url_for('analysis.sentiment'))

        sentiment_data = None
        error = None
        if selected_symbol:
            # Use real sentiment data if available, fallback if missing or None
            if DataService and hasattr(DataService, 'get_sentiment_data'):
                try:
                    sentiment_data = DataService.get_sentiment_data(selected_symbol)
                except Exception:
                    sentiment_data = None
            if not sentiment_data:
                sentiment_data = _generate_demo_sentiment_data(selected_symbol)
        return render_template(
            'analysis/sentiment.html',
            sentiment_data=sentiment_data or {},
            error=error,
            popular_stocks=['EQNR.OL', 'DNB.OL', 'MOWI.OL', 'TEL.OL', 'NHY.OL', 'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA'],
            selected_symbol=selected_symbol
        )
    except Exception as e:
        logger.error(f"Critical error in sentiment analysis: {e}")
        import traceback
        logger.error(f"Sentiment analysis traceback: {traceback.format_exc()}")
        return render_template(
            'error.html',
            error="Sentimentanalyse er midlertidig utilgjengelig. Prøv igjen senere.")

def _generate_demo_sentiment_data(symbol):
    """Generate consistent demo sentiment data for any symbol"""
    import random
    random.seed(hash(symbol) % 10000)  # Consistent data based on symbol
    
    base_score = 45 + random.randint(0, 20)  # Range 45-65
    
    return {
        'overall_score': base_score,
        'sentiment_label': 'Positiv' if base_score > 55 else 'Nøytral' if base_score > 45 else 'Negativ',
        'news_score': base_score + random.randint(-5, 5),
        'social_score': base_score + random.randint(-8, 8),
        'volume_trend': random.choice(['Økende', 'Stabil', 'Avtagende']),
        'market_sentiment': base_score,
        'fear_greed_index': random.randint(20, 80),
        'vix': 15.0 + random.random() * 20,
        'market_trend': 'bullish' if base_score > 55 else 'neutral' if base_score > 45 else 'bearish',
        'sentiment_reasons': [
            f'Positive nyheter om {symbol}',
            'Sterke fundamentale faktorer',
            'Økt institusjonell interesse'
        ] if base_score > 55 else [
            'Blandede signaler fra markedet',
            'Usikkerhet i sektoren'
        ],
        'indicators': _generate_sentiment_indicators(symbol),
        'recommendation': 'KJØP' if base_score > 60 else 'HOLD' if base_score > 50 else 'SELG',
        'news_sentiment_articles': _generate_news_articles(symbol),
        'history': _generate_sentiment_history(symbol)
    }

def _generate_sentiment_indicators(symbol):
    """Generate sentiment indicators based on the symbol"""
    import random
    
    # Create deterministic but seemingly random data based on symbol
    symbol_hash = sum(ord(c) for c in symbol)
    random.seed(symbol_hash)
    
    indicators = []
    indicator_types = [
        'RSI (14)', 'MACD', 'Stochastic Oscillator', 'Bollinger Bands',
        'Sentiment Score', 'Momentum', 'Volume Analysis', 'Moving Average (50)'
    ]
    
    # Generate 3-5 indicators
    num_indicators = random.randint(3, 5)
    selected_indicators = random.sample(indicator_types, num_indicators)
    
    for indicator_name in selected_indicators:
        # Value between 0.0 and 1.0, biased by the hash
        base_value = (symbol_hash % 100) / 100.0
        # Add some randomness while keeping it consistent for the same symbol
        value = max(0.1, min(0.9, base_value + random.uniform(-0.3, 0.3)))
        
        indicators.append({
            'name': indicator_name,
            'value': value
        })
    
    return indicators

def _generate_sentiment_recommendation(symbol):
    """Generate a sentiment-based recommendation"""
    import random
    
    # Create deterministic but seemingly random data based on symbol
    symbol_hash = sum(ord(c) for c in symbol)
    random.seed(symbol_hash)
    
    # Determine recommendation type based on hash
    recommendation_value = (symbol_hash % 10)
    
    if recommendation_value >= 7:
        rec_type = 'buy'
        action = 'Kjøp'
        reasoning_options = [
            f"Tekniske indikatorer viser positiv trend for {symbol}",
            f"Sterk markedssentiment og økende volum indikerer bullish momentum for {symbol}",
            f"Flere analytikere har oppgradert {symbol} til kjøp basert på positive forventninger"
        ]
    elif recommendation_value <= 2:
        rec_type = 'sell'
        action = 'Selg'
        reasoning_options = [
            f"Tekniske indikatorer tyder på negativ trend for {symbol}",
            f"Svak markedssentiment og avtagende volum indikerer bearish momentum for {symbol}",
            f"Flere analytikere har nedgradert {symbol} basert på svakere forventninger"
        ]
    else:
        rec_type = 'hold'
        action = 'Hold'
        reasoning_options = [
            f"Blandede signaler indikerer en avventende strategi for {symbol}",
            f"Nøytral markedssentiment og stabilt volum anbefaler hold for {symbol}",
            f"Analytikere er delte i sine anbefalinger, noe som indikerer en hold-strategi for {symbol}"
        ]
    
    # Select reasoning and confidence
    reasoning = random.choice(reasoning_options)
    confidence = random.uniform(0.6, 0.95)
    
    return {
        'type': rec_type,
        'action': action,
        'reasoning': reasoning,
        'confidence': confidence
    }

def _generate_news_articles(symbol):
    """Generate realistic-looking news articles related to the symbol"""
    import random
    from datetime import datetime, timedelta
    
    # Create deterministic but seemingly random data based on symbol
    symbol_hash = sum(ord(c) for c in symbol)
    random.seed(symbol_hash)
    
    # Company name (approximate from symbol)
    company_name = symbol.split('.')[0]
    if company_name == 'AAPL':
        company_name = 'Apple'
    elif company_name == 'MSFT':
        company_name = 'Microsoft'
    elif company_name == 'GOOGL':
        company_name = 'Google'
    elif company_name == 'TSLA':
        company_name = 'Tesla'
    elif company_name == 'NVDA':
        company_name = 'NVIDIA'
    elif company_name == 'EQNR':
        company_name = 'Equinor'
    elif company_name == 'DNB':
        company_name = 'DNB'
    elif company_name == 'TEL':
        company_name = 'Telenor'
    elif company_name == 'NHY':
        company_name = 'Norsk Hydro'
    elif company_name == 'MOWI':
        company_name = 'Mowi'
    
    # News templates
    positive_news = [
        {"title": f"{company_name} overgår forventningene med sterke kvartalstall", 
         "sentiment": "positive",
         "summary": f"{company_name} rapporterte i dag resultater som overgår analytikernes forventninger med sterk vekst i både inntekter og fortjeneste."},
        {"title": f"Analytikere oppgraderer {company_name} etter positive signaler", 
         "sentiment": "positive",
         "summary": f"Flere analytikere har oppgradert sine anbefalinger for {company_name} etter positive signaler fra selskapet og markedet."},
        {"title": f"{company_name} annonserer nytt partnerskap for økt vekst", 
         "sentiment": "positive",
         "summary": f"{company_name} har inngått et strategisk partnerskap som forventes å drive betydelig vekst i de kommende kvartalene."}
    ]
    
    neutral_news = [
        {"title": f"{company_name} møter forventningene i siste kvartalsrapport", 
         "sentiment": "neutral",
         "summary": f"{company_name}s resultater for siste kvartal var på linje med analytikernes forventninger, uten større overraskelser."},
        {"title": f"{company_name} ansetter ny finansdirektør", 
         "sentiment": "neutral",
         "summary": f"{company_name} har utnevnt en ny finansdirektør som vil tiltre stillingen neste måned."},
        {"title": f"{company_name} holder årlig aksjonærmøte neste uke", 
         "sentiment": "neutral",
         "summary": f"{company_name} forbereder seg til sitt årlige aksjonærmøte der strategien for det kommende året vil bli presentert."}
    ]
    
    negative_news = [
        {"title": f"{company_name} skuffer med svakere kvartalstall enn forventet", 
         "sentiment": "negative",
         "summary": f"{company_name}s resultater for siste kvartal var under analytikernes forventninger, noe som har ført til bekymring blant investorer."},
        {"title": f"Analytikere nedgraderer {company_name} på grunn av vekstbekymringer", 
         "sentiment": "negative",
         "summary": f"Flere analytikere har nedgradert sine anbefalinger for {company_name} grunnet bekymringer om selskapets vekstutsikter."},
        {"title": f"{company_name} møter økt konkurranse i hovedmarkedet", 
         "sentiment": "negative",
         "summary": f"{company_name} opplever økende press fra konkurrenter, noe som kan påvirke markedsandelen negativt i kommende kvartaler."}
    ]
    
    # Decide sentiment distribution based on symbol_hash
    sentiment_value = (symbol_hash % 10)
    if sentiment_value >= 7:
        # Mostly positive
        news_pool = positive_news * 3 + neutral_news * 2 + negative_news
    elif sentiment_value <= 3:
        # Mostly negative
        news_pool = negative_news * 3 + neutral_news * 2 + positive_news
    else:
        # Balanced
        news_pool = positive_news * 2 + neutral_news * 2 + negative_news * 2
    
    # Randomly select 4-6 news articles
    num_articles = random.randint(4, 6)
    selected_news = random.sample(news_pool, min(num_articles, len(news_pool)))
    
    # Add dates within the last 14 days
    now = datetime.now()
    
    for i, news in enumerate(selected_news):
        # Spread dates over the last 14 days
        days_ago = random.randint(0, 14)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        news_date = now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        
        # Add date and source
        news['date'] = news_date.strftime('%Y-%m-%d %H:%M')
        
        # Add sources
        sources = ['Bloomberg', 'Reuters', 'Financial Times', 'CNBC', 'Wall Street Journal', 'E24', 'Dagens Næringsliv']
        news['source'] = random.choice(sources)
    
    return selected_news

def _generate_sentiment_history(symbol):
    """Generate historical sentiment data for chart visualization"""
    import random
    from datetime import datetime, timedelta
    # This function is currently unused and can be removed, but fixing indentation for now
    # Placeholder implementation
    return {
        'dates': [],
        'scores': []
    }

# Old recommendations function - disabled to avoid route conflicts
# @analysis.route('/recommendations')
# @analysis.route('/recommendations/')
# @analysis.route('/recommendations/<symbol>')
@access_required
def recommendations_old(symbol=None):
    """AI-powered stock recommendations and ratings"""
    try:
        # If specific symbol requested, get detailed recommendation
        if symbol:
            # Helper to clean dict for JSON serialization
            def clean_dict(d):
                from jinja2.runtime import Undefined
                if isinstance(d, dict):
                    return {k: clean_dict(v) for k, v in d.items() if not isinstance(v, Undefined)}
                elif isinstance(d, list):
                    return [clean_dict(v) for v in d]
                elif isinstance(d, Undefined):
                    return None
                return d
            symbol = symbol.strip().upper()
            # Mock detailed recommendation data for specific symbol
            hash_seed = abs(hash(symbol)) % 1000
            sentiment_data = {}  # Provide a default empty dict for demonstration
            sentiment_data = clean_dict(sentiment_data)
            detailed_recommendation = {
                'symbol': symbol,
                'name': f"{symbol.replace('.OL', ' ASA').replace('-USD', '')} Company",
                'current_price': 100 + (hash_seed % 200),
                'target_price': (100 + (hash_seed % 200)) * 1.15,
                'upside': 15.0 + (hash_seed % 20),
                'rating': ['STRONG_BUY', 'BUY', 'HOLD', 'SELL'][hash_seed % 4],
                'confidence': 70 + (hash_seed % 25),
                'risk_level': ['Low', 'Medium', 'High'][hash_seed % 3],
                'timeframe': '12 months',
                'reasons': [
                    'Strong fundamentals and earnings growth',
                    'Market leadership position in sector',
                    'Favorable industry trends and tailwinds',
                    'Solid financial metrics and balance sheet',
                    'Positive analyst sentiment and upgrades'
                ],
                'risks': [
                    'Market volatility and economic uncertainty',
                    'Competitive pressure in sector',
                    'Regulatory changes potential impact',
                    'Currency fluctuation risks'
                ],
                'sector': ['Technology', 'Banking', 'Energy', 'Healthcare', 'Consumer'][hash_seed % 5],
                'analyst_count': 5 + (hash_seed % 15),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'price_targets': {
                    'high': (100 + (hash_seed % 200)) * 1.25,
                    'average': (100 + (hash_seed % 200)) * 1.15,
                    'low': (100 + (hash_seed % 200)) * 1.05
                },
                'analyst_ratings': {
                    'strong_buy': hash_seed % 5,
                    'buy': hash_seed % 8,
                    'hold': hash_seed % 6,
                    'sell': hash_seed % 3,
                    'strong_sell': hash_seed % 2
                },
                'key_metrics': {
                    'pe_ratio': 15.0 + (hash_seed % 20),
                    'pb_ratio': 1.5 + (hash_seed % 3),
                    'dividend_yield': 2.0 + (hash_seed % 5),
                    'roe': 10.0 + (hash_seed % 20)
                }
            }
            return render_template('analysis/recommendation_detail.html',
                                 recommendation=detailed_recommendation,
                                 symbol=symbol,
                                 page_title=f"Anbefaling for {symbol}")
        
        # Generate comprehensive mock recommendations data for overview
        recommendations_data = {
            'featured_picks': [
                {
                    'symbol': 'DNB.OL',
                    'name': 'DNB Bank ASA',
                    'current_price': 185.20,
                    'target_price': 210.00,
                    'upside': 13.4,
                    # ... rest of featured_picks ...
                },
                # ... other featured picks ...
            ],
            # ... rest of recommendations_data ...
        }
        # Now handle symbol-specific recommendation
        if symbol:
            # Helper to clean dict for JSON serialization
            def clean_dict(d):
                from jinja2.runtime import Undefined
                if isinstance(d, dict):
                    return {k: clean_dict(v) for k, v in d.items() if not isinstance(v, Undefined)}
                elif isinstance(d, list):
                    return [clean_dict(v) for v in d]
                elif isinstance(d, Undefined):
                    return None
                return d
            symbol = symbol.strip().upper()
            # Mock detailed recommendation data for specific symbol
            hash_seed = abs(hash(symbol)) % 1000
            sentiment_data = {}  # Provide a default empty dict for demonstration
            sentiment_data = clean_dict(sentiment_data)
            detailed_recommendation = {
                'symbol': symbol,
                'name': f"{symbol.replace('.OL', ' ASA').replace('-USD', '')} Company",
                'current_price': 100 + (hash_seed % 200),
                'target_price': (100 + (hash_seed % 200)) * 1.15,
                'upside': 15.0 + (hash_seed % 20),
                'rating': ['STRONG_BUY', 'BUY', 'HOLD', 'SELL'][hash_seed % 4],
                'confidence': 70 + (hash_seed % 25),
                'risk_level': ['Low', 'Medium', 'High'][hash_seed % 3],
                'timeframe': '12 months',
                'reasons': [
                    'Strong fundamentals and earnings growth',
                    'Market leadership position in sector',
                    'Favorable industry trends and tailwinds',
                    'Solid financial metrics and balance sheet',
                    'Positive analyst sentiment and upgrades'
                ],
                'risks': [
                    'Market volatility and economic uncertainty',
                    'Competitive pressure in sector',
                    'Regulatory changes potential impact',
                    'Currency fluctuation risks'
                ],
                'sector': ['Technology', 'Banking', 'Energy', 'Healthcare', 'Consumer'][hash_seed % 5],
                'analyst_count': 5 + (hash_seed % 15),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'price_targets': {
                    'high': (100 + (hash_seed % 200)) * 1.25,
                    'average': (100 + (hash_seed % 200)) * 1.15,
                    'low': (100 + (hash_seed % 200)) * 1.05
                },
                'analyst_ratings': {
                    'strong_buy': hash_seed % 5,
                    'buy': hash_seed % 8,
                    'hold': hash_seed % 6,
                    'sell': hash_seed % 3,
                    'strong_sell': hash_seed % 2
                },
                'key_metrics': {
                    'pe_ratio': 15.0 + (hash_seed % 20),
                    'pb_ratio': 1.5 + (hash_seed % 3),
                    'dividend_yield': 2.0 + (hash_seed % 5),
                    'roe': 10.0 + (hash_seed % 20)
                }
            }
            return render_template('analysis/recommendation_detail.html',
                                 recommendation=detailed_recommendation,
                                 symbol=symbol,
                                 page_title=f"Anbefaling for {symbol}")
        # If no symbol, continue with recommendations_data logic
                             
    except Exception as e:
        logger.error(f"Error in recommendations: {e}")
        return render_template('error.html',
                             error="Anbefalinger er midlertidig utilgjengelig.")

@analysis.route('/comparison')
@demo_access  
def comparison():
    """Stock comparison page"""
    logger.info("Stock comparison page accessed")
    
    try:
        symbols = request.args.get('symbols', '').split(',') if request.args.get('symbols') else []
        symbols = [s.strip().upper() for s in symbols if s.strip()]
        
        comparison_data = {}
        
        if symbols:
            logger.info(f"Comparing symbols: {symbols}")
            
            # Mock comparison data for now
            for symbol in symbols[:5]:  # Limit to 5 symbols max
                comparison_data[symbol] = {
                    'symbol': symbol,
                    'name': symbol,
                    'current_price': 100.0,
                    'change_percent': 2.5,
                    'market_cap': '1.5B',
                    'pe_ratio': 18.5,
                    'dividend_yield': 2.1,
                    'volume': '2.1M',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
        
        return render_template('analysis/comparison.html',
                             comparison_data=comparison_data,
                             symbols=symbols,
                             title="Stock Comparison")
                             
    except Exception as e:
        logger.error(f"Error in stock comparison: {e}")
        return render_template('analysis/comparison.html',
                             comparison_data={},
                             symbols=[],
                             title="Stock Comparison",
                             error="Det oppstod en feil ved sammenligning av aksjer.")

@analysis.route('/screener', methods=['GET', 'POST'])
@demo_access
def screener():
    """Stock screener with basic functionality"""
    logger.info(f"Screener route accessed - Method: {request.method}")
    try:
        results = []
        logger.info("Starting screener processing...")
        # Define available filters for the screener
        available_filters = {
            'Valuation': {
                'pe_ratio': 'P/E Ratio',
                'pb_ratio': 'P/B Ratio',
                'price_to_sales': 'Price/Sales',
                'ev_ebitda': 'EV/EBITDA'
            },
            'Financial Health': {
                'debt_equity': 'Debt/Equity',
                'current_ratio': 'Current Ratio',
                'roe': 'Return on Equity',
                'roa': 'Return on Assets'
            },
            'Growth': {
                'revenue_growth': 'Revenue Growth',
                'earnings_growth': 'Earnings Growth',
                'eps_growth': 'EPS Growth'
            },
            'Dividends': {
                'dividend_yield': 'Dividend Yield',
                'payout_ratio': 'Payout Ratio',
                'dividend_growth': 'Dividend Growth'
            }
        }
        preset_screens = {
            'value_stocks': {
                'pe_ratio_max': 15,
                'pb_ratio_max': 2.0,
                'debt_equity_max': 0.5
            },
            'growth_stocks': {
                'earnings_growth_min': 15,
                'revenue_growth_min': 10,
                'pe_ratio_max': 30
            },
            'dividend_stocks': {
                'dividend_yield_min': 3.0,
                'payout_ratio_max': 80,
                'debt_equity_max': 0.6
            }
        }
        selected_filters = request.form.getlist('filters') if request.method == 'POST' else []
        selected_preset = request.form.get('preset_screen', '') if request.method == 'POST' else ''
        filter_display_names = {}
        for category in available_filters.values():
            filter_display_names.update(category)
        if request.method == 'POST':
            # Use real screener results from DataService
            results = DataService.run_screener(selected_filters, selected_preset) if DataService and hasattr(DataService, 'run_screener') else []
        return render_template('analysis/screener.html',
                              results=results,
                              show_results=bool(results),
                              available_filters=available_filters,
                              preset_screens=preset_screens,
                              filter_display_names=filter_display_names,
                              selected_filters=selected_filters,
                              selected_preset=selected_preset)
    except Exception as e:
        logger.error(f"Error in screener: {e}")
        return render_template('error.html', error=f"Screener error: {str(e)}")
        
        preset_screens = {
            'value_stocks': {
                'pe_ratio_max': 15,
                'pb_ratio_max': 2.0,
                'debt_equity_max': 0.5
            },
            'growth_stocks': {
                'earnings_growth_min': 15,
                'revenue_growth_min': 10,
                'pe_ratio_max': 30
            },
            'dividend_stocks': {
                'dividend_yield_min': 3.0,
                'payout_ratio_max': 80,
                'debt_equity_max': 0.6
            }
        }
        
        if request.method == 'POST':
            # Mock screener results
            results = [
                {
                    'ticker': 'EQNR.OL',
                    'name': 'Equinor ASA',
                    'price': 320.50,
                    'change_percent': 2.5,
                    'volume': '1.2M',
                    'market_cap': '1020B',
                    'pe_ratio': 12.4,
                    'dividend_yield': 5.2,
                    'sector': 'Energy'
                },
                {
                    'ticker': 'DNB.OL',
                    'name': 'DNB Bank ASA',
                    'price': 185.20,
                    'change_percent': 1.8,
                    'volume': '890K',
                    'market_cap': '280B',
                    'pe_ratio': 11.2,
                    'dividend_yield': 6.2,
                    'sector': 'Financial'
                }
            ]
        
        # Process filter names before template rendering
        filter_display_names = {}
        for category in available_filters.values():
            filter_display_names.update(category)

            return render_template('analysis/screener.html',
                                 results=results,
                                 show_results=bool(results),
                                 available_filters=available_filters,
                                 preset_screens=preset_screens,
                                 filter_display_names=filter_display_names)
                             
    except Exception as e:
        import traceback
        logger.error(f"Error in screener: {e}")
        logger.error(f"Screener traceback: {traceback.format_exc()}")
        return render_template('error.html',
                             error=f"Screener error: {str(e)}")

@analysis.route('/benjamin-graham', methods=['GET', 'POST'])
@access_required
def benjamin_graham():
    """Benjamin Graham value analysis"""
    ticker = request.args.get('ticker') or request.form.get('ticker')
    if ticker:
        ticker = ticker.strip().upper()
        # Always return mock analysis for any ticker
        analysis_data = {
            'ticker': ticker,
            'graham_score': 78.5,
            'intrinsic_value': 195.00,
            'current_price': 185.20,
            'margin_of_safety': 5.3,
            'criteria_met': ['Low P/E ratio', 'Strong balance sheet', 'Consistent earnings'],
            'criteria_failed': ['Limited growth'],
            'criteria_results': {
                'low_pe_ratio': {
                    'criterion': {'name': 'Low P/E ratio', 'description': 'P/E ratio under 15'},
                    'value': 11.2,
                    'passed': True
                },
                'strong_balance_sheet': {
                    'criterion': {'name': 'Strong balance sheet', 'description': 'Solid financial position'},
                    'value': 'Yes',
                    'passed': True
                },
                'consistent_earnings': {
                    'criterion': {'name': 'Consistent earnings', 'description': 'Stable earnings over time'},
                    'value': 'Yes',
                    'passed': True
                },
                'limited_growth': {
                    'criterion': {'name': 'Limited growth', 'description': 'Growth below sector average'},
                    'value': 'Low',
                    'passed': False
                }
            },
            'financial_metrics': {'pe_ratio': 11.2, 'pb_ratio': 1.1},
            'recommendation': {
                'action': 'BUY',
                'reasoning': f"Graham score of 78.5 indicates strong value proposition"
            },
            'company_name': f"Company Analysis for {ticker}",
            'sector': 'Financial Services'
        }
        return render_template('analysis/benjamin_graham_select.html', analysis=analysis_data, ticker=ticker)
    # Show selection page if no ticker
    oslo_stocks = {
        'EQNR.OL': {'name': 'Equinor ASA', 'last_price': 270.50},
        'DNB.OL': {'name': 'DNB Bank ASA', 'last_price': 185.20}
    }
    global_stocks = {
        'AAPL': {'name': 'Apple Inc.', 'last_price': 185.00},
        'MSFT': {'name': 'Microsoft Corporation', 'last_price': 420.50}
    }
    return render_template('analysis/benjamin_graham_select.html', oslo_stocks=oslo_stocks, global_stocks=global_stocks, analysis=None)

@analysis.route('/sentiment-view')
@access_required  
def sentiment_view():
    """Sentiment analysis view"""
    return redirect(url_for('analysis.sentiment'))

@analysis.route('/insider-trading')
@access_required
def insider_trading():
    """Redirect to dedicated insider trading page"""
    return redirect(url_for('market_intel.insider_trading'))

# API Endpoints
@analysis.route('/api/technical/<symbol>')
@access_required
def api_technical_data(symbol):
    """API endpoint for technical data"""
    try:
        # Mock technical data
        data = {
            'ticker': symbol.upper(),
            'current_price': 320.50,
            'change': 5.20,
            'change_percent': 1.65,
            'volume': 1250000,
            'indicators': {
                'rsi': 62.5,
                'macd': 2.15,
                'macd_signal': 1.85,
                'sma_20': 315.20,
                'sma_50': 310.80,
                'sma_200': 295.40
            },
            'patterns': ['Ascending Triangle'],
            'recommendation': 'BUY',
            'momentum': 'Bullish',
            'volatility': 0.25,
            'volume_analysis': 'Above Average'
        }
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error in API technical data for {symbol}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@analysis.route('/ai')
@analysis.route('/ai/<ticker>')
@access_required
def ai(ticker=None):
    """AI-powered stock analysis"""
    try:
        # Get ticker from URL parameter, query string, or form
        if not ticker:
            ticker = request.args.get('ticker') or request.form.get('ticker')
        
        if ticker:
            ticker = ticker.strip().upper()
            cache_key = f"ai_analysis_{ticker}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data
            
            # Mock AI analysis data
            ai_analysis = {
                'ticker': ticker.upper(),
                'sentiment': 'bullish',
                'summary': f'Basert på vår KI-analyse viser {ticker} sterke signaler for potensielt oppgang. Tekniske indikatorer er overveiende positive, mens fundamentale faktorer støtter oppunder verdivurderingen.',
                'prediction': {
                    'direction': 'Bullish',
                    'confidence': 0.78,
                    'target_price': 165.50,
                    'timeframe': '3 months'
                },
                'factors': [
                    {'factor': 'Technical indicators', 'weight': 0.35, 'signal': 'Buy'},
                    {'factor': 'Market sentiment', 'weight': 0.25, 'signal': 'Hold'},
                    {'factor': 'Financial metrics', 'weight': 0.40, 'signal': 'Buy'}
                ],
                'technical_factors': [
                    'RSI indikerer kjøpsmulighet (32.4)',
                    'MACD viser bullish crossover',
                    'Volum er over gjennomsnitt (+23%)',
                    'Støtte ved 142.50, motstand ved 168.00',
                    'Moving averages (50/200) i gylden kors formasjon'
                ],
                'fundamental_factors': [
                    'P/E ratio på 18.4 er rimelig for sektoren',
                    'Inntektsvekst på 12% siste kvartal',
                    'Solid balanse med lav gjeld/egenkapital',
                    'Økning i markedsandel innen hovedsegment',
                    'Ledelsen har guidet oppover for Q4'
                ],
                'economic_indicators': {
                    'sector_performance': 'Sektoren presterer bedre enn markedet',
                    'macro_conditions': 'Makroøkonomiske forhold støtter vekst',
                    'currency_impact': 'Valutakurser favoriserer eksportinntekter',
                    'interest_rates': 'Rentemiljøet er stabilt',
                    'market_outlook': 'Positive markedsutsikter'
                },
                'risk_assessment': {
                    'level': 'Medium',
                    'factors': ['Market volatility', 'Sector rotation risk']
                }
            }
            
            result = render_template('analysis/ai.html', 
                                   analysis=ai_analysis,
                                   ticker=ticker)
            cache.set(cache_key, result, timeout=1800)
            return result
        else:
            return render_template('analysis/ai_form.html')
    except Exception as e:
        logger.error(f'AI analysis error: {str(e)}')
        flash(f'Feil ved lasting av AI-analyse: {str(e)}', 'error')
        return render_template('analysis/ai_form.html')

@analysis.route('/short-analysis')
@analysis.route('/short-analysis/<ticker>')
@demo_access
def short_analysis(ticker=None):
    """Short selling analysis"""
    try:
        # Check for ticker in URL path or GET parameter
        if not ticker:
            ticker = request.args.get('ticker')
        
        if ticker:
            cache_key = f"short_analysis_{ticker}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data
            
            # Mock short analysis data with all required fields
            short_data = {
                'ticker': ticker.upper(),
                'short_interest': {
                    'current': 12.5,  # Add current field
                    'percentage': 12.5,
                    'change': -2.1,  # Add change field for template
                    'shares_short': 2500000,
                    'days_to_cover': 3.2,
                    'trend': 'Increasing'
                },
                'analysis': {
                    'recommendation': 'Avoid shorting',
                    'risk_level': 'High',
                    'reasoning': 'Strong fundamentals and positive momentum'
                },
                'key_metrics': [
                    {'metric': 'Borrow rate', 'value': '2.5%'},
                    {'metric': 'Float shorted', 'value': '12.5%'},
                    {'metric': 'Short squeeze risk', 'value': 'Medium'}
                ]
            }
            
            result = render_template('analysis/short_analysis.html', 
                                   short_data=short_data,
                                   ticker=ticker)
            cache.set(cache_key, result, timeout=1800)
            return result
        else:
            return render_template('analysis/short_analysis_select.html')
    except Exception as e:
        flash(f'Feil ved lasting av short-analyse: {str(e)}', 'error')
        return render_template('analysis/short_analysis_select.html')

@analysis.route('/ai-predictions')
@analysis.route('/ai-predictions/<ticker>')
@access_required
def ai_predictions(ticker=None):
    """AI predictions for stocks"""
    try:
        # Accept ticker from URL or GET query string
        if not ticker:
            ticker = request.args.get('ticker')
        if ticker:
            cache_key = f"ai_predictions_{ticker}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data
            
            # Mock AI predictions data
            predictions = {
                'ticker': ticker.upper(),
                'current_price': 150.00,
                'predicted_price': 152.30,
                'change_percent': 1.53,
                'confidence': 0.85,
                'key_factors': [
                    'Historical price patterns',
                    'Market sentiment analysis',
                    'Technical indicators',
                    'News sentiment'
                ],
                'sentiment_score': 0.72,
                'news_sentiment': 0.78,
                'risk_metrics': {
                    'volatility': 0.18
                },
                'dates': ['2025-08-01', '2025-08-02', '2025-08-03', '2025-08-04', '2025-08-05', '2025-08-06', '2025-08-07'],
                'predicted_values': [150.00, 150.80, 151.20, 151.60, 151.90, 152.10, 152.30],
                'confidence_upper': [151.00, 151.80, 152.20, 152.60, 152.90, 153.10, 153.30],
                'confidence_lower': [149.00, 149.80, 150.20, 150.60, 150.90, 151.10, 151.30],
                'model_accuracy': 87.3,
                'factors': [
                    'Historical price patterns',
                    'Market sentiment analysis',
                    'Technical indicators',
                    'News sentiment'
                ]
            }
            
            result = render_template('analysis/ai_predictions.html', 
                                   predictions=predictions,
                                   ticker=ticker)
            cache.set(cache_key, result, timeout=1800)
            return result
        else:
            return render_template('analysis/ai_predictions_select.html')
    except Exception as e:
        flash(f'Feil ved lasting av AI-prediksjoner: {str(e)}', 'error')
        return render_template('analysis/ai_predictions_select.html')

@analysis.route('/fundamental', methods=['GET', 'POST'])
@analysis.route('/fundamental/', methods=['GET', 'POST'])
@access_required
def fundamental():
    """Fundamental analysis"""
    try:
        ticker = None
        
        # Handle POST requests (form submissions)
        if request.method == 'POST':
            ticker = request.form.get('ticker')
        # Handle GET requests with query parameter (without symbol in URL)
        else:
            ticker = request.args.get('ticker')
            
        if ticker and ticker.strip():
            ticker = ticker.strip().upper()
            logger.info(f"Fundamental analysis requested for: {ticker}")
            
            # Enhanced mock fundamental analysis data
            fundamental_data = {
                'ticker': ticker,
                'company_name': f"{ticker} Corporation",
                'longName': f"{ticker} Corporation",  # For template compatibility
                'sector': 'Technology' if ticker in ['AAPL', 'MSFT', 'GOOGL', 'TSLA'] else 'Energy' if ticker.endswith('.OL') else 'Financial',
                'industry': 'Software' if ticker in ['AAPL', 'MSFT', 'GOOGL'] else 'Oil & Gas' if ticker.endswith('.OL') else 'Banking',
                'market_cap': 2.5e12 if ticker == 'AAPL' else 1.2e9,
                'marketCap': 2.5e12 if ticker == 'AAPL' else 1.2e9,  # Template expects this key
                'beta': 1.2,  # For template compatibility
                'revenue': 2.5e11 if ticker == 'AAPL' else 1.5e10,  # Add revenue
                'revenue_growth': 12.4,
                'eps_growth': 15.2,
                'financial_metrics': {
                    'pe_ratio': 24.5,
                    'peg_ratio': 1.2,
                    'price_to_book': 3.8,
                    'debt_to_equity': 0.65,
                    'roe': 18.5,
                    'roa': 12.3,
                    'current_ratio': 1.8,
                    'quick_ratio': 1.4,
                    'profit_margin': 21.2,
                    'operating_margin': 28.5
                },
                'valuation': {
                    'fair_value': 165.0,
                    'current_price': 152.0,
                    'upside_potential': 8.5,
                    'target_price': 170.0,
                    'rating': 'BUY',
                    'analyst_rating': 'Strong Buy',
                    'price_target_confidence': 'High'
                },
                'growth_metrics': {
                    'revenue_growth_5y': 12.4,
                    'earnings_growth_5y': 15.2,
                    'dividend_yield': 2.4,
                    'dividend_growth_5y': 8.1,
                    'eps_growth_ttm': 18.7,
                    'revenue_growth_ttm': 11.3
                },
                'financial_health': {
                    'debt_to_assets': 0.28,
                    'interest_coverage': 12.5,
                    'altman_z_score': 3.2,
                    'piotroski_score': 7,
                    'financial_strength': 'Strong'
                },
                'key_ratios': {
                    'price_to_sales': 5.8,
                    'price_to_cash_flow': 18.2,
                    'enterprise_value_to_ebitda': 15.6,
                    'book_value_per_share': 4.2
                },
                'analysis_summary': {
                    'strengths': [
                        'Strong revenue growth',
                        'Healthy profit margins',
                        'Low debt levels',
                        'Consistent dividend payments'
                    ],
                    'weaknesses': [
                        'High valuation multiples',
                        'Increased competition',
                        'Market saturation risk'
                    ],
                    'recommendation': 'BUY',
                    'confidence_level': 'High',
                    'time_horizon': '12 months'
                }
            }
            
            logger.info(f"Rendering fundamental analysis for {ticker}")
            result = render_template('analysis/fundamental.html', 
                                   symbol=ticker,
                                   ticker=ticker,
                                   analysis_data=fundamental_data,
                                   data=fundamental_data,
                                   stock_info=fundamental_data,  # Also pass as stock_info
                                   demo_mode=True)
            return result
        else:
            logger.info("Fundamental analysis - no ticker provided")
            return render_template('analysis/fundamental_select.html')
            
    except Exception as e:
        logger.error(f'Error in fundamental analysis for {ticker}: {str(e)}')
        flash(f'Feil ved lasting av fundamental analyse: {str(e)}', 'error')
        return render_template('analysis/fundamental_select.html', 
                             error=f"Kunne ikke laste fundamental analyse for {ticker}")

@analysis.route('/technical-analysis/<symbol>')
@access_required
def technical_analysis(symbol):
    """Alternative route for technical analysis with symbol parameter"""
    return redirect(url_for('analysis.technical', ticker=symbol))

@analysis.route('/screener-view')
@demo_access
def screener_view():
    """Screener view page"""
    return render_template('analysis/screener_view.html', title='Aksje Screener')

@analysis.route('/recommendation')
@analysis.route('/recommendations')
@analysis.route('/recommendation/<symbol>')
@analysis.route('/recommendations/<symbol>')
@access_required
def recommendation(symbol=None):
    """Investment recommendations page with comprehensive analysis"""
    from datetime import datetime, timedelta
    
    # If specific symbol requested, show focused recommendations
    if symbol:
        # Generate symbol-specific recommendation
        symbol_hash = abs(hash(symbol)) % 10000
        base_score = 65 + (symbol_hash % 30)  # Score between 65-95
        
        # Determine recommendation type
        if base_score >= 85:
            recommendation_type = 'STRONG BUY'
            recommendation_color = 'success'
        elif base_score >= 75:
            recommendation_type = 'BUY'
            recommendation_color = 'success'
        elif base_score >= 60:
            recommendation_type = 'HOLD'
            recommendation_color = 'warning'
        else:
            recommendation_type = 'SELL'
            recommendation_color = 'danger'
        
        symbol_recommendation = {
            'symbol': symbol,
            'company_name': f'Company {symbol}',
            'recommendation': recommendation_type,
            'confidence': base_score,
            'target_price': 100 + (symbol_hash % 50),
            'current_price': 95 + (symbol_hash % 40),
            'analyst_count': 8 + (symbol_hash % 12),
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'key_factors': [
                'Strong fundamental analysis',
                'Positive technical indicators', 
                'Market sentiment improving',
                'Sector outlook favorable'
            ],
            'price_targets': {
                'high': 120 + (symbol_hash % 30),
                'average': 110 + (symbol_hash % 20), 
                'low': 100 + (symbol_hash % 15)
            }
        }
        
        return render_template('analysis/recommendation_detail.html',
                             recommendation=symbol_recommendation,
                             symbol=symbol,
                             focused_analysis=True,
                             recommendation_color=recommendation_color)
    
    # General recommendations if no specific symbol
    
    # Comprehensive investment recommendations data
    recommendations = {
        'norwegian_stocks': [
            {
                'ticker': 'DNB.OL',
                'company_name': 'DNB Bank ASA',
                'sector': 'Finansielle tjenester',
                'recommendation': 'KJØP',
                'target_price': 190.00,
                'current_price': 175.20,
                'upside_percent': 8.44,
                'risk_level': 'Moderat',
                'time_horizon': '6-12 måneder',
                'analyst_rating': 4.2,
                'strengths': [
                    'Markedsledende posisjon i Norge',
                    'Sterk kapitalbase og likviditet',
                    'Robust utbyttepolitikk',
                    'Diversifisert forretningsmodell'
                ],
                'risks': [
                    'Renteendringer kan påvirke marginer',
                    'Kreditttap ved økonomisk nedgang',
                    'Regulatoriske endringer'
                ],
                'recent_news': 'Rapporterte sterke Q4-resultater med økt utlånsvolum',
                'dividend_yield': 6.8,
                'pe_ratio': 12.5
            },
            {
                'ticker': 'EQNR.OL',
                'company_name': 'Equinor ASA',
                'sector': 'Energi',
                'recommendation': 'KJØP',
                'target_price': 295.00,
                'current_price': 278.40,
                'upside_percent': 5.96,
                'risk_level': 'Høy',
                'time_horizon': '12-18 måneder',
                'analyst_rating': 4.0,
                'strengths': [
                    'Ledende posisjon innen offshore vind',
                    'Sterke kontantstrømmer fra olje og gass',
                    'Ambisiøse klimamål og grønn omstilling',
                    'Teknologisk ekspertise og innovasjon'
                ],
                'risks': [
                    'Volatilitet i olje- og gasspriser',
                    'Klimapolitiske endringer',
                    'Høye investeringskostnader i fornybar energi'
                ],
                'recent_news': 'Kunngjorde nye offshore vindprosjekter i Storbritannia',
                'dividend_yield': 4.2,
                'pe_ratio': 14.8
            },
            {
                'ticker': 'NEL.OL',
                'company_name': 'Nel ASA',
                'sector': 'Ren energi',
                'recommendation': 'HOLD',
                'target_price': 8.50,
                'current_price': 7.85,
                'upside_percent': 8.28,
                'risk_level': 'Høy',
                'time_horizon': '18-24 måneder',
                'analyst_rating': 3.5,
                'strengths': [
                    'Teknologileder innen hydrogenløsninger',
                    'Stor ordrereserve og pipeline',
                    'Støtte fra EU Green Deal',
                    'Strategiske partnerskap globalt'
                ],
                'risks': [
                    'Høy volatilitet og spekulativ karakter',
                    'Avhengig av statlige subsidier',
                    'Intens konkurranse i hydrogensektoren'
                ],
                'recent_news': 'Signerte stor elektrolysekontrakt i Tyskland',
                'dividend_yield': 0.0,
                'pe_ratio': None
            }
        ],
        'international_stocks': [
            {
                'ticker': 'AAPL',
                'company_name': 'Apple Inc.',
                'sector': 'Teknologi',
                'recommendation': 'KJØP',
                'target_price': 210.00,
                'current_price': 192.50,
                'upside_percent': 9.09,
                'risk_level': 'Moderat',
                'time_horizon': '6-12 måneder',
                'analyst_rating': 4.5,
                'strengths': [
                    'Sterk merkevare og kundeprogramlojalitet',
                    'Diversifisert produktportefølje',
                    'Sterke kontantstrømmer og balanse',
                    'Innovasjon innen AI og AR/VR'
                ],
                'risks': [
                    'Høy verdsettelse sammenlignet med historiske nivåer',
                    'Avhengighet av iPhone-salg',
                    'Geopolitiske spenninger med Kina'
                ],
                'recent_news': 'Lanserte nye AI-funksjoner i iOS 18',
                'dividend_yield': 0.5,
                'pe_ratio': 28.5
            },
            {
                'ticker': 'NVDA',
                'company_name': 'NVIDIA Corporation',
                'sector': 'Halvledere',
                'recommendation': 'KJØP',
                'target_price': 520.00,
                'current_price': 485.20,
                'upside_percent': 7.18,
                'risk_level': 'Høy',
                'time_horizon': '12-18 måneder',
                'analyst_rating': 4.8,
                'strengths': [
                    'Dominerer AI-chip-markedet',
                    'Sterk vekst i datasenterprodukter',
                    'Teknologisk moat og innovasjon',
                    'Ekspanderende adresserbart marked'
                ],
                'risks': [
                    'Høy verdsettelse og forventninger',
                    'Syklisk halvledermarked',
                    'Økt konkurranse fra AMD og Intel'
                ],
                'recent_news': 'Rapporterte rekordresultater drevet av AI-etterspørsel',
                'dividend_yield': 0.03,
                'pe_ratio': 65.2
            }
        ],
        'sector_themes': [
            {
                'theme': 'Fornybar Energi og Klimateknologi',
                'description': 'Kraftig vekst forventes i sektoren drevet av klimapolitikk og teknologiutvikling',
                'recommended_stocks': ['NEL.OL', 'EQNR.OL', 'ENPH', 'TSLA'],
                'time_horizon': '2-5 år',
                'risk_level': 'Høy',
                'potential_return': '15-25% årlig'
            },
            {
                'theme': 'Kunstig Intelligens og Teknologi',
                'description': 'AI-revolusjon driver vekst i cloud, halvledere og programvare',
                'recommended_stocks': ['NVDA', 'MSFT', 'GOOGL', 'AAPL'],
                'time_horizon': '1-3 år',
                'risk_level': 'Moderat-Høy',
                'potential_return': '10-20% årlig'
            },
            {
                'theme': 'Nordiske Finansaksjer',
                'description': 'Stabile utbyttebetalere med solide fundamentale forhold',
                'recommended_stocks': ['DNB.OL', 'SEB-A.ST', 'DANSKE.CO'],
                'time_horizon': '1-2 år',
                'risk_level': 'Lav-Moderat',
                'potential_return': '8-12% årlig'
            }
        ],
        'portfolio_models': [
            {
                'name': 'Konservativ Vekst',
                'description': 'Stabile aksjer med moderat risiko og jevn avkastning',
                'allocation': {
                    'Nordiske finansaksjer': 40,
                    'Amerikanske blue chips': 35,
                    'Obligasjoner': 20,
                    'Kontanter': 5
                },
                'expected_return': '6-8% årlig',
                'volatility': 'Lav',
                'recommended_for': 'Konservative investorer, pensjonssparing'
            },
            {
                'name': 'Balansert Vekst',
                'description': 'Diversifisert portefølje med moderat til høy vekstpotensial',
                'allocation': {
                    'Teknologiaksjer': 30,
                    'Norske aksjer': 25,
                    'Internasjonale aksjer': 25,
                    'Fornybar energi': 15,
                    'Kontanter': 5
                },
                'expected_return': '8-12% årlig',
                'volatility': 'Moderat',
                'recommended_for': 'Langsiktige investorer med moderat risikotoleranse'
            },
            {
                'name': 'Aggressiv Vekst',
                'description': 'Høy vekst fokusert på teknologi og fremvoksende sektorer',
                'allocation': {
                    'AI og teknologi': 40,
                    'Fornybar energi': 25,
                    'Vekstaksjer': 20,
                    'Kryptovaluta': 10,
                    'Kontanter': 5
                },
                'expected_return': '12-20% årlig',
                'volatility': 'Høy',
                'recommended_for': 'Unge investorer med høy risikotoleranse'
            }
        ]
    }
    
    # Market insights and analysis
    market_insights = {
        'current_environment': {
            'market_sentiment': 'Forsiktig optimistisk',
            'key_drivers': [
                'AI-revolusjon fortsetter å drive teknologiaksjer',
                'Sentralbankers rentepolitikk påvirker valg',
                'Grønn omstilling skaper nye investeringsmuligheter',
                'Geopolitiske forhold skaper usikkerhet'
            ],
            'opportunities': [
                'AI og maskinlæring teknologier',
                'Fornybar energi og energilagring',
                'Nordiske kvalitetsaksjer med høye utbytter',
                'Cybersikkerhet og digital infrastruktur'
            ],
            'risks': [
                'Inflasjon og renteendringer',
                'Geopolitiske spenninger',
                'Oververdsettelse i enkelte sektorer',
                'Regulatoriske endringer innen teknologi'
            ]
        },
        'quarterly_outlook': {
            'q1_2024': 'Fokus på earnings season og rentebeslutninger',
            'q2_2024': 'Sommertradition og potensielle volatilitet',
            'q3_2024': 'Tilbake til normal handel etter sommerferien',
            'q4_2024': 'Årsresultater og utsikter for 2025'
        }
    }
    
    return render_template('analysis/recommendation.html', 
                         title='Investeringsanbefalinger',
                         recommendations=recommendations,
                         market_insights=market_insights,
                         last_updated=datetime.now())

@analysis.route('/prediction')
@access_required  
def prediction():
    """AI prediction analysis page"""
    # Demo predictions data
    predictions_oslo = {
        'DNB.OL': {
            'price_prediction': 185.50,
            'confidence': 78,
            'trend': 'UP',
            'data_period': '60 dager',
            'trend_period': '5-30 dager',
            'last_price': 175.20,
            'next_price': 185.50,
            'change_percent': 5.88,
            'confidence': 'HIGH'
        },
        'EQNR.OL': {
            'price_prediction': 290.25,
            'confidence': 82,
            'trend': 'UP',
            'data_period': '60 dager', 
            'trend_period': '5-30 dager',
            'last_price': 278.40,
            'next_price': 290.25,
            'change_percent': 4.26,
            'confidence': 'HIGH'
        },
        'TEL.OL': {
            'price_prediction': 165.75,
            'confidence': 75,
            'trend': 'STABLE',
            'data_period': '60 dager',
            'trend_period': '5-30 dager',
            'last_price': 162.30,
            'next_price': 165.75,
            'change_percent': 2.13,
            'confidence': 'MEDIUM'
        }
    }
    
    # Demo global predictions data
    predictions_global = {
        'AAPL': {
            'price_prediction': 195.75,
            'confidence': 85,
            'trend': 'UP',
            'data_period': '60 dager',
            'trend_period': '5-30 dager',
            'last_price': 185.20,
            'next_price': 195.75,
            'change_percent': 5.69,
            'confidence': 'HIGH'
        },
        'TSLA': {
            'price_prediction': 245.80,
            'confidence': 79,
            'trend': 'UP',
            'data_period': '60 dager', 
            'trend_period': '5-30 dager',
            'last_price': 238.45,
            'next_price': 245.80,
            'change_percent': 3.08,
            'confidence': 'MEDIUM'
        },
        'MSFT': {
            'price_prediction': 425.30,
            'confidence': 88,
            'trend': 'UP',
            'data_period': '60 dager',
            'trend_period': '5-30 dager',
            'last_price': 415.25,
            'next_price': 425.30,
            'change_percent': 2.42,
            'confidence': 'HIGH'
        }
    }
    
    return render_template('analysis/prediction.html', 
                         title='AI Prognoser',
                         predictions_oslo=predictions_oslo,
                         predictions_global=predictions_global)

@analysis.route('/currency-overview')
@premium_required
def currency_overview():
    """Currency market overview"""
    from datetime import datetime
    
    # Use real currency data
    currencies = DataService.get_currency_overview() if DataService else {}
    return render_template('analysis/currency_overview.html', 
                         title='Valutaoversikt',
                         currencies=currencies,
                         now=datetime.now())

@analysis.route('/oslo-overview')
@access_required
def oslo_overview():
    """Oslo Børs market overview"""
    return render_template('analysis/oslo_overview.html', title='Oslo Børs Oversikt')

@analysis.route('/global-overview')
@access_required
def global_overview():
    """Global market overview"""
    return render_template('analysis/global_overview.html', title='Global Markeds Oversikt')

@analysis.route('/tradingview')
@access_required
def tradingview():
    """TradingView Charts Analysis"""
    symbol = request.args.get('symbol', 'AAPL')
    try:
        return render_template('analysis/tradingview.html', 
                             title='TradingView Charts',
                             symbol=symbol)
    except Exception as e:
        logger.error(f"Error loading TradingView page: {e}")
        return render_template('analysis/tradingview.html', 
                             title='TradingView Charts',
                             symbol=symbol,
                             error=True)
