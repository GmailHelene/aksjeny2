
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.portfolio import Portfolio, PortfolioStock
from app.models.stock import Stock

portfolio_bp = Blueprint('portfolio_bp', __name__)

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
                shares=request.form.get('quantity', 1),
                purchase_price=request.form.get('price', 0)
            )
            db.session.add(stock)
            db.session.commit()
            flash('Aksje lagt til!', 'success')
            return redirect(url_for('portfolio_bp.portfolio_detail', portfolio_id=portfolio_id))
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
            return redirect(url_for('portfolio_bp.portfolio_detail', portfolio_id=portfolio.id))
        except Exception as e:
            db.session.rollback()
            flash('Kunne ikke opprette portefølje i databasen. Prøv igjen.', 'error')
    
    return render_template('portfolio/create.html')


# --- Portfolio Detail View ---
@portfolio_bp.route('/portfolio/<int:portfolio_id>')
@login_required
def portfolio_detail(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    # Build holdings list with required fields for template
    holdings = []
    for stock in portfolio.stocks:
        # Get current price and company name
        try:
            from app.services.data_service import DataService
            stock_info = DataService.get_stock_info(stock.ticker)
            current_price = stock_info.get('regularMarketPrice', 0) if stock_info else 0
            company_name = stock_info.get('longName', stock.ticker) if stock_info else stock.ticker
        except Exception:
            current_price = 0
            company_name = stock.ticker
        market_value = current_price * stock.shares if current_price else 0
        average_price = stock.purchase_price or 0
        unrealized_gain = (current_price - average_price) * stock.shares if average_price else 0
        unrealized_gain_percent = ((current_price - average_price) / average_price * 100) if average_price else 0
        holdings.append({
            'id': stock.id,
            'symbol': stock.ticker,
            'company_name': company_name,
            'quantity': stock.shares,
            'average_price': average_price,
            'current_price': current_price,
            'market_value': market_value,
            'unrealized_gain': unrealized_gain,
            'unrealized_gain_percent': unrealized_gain_percent
        })
    # Calculate total value and return
    total_value = sum(h['market_value'] for h in holdings)
    total_return = sum(h['unrealized_gain'] for h in holdings)
    return_percentage = (total_return / sum(h['average_price'] * h['quantity'] for h in holdings if h['average_price']) * 100) if holdings and sum(h['average_price'] * h['quantity'] for h in holdings if h['average_price']) > 0 else 0
    return render_template(
        'portfolio/view.html',
        portfolio=portfolio,
        holdings=holdings,
        total_value=total_value,
        total_return=total_return,
        return_percentage=return_percentage
    )