
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.utils.market_intel_utils import get_market_intelligence_data, get_analyst_coverage_data

# Opprett blueprint
external_data_bp = Blueprint('external_data', __name__)

@external_data_bp.route('/external-data/market-intelligence')
def market_intelligence():
    try:
        if current_user.is_authenticated:
            data = get_market_intelligence_data(real=True)
        else:
            data = get_market_intelligence_data(real=False)
        
        # Ensure data is a list
        if not isinstance(data, list):
            data = []
            
        return render_template('external_data/market_intelligence.html', data=data)
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Market intelligence error: {str(e)}")
        # Fallback for errors with proper data structure
        data = [{'title': 'Market Intelligence', 'summary': 'Kunne ikke hente markedsdata. Vennligst prøv igjen senere.'}]
        return render_template('external_data/market_intelligence.html', data=data)

@external_data_bp.route('/external-data/analyst-coverage')
def analyst_coverage():
    try:
        if current_user.is_authenticated:
            data = get_analyst_coverage_data(real=True)
        else:
            data = get_analyst_coverage_data(real=False)
            
        # Ensure data is a list  
        if not isinstance(data, list):
            data = []
            
        return render_template('external_data/analyst_coverage.html', analyst_coverage=data)
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Analyst coverage error: {str(e)}")
        # Fallback for errors with proper data structure
        data = [{'company': 'N/A', 'symbol': 'N/A', 'recommendation': 'Kunne ikke hente analytikerdata', 'firm': 'System', 'date': 'N/A'}]
        return render_template('external_data/analyst_coverage.html', analyst_coverage=data)
        # Fallback for errors
        data = {'EQNR': {'consensus': {'rating': 'Hold', 'avg_target_price': 0, 'num_analysts': 0}, 'recommendations': []}}
        return render_template('external_data/analyst_coverage.html', analyst_coverage=data)
