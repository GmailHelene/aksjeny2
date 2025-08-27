from flask import render_template, request
from app import app
from app.utils import get_stock_data, generate_demo_data

@app.route('/analysis/warren-buffett')
def warren_buffett():
    try:
        ticker = request.args.get('ticker', '').upper()
        if ticker:
            data = get_stock_data(ticker)
            if not data:
                data = generate_demo_data(ticker)
        else:
            data = None
        return render_template('analysis/warren-buffett.html', 
                             ticker=ticker,
                             data=data,
                             error=False)
    except Exception as e:
        app.logger.error(f"Warren Buffett analysis error: {str(e)}")
        return render_template('analysis/warren-buffett.html', 
                             ticker=ticker,
                             data=None,
                             error=True)