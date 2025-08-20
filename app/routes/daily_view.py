from flask import Blueprint, render_template, jsonify
from datetime import datetime, timedelta
import random

# Create Daily View Blueprint
daily_view = Blueprint('daily_view', __name__, url_prefix='/daily-view')

@daily_view.route('/')
def index():
    """Daily Market View - Financial Blog Style"""
    today = datetime.now()
    
    # Simulated daily market insights
    market_insights = [
        {
            'title': 'Oslo Børs åpner sterkt etter positive olje-nyheter',
            'summary': 'Hovedindeksen opp 1.2% i åpningen etter at Brent crude steg til $86 per fat. Equinor og Aker leder oppgangen.',
            'time': '09:15',
            'category': 'Markedsåpning',
            'impact': 'Positiv',
            'affected_stocks': ['EQNR', 'AKER', 'PGS']
        },
        {
            'title': 'DNB rapporterer sterkere enn ventet kvartalstall',
            'summary': 'Bankgiganten overrasket positivt med Q3-tall. Inntektene opp 8% og kredittapene lavere enn fryktet.',
            'time': '08:30',
            'category': 'Kvartalstall', 
            'impact': 'Meget Positiv',
            'affected_stocks': ['DNB', 'SPOG', 'HELG']
        },
        {
            'title': 'Regjeringen foreslår nye skatteregler for olje',
            'summary': 'Finansdepartementet lanserer høringsutkast om økt særskatt. Oljeaksjer under press i førhandelen.',
            'time': '07:45',
            'category': 'Politikk',
            'impact': 'Negativ',
            'affected_stocks': ['EQNR', 'AKER', 'VEI', 'PGS']
        }
    ]
    
    # Market movers
    top_movers = {
        'gainers': [
            {'ticker': 'DNB', 'change': '+3.45%', 'price': '234.50 NOK'},
            {'ticker': 'EQNR', 'change': '+2.87%', 'price': '298.30 NOK'},
            {'ticker': 'MOWI', 'change': '+1.95%', 'price': '189.75 NOK'}
        ],
        'losers': [
            {'ticker': 'TEL', 'change': '-2.10%', 'price': '156.80 NOK'},
            {'ticker': 'YAR', 'change': '-1.55%', 'price': '445.20 NOK'},
            {'ticker': 'REC', 'change': '-1.32%', 'price': '78.90 NOK'}
        ]
    }
    
    # Economic calendar
    economic_events = [
        {
            'time': '14:30',
            'event': 'Norges Bank rentebeslutning',
            'importance': 'Høy',
            'expected': '4.25%',
            'previous': '4.25%'
        },
        {
            'time': '16:00',
            'event': 'USA arbeidsløshetstall',
            'importance': 'Medium',
            'expected': '3.8%',
            'previous': '3.9%'
        }
    ]
    
    return render_template('daily_view/index.html',
                         insights=market_insights,
                         movers=top_movers,
                         events=economic_events,
                         date=today)

@daily_view.route('/analysis/<date>')
def daily_analysis(date):
    """Deep dive analysis for a specific day"""
    # Simulated deep analysis
    analysis = {
        'market_summary': 'Oslo Børs hadde en blandet dag med olje- og bankaksjer som drivkrefter...',
        'sector_performance': [
            {'sector': 'Olje & Gass', 'performance': '+2.3%', 'leader': 'EQNR'},
            {'sector': 'Bank & Finans', 'performance': '+1.8%', 'leader': 'DNB'},
            {'sector': 'Telekom', 'performance': '-1.2%', 'leader': 'TEL'},
            {'sector': 'Oppdrett', 'performance': '+0.8%', 'leader': 'MOWI'}
        ],
        'key_events': [
            'Brent crude opp 2.1% til $86.45',
            'USD/NOK ned 0.3% til 10.82',
            'Norges Bank holder renten uendret på 4.25%'
        ]
    }
    
    return render_template('daily_view/analysis.html', 
                         analysis=analysis, 
                         date=date)

@daily_view.route('/api/live-updates')
def api_live_updates():
    """API for live market updates"""
    updates = [
        {
            'time': datetime.now().strftime('%H:%M'),
            'message': f'EQNR opp {random.uniform(0.5, 2.5):.1f}% på økt oljepris',
            'type': 'positive'
        },
        {
            'time': (datetime.now() - timedelta(minutes=5)).strftime('%H:%M'),
            'message': f'Oslo Børs hovedindeks +{random.uniform(0.2, 1.5):.1f}%',
            'type': 'neutral'
        }
    ]
    
    return jsonify(updates)
