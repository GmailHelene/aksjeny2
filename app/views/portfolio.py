from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.portfolio import Portfolio
from app.models.stock import Stock

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/portfolio/<int:portfolio_id>/add', methods=['GET', 'POST'])
@login_required
def portfolio_add(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if request.method == 'POST':
        try:
            ticker = request.form.get('ticker')
            if not ticker:
                flash('Ticker-symbol mangler', 'error')
                return redirect(url_for('portfolio_add', portfolio_id=portfolio_id))
            # Add stock to portfolio
            stock = PortfolioStock(
                portfolio_id=portfolio_id,
                ticker=ticker,
                quantity=request.form.get('quantity', 1),
                purchase_price=request.form.get('price', 0)
            )
            db.session.add(stock)
            db.session.commit()
            flash('Aksje lagt til!', 'success')
            return redirect(url_for('portfolio_detail', portfolio_id=portfolio_id))
        except Exception as e:
            db.session.rollback()
            flash('Kunne ikke legge til aksje', 'error')
    return render_template('portfolio/add.html', portfolio=portfolio)

@portfolio_bp.route('/portfolio/create', methods=['GET', 'POST'])
@login_required
def portfolio_create():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            if not name:
                flash('Porteføljenavn mangler', 'error')
                return render_template('portfolio/create.html')
            
            portfolio = Portfolio(
                name=name,
                user_id=current_user.id,
                description=request.form.get('description', '')
            )
            db.session.add(portfolio)
            db.session.commit()
            flash(f'Porteføljen "{name}" ble opprettet!', 'success')
            return redirect(url_for('portfolio_detail', portfolio_id=portfolio.id))
        except Exception as e:
            db.session.rollback()
            flash('Kunne ikke opprette portefølje i databasen. Prøv igjen.', 'error')
    
    return render_template('portfolio/create.html')