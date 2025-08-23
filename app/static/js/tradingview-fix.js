/* TradingView Chart Fixes */

/* Enhanced loading detection */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 TradingView Chart Fix Script Loaded');
    
    // Wait for TradingView to load
    let attempts = 0;
    const maxAttempts = 20;
    
    function checkTradingView() {
        attempts++;
        console.log(`Checking TradingView availability (attempt ${attempts}/${maxAttempts})`);
        
        if (typeof TradingView !== 'undefined' && TradingView.widget) {
            console.log('✅ TradingView is ready');
            initializeTradingViewCharts();
        } else if (attempts >= maxAttempts) {
            console.warn('❌ TradingView failed to load - showing fallback');
            showTradingViewFallback();
        } else {
            setTimeout(checkTradingView, 500);
        }
    }
    
    checkTradingView();
});

function initializeTradingViewCharts() {
    const currentSymbol = '{{ symbol if symbol else "AAPL" }}';
    
    // Initialize main chart
    setTimeout(() => {
        loadMainChartFixed(currentSymbol);
    }, 1000);
}

function loadMainChartFixed(symbol) {
    const container = document.getElementById('tradingview_main_widget');
    if (!container) return;
    
    console.log(`Loading chart for symbol: ${symbol}`);
    
    try {
        // Format symbol properly
        let formattedSymbol = symbol;
        if (symbol.endsWith('.OL')) {
            formattedSymbol = `OSL:${symbol.replace('.OL', '')}`;
        } else if (!symbol.includes(':')) {
            formattedSymbol = `NASDAQ:${symbol}`;
        }
        
        console.log(`Formatted symbol: ${formattedSymbol}`);
        
        // Create widget with minimal configuration
        const widget = new TradingView.widget({
            width: "100%",
            height: 600,
            symbol: formattedSymbol,
            interval: "D",
            timezone: "Europe/Oslo",
            theme: "light",
            style: "1",
            locale: "en",
            toolbar_bg: "#f1f3f6",
            enable_publishing: false,
            allow_symbol_change: true,
            container_id: "tradingview_main_widget",
            
            onChartReady: function() {
                console.log('✅ TradingView chart loaded successfully');
            }
        });
        
        // Set timeout for loading detection
        setTimeout(() => {
            const iframe = container.querySelector('iframe');
            if (!iframe) {
                console.warn('No iframe found - showing fallback');
                showTradingViewFallback();
            } else {
                console.log('✅ TradingView iframe detected');
            }
        }, 8000);
        
    } catch (error) {
        console.error('Error loading TradingView:', error);
        showTradingViewFallback();
    }
}

function showTradingViewFallback() {
    const container = document.getElementById('tradingview_main_widget');
    if (!container) return;
    
    container.innerHTML = `
        <div class="alert alert-warning text-center p-4">
            <i class="bi bi-exclamation-triangle fs-1 mb-3"></i>
            <h4>TradingView Chart Ikke Tilgjengelig</h4>
            <p class="mb-3">TradingView charts kan ikke lastes for øyeblikket.</p>
            <p class="mb-3"><strong>Mulige årsaker:</strong></p>
            <ul class="list-unstyled mb-3">
                <li>• Ad blocker eller privacy extension</li>
                <li>• Nettverksbegrensninger</li>
                <li>• TradingView tjeneste utilgjengelig</li>
            </ul>
            <div class="d-flex gap-2 justify-content-center flex-wrap">
                <button class="btn btn-primary" onclick="location.reload()">
                    <i class="bi bi-arrow-clockwise"></i> Prøv igjen
                </button>
                <a href="https://www.tradingview.com" target="_blank" class="btn btn-outline-success">
                    <i class="bi bi-box-arrow-up-right"></i> Åpne TradingView
                </a>
            </div>
            <small class="text-muted mt-3 d-block">
                <strong>Tips:</strong> Prøv å deaktivere ad blocker eller bruk en annen nettleser
            </small>
        </div>
    `;
}
