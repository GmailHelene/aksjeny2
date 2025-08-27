
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.utils.market_intel_utils import get_market_intelligence_data, get_analyst_coverage_data

# Opprett blueprint
external_data_bp = Blueprint('external_data', __name__)

@external_data_bp.route('/external-data/market-intelligence')
def market_intelligence():
    if current_user.is_authenticated:
        data = get_market_intelligence_data(real=True)
    else:
        data = get_market_intelligence_data(real=False)
    return render_template('external_data/market_intelligence.html', data=data)

@external_data_bp.route('/external-data/analyst-coverage')
def analyst_coverage():
    if current_user.is_authenticated:
        data = get_analyst_coverage_data(real=True)
    else:
        data = get_analyst_coverage_data(real=False)
    return render_template('external_data/analyst_coverage.html', data=data)
