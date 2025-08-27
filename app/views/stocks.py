from flask import render_template, request, jsonify
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

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
                return render_template('stocks/compare.html', 
                                     error=True,
                                     message="Ingen aksjer valgt for sammenligning")
            
            comparison_data = get_comparison_data(tickers)
            if not comparison_data:
                comparison_data = generate_demo_comparison(tickers)
            
            return render_template('stocks/compare.html',
                                 tickers=tickers,
                                 data=comparison_data,
                                 error=False)
                                 
        except Exception as e:
            app.logger.error(f"Compare error: {str(e)}")
            return render_template('stocks/compare.html',
                                 error=True,
                                 message="Kunne ikke sammenligne aksjer")