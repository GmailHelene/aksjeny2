from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from . import price_alerts_bp
from ..models import PriceAlert, db
from ..services import data_service

@price_alerts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            symbol = request.form.get('symbol', '').upper()
            alert_type = request.form.get('alert_type')
            target_price = request.form.get('target_price', type=float)
            
            # Validate input
            if not symbol or not alert_type or not target_price:
                flash('Alle felt må fylles ut', 'error')
                return redirect(url_for('price_alerts.create'))
            
            # Get current stock price
            stock = data_service.get_stock_data(symbol)
            if not stock:
                flash(f'Kunne ikke finne aksje med symbol {symbol}', 'error')
                return redirect(url_for('price_alerts.create'))
            
            # Create price alert
            alert = PriceAlert(
                user_id=current_user.id,
                symbol=symbol,
                alert_type=alert_type,
                target_price=target_price,
                current_price=stock.current_price,
                is_active=True
            )
            
            db.session.add(alert)
            db.session.commit()
            
            flash(f'Prisvarsel opprettet for {symbol}', 'success')
            return redirect(url_for('price_alerts.list'))
            
        except Exception as e:
            current_app.logger.error(f"Error creating price alert: {str(e)}")
            db.session.rollback()
            flash('Kunne ikke opprette prisvarsel, prøv igjen', 'error')
            return redirect(url_for('price_alerts.create'))
    
    # GET request - show form
    return render_template('price_alerts/create.html')