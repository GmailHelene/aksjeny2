def get_comparison_data(tickers):
    # Dummy implementation: Replace with real data fetching logic
    chart_data = []
    current_prices = {}
    price_changes = {}
    volatility = {}
    volumes = {}
    correlations = {}
    betas = {}
    ticker_names = {}
    for ticker in tickers:
        chart_data.append({
            'ticker': ticker,
            'prices': [100, 105, 110, 115, 120],
            'volumes': [1000, 1200, 1100, 1300, 1250]
        })
        current_prices[ticker] = 120.0
        price_changes[ticker] = 15.0
        volatility[ticker] = 2.5
        volumes[ticker] = 1200
        correlations[ticker] = {tickers[0]: 1.0}
        betas[ticker] = 1.0
        ticker_names[ticker] = ticker
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

def generate_demo_comparison(tickers):
    # Dummy implementation for demo mode
    return get_comparison_data(tickers)
