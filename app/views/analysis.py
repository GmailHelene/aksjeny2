from flask import render_template, request
from app.utils.analysis_utils import get_stock_data, generate_demo_data

def init_analysis_routes(app):
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

    @app.route('/analysis/short-analysis', methods=['GET', 'POST'])
    def short_analysis():
        try:
            if request.method == 'POST':
                ticker = request.form.get('ticker', '').upper()
            else:
                ticker = request.args.get('ticker', '').upper()
            
            if ticker:
                data = get_stock_data(ticker)
                if not data:
                    data = generate_demo_data(ticker)
            else:
                data = None
            return render_template('analysis/short-analysis.html', 
                                 ticker=ticker,
                                 stock_data=data,
                                 error=False)
        except Exception as e:
            app.logger.error(f"Short analysis error: {str(e)}")
        return render_template('analysis/short-analysis.html', 
                             ticker=ticker,
                             stock_data=None,
                             error=True)