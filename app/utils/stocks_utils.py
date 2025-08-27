def get_comparison_data(tickers):
    from flask_login import current_user
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        from app.services.data_service import DataService
        chart_data = {}
        current_prices = {}
        price_changes = {}
        volatility = {}
        volumes = {}
        correlations = {}
        betas = {}
        ticker_names = {}
        for ticker in tickers:
            try:
                stock_info = DataService.get_stock_info(ticker)
                if stock_info:
                    # Example: chart_data could be historical prices if available
                    chart_data[ticker] = stock_info.get('historical', [])
                    current_prices[ticker] = stock_info.get('last_price', 0)
                    price_changes[ticker] = stock_info.get('change_percent', 0)
                    volatility[ticker] = stock_info.get('volatility', 0)
                    volumes[ticker] = stock_info.get('volume', 0)
                    betas[ticker] = stock_info.get('beta', 0)
                    ticker_names[ticker] = stock_info.get('name', ticker)
                else:
                    chart_data[ticker] = []
                    current_prices[ticker] = 0
                    price_changes[ticker] = 0
                    volatility[ticker] = 0
                    volumes[ticker] = 0
                    betas[ticker] = 0
                    ticker_names[ticker] = ticker
            except Exception:
                chart_data[ticker] = []
                current_prices[ticker] = 0
                price_changes[ticker] = 0
                volatility[ticker] = 0
                volumes[ticker] = 0
                betas[ticker] = 0
                ticker_names[ticker] = ticker
        # Correlations: placeholder, should be calculated from historical data
        for t1 in tickers:
            for t2 in tickers:
                if t1 != t2:
                    correlations[(t1, t2)] = 0  # TODO: Implement real correlation calculation
        return {
            'chart_data': chart_data,
            'current_prices': current_prices,
            'price_changes': price_changes,
            'volatility': volatility,
            'volumes': volumes,
            'correlations': correlations,
            'betas': betas,
            'ticker_names': ticker_names
        }
    else:
        return generate_demo_comparison(tickers)

def generate_demo_comparison(tickers):
    # Dummy implementation for demo mode
    # Return static demo data for non-authenticated users
    chart_data = {}
    current_prices = {}
    price_changes = {}
    volatility = {}
    volumes = {}
    correlations = {}
    betas = {}
    ticker_names = {}
    for ticker in tickers:
        chart_data[ticker] = [
            {'date': '2023-01-01', 'close': 100, 'volume': 1000},
            {'date': '2023-01-02', 'close': 105, 'volume': 1200},
            {'date': '2023-01-03', 'close': 110, 'volume': 1100},
            {'date': '2023-01-04', 'close': 115, 'volume': 1300},
            {'date': '2023-01-05', 'close': 120, 'volume': 1250}
        ]
        current_prices[ticker] = 120
        price_changes[ticker] = 5
        volatility[ticker] = 0.02
        volumes[ticker] = 1250
        betas[ticker] = 1.0
        ticker_names[ticker] = ticker
    for t1 in tickers:
        for t2 in tickers:
            if t1 != t2:
                correlations[(t1, t2)] = 0
    return {
        'chart_data': chart_data,
        'current_prices': current_prices,
        'price_changes': price_changes,
        'volatility': volatility,
        'volumes': volumes,
        'correlations': correlations,
        'betas': betas,
        'ticker_names': ticker_names
    }
