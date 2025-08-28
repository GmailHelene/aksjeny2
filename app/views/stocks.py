from flask import render_template, request, jsonify, current_app
from app.utils.stocks_utils import get_comparison_data, generate_demo_comparison

def init_stocks_routes(app):
    """Initialize stock routes with app instance"""
    
    @app.route('/stocks/compare')
    def stocks_compare():
        """Compare multiple stocks"""
        try:
            tickers = request.args.getlist('tickers')
            # Remove empty strings
            tickers = [t for t in tickers if t]
            
            if not tickers:
                tickers = ['EQNR.OL', 'DNB.OL']
            comparison_data = get_comparison_data(tickers)
            if not comparison_data:
                comparison_data = generate_demo_comparison(tickers)
            return render_template('stocks/compare.html',
                                 tickers=tickers,
                                 error=False,
                                 **comparison_data)
                                 
        except Exception as e:
            current_app.logger.error(f"Compare error: {str(e)}")
            return render_template('stocks/compare.html',
                                 error=True,
                                 message="Kunne ikke sammenligne aksjer")

    @app.route('/stocks/details/<symbol>')
    def details(symbol):
        """Display detailed stock information"""
        try:
            # Get stock data
            stock_data = get_comparison_data([symbol])
            if not stock_data or symbol not in stock_data.get('chart_data', {}):
                # Generate demo data
                stock_data = generate_demo_comparison([symbol])
            
            chart_data = stock_data.get('chart_data', {}).get(symbol, [])
            current_price = stock_data.get('current_prices', {}).get(symbol, 0)
            price_change = stock_data.get('price_changes', {}).get(symbol, 0)
            
            # Generate technical indicators
            rsi = 65.5  # Demo RSI
            macd = 1.23  # Demo MACD
            
            return render_template('stocks/details.html',
                                 symbol=symbol,
                                 chart_data=chart_data,
                                 current_price=current_price,
                                 price_change=price_change,
                                 rsi=rsi,
                                 macd=macd,
                                 error=False)
        except Exception as e:
            current_app.logger.error(f"Details error: {str(e)}")
            return render_template('stocks/details.html',
                                 symbol=symbol,
                                 error=True,
                                 message="Kunne ikke laste aksjedetaljer")