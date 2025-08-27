from flask import render_template, request, jsonify
from app import app
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

@app.route('/stocks/compare')
def compare():
    try:
        tickers = request.args.getlist('tickers')
        # Filter out empty tickers
        tickers = [t for t in tickers if t and t.strip()]
        
        if not tickers:
            flash('Velg minst én aksje for sammenligning', 'warning')
            return render_template('stocks/compare.html', data=None)
        
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
                             tickers=tickers,
                             data=None,
                             error=True)