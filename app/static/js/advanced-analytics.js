/**
 * Advanced Analytics Module
 * Handles ML predictions, portfolio optimization, and risk management
 */

class AdvancedAnalytics {
    constructor() {
        this.baseURL = '/advanced-analytics/api';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // ML Prediction listeners
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-ml-predict]')) {
                this.handleMLPrediction(e.target);
            }
            if (e.target.matches('[data-portfolio-optimize]')) {
                this.handlePortfolioOptimization(e.target);
            }
            if (e.target.matches('[data-risk-analysis]')) {
                this.handleRiskAnalysis(e.target);
            }
        });
    }

    // ML Prediction Methods
    async predictStock(symbol, days = 30) {
        try {
            const response = await fetch(`${this.baseURL}/ml/predict/${symbol}?days=${days}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayPrediction(data.prediction);
                return data.prediction;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Prediction error:', error);
            this.showError('Kunne ikke generere prediksjon');
        }
    }

    async batchPredict(symbols, days = 30) {
        try {
            const response = await fetch(`${this.baseURL}/ml/batch-predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symbols, days })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayBatchPredictions(data.predictions);
                return data.predictions;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Batch prediction error:', error);
            this.showError('Kunne ikke generere batch-prediksjoner');
        }
    }

    async getMarketAnalysis() {
        try {
            const response = await fetch(`${this.baseURL}/ml/market-analysis`);
            const data = await response.json();
            
            if (data.success) {
                this.displayMarketAnalysis(data.analysis);
                return data.analysis;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Market analysis error:', error);
            this.showError('Kunne ikke hente markedsanalyse');
        }
    }

    // Portfolio Optimization Methods
    async optimizePortfolio(symbols, weights = null, method = 'sharpe') {
        try {
            const response = await fetch(`${this.baseURL}/portfolio/optimize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symbols, weights, method })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayOptimization(data.optimization);
                return data.optimization;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Portfolio optimization error:', error);
            this.showError('Kunne ikke optimalisere portefølje');
        }
    }

    async generateEfficientFrontier(symbols, numPortfolios = 10000) {
        try {
            const response = await fetch(`${this.baseURL}/portfolio/efficient-frontier`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symbols, num_portfolios: numPortfolios })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayEfficientFrontier(data.frontier);
                return data.frontier;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Efficient frontier error:', error);
            this.showError('Kunne ikke generere effisient frontier');
        }
    }

    async rebalancePortfolio(currentPortfolio, targetAllocation) {
        try {
            const response = await fetch(`${this.baseURL}/portfolio/rebalance`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    current_portfolio: currentPortfolio,
                    target_allocation: targetAllocation 
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayRebalancing(data.rebalancing);
                return data.rebalancing;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Rebalancing error:', error);
            this.showError('Kunne ikke rebalansere portefølje');
        }
    }

    // Risk Management Methods
    async calculatePortfolioRisk(portfolio, timeframe = 252) {
        try {
            const response = await fetch(`${this.baseURL}/risk/portfolio-risk`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ portfolio, timeframe })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayRiskMetrics(data.risk_metrics);
                return data.risk_metrics;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Risk calculation error:', error);
            this.showError('Kunne ikke beregne porteføljerisiko');
        }
    }

    async performVarAnalysis(portfolio, confidenceLevel = 0.95, timeHorizon = 1) {
        try {
            const response = await fetch(`${this.baseURL}/risk/var-analysis`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    portfolio,
                    confidence_level: confidenceLevel,
                    time_horizon: timeHorizon 
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayVarAnalysis(data.var_analysis);
                return data.var_analysis;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('VaR analysis error:', error);
            this.showError('Kunne ikke utføre VaR-analyse');
        }
    }

    async stressTestPortfolio(portfolio, scenario = 'market_crash') {
        try {
            const response = await fetch(`${this.baseURL}/risk/stress-test`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ portfolio, scenario })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayStressTest(data.stress_test);
                return data.stress_test;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Stress test error:', error);
            this.showError('Kunne ikke utføre stresstest');
        }
    }

    async runMonteCarloSimulation(portfolio, simulations = 10000, timeHorizon = 252) {
        try {
            const response = await fetch(`${this.baseURL}/risk/monte-carlo`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    portfolio,
                    simulations,
                    time_horizon: timeHorizon 
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayMonteCarloResults(data.monte_carlo);
                return data.monte_carlo;
            } else {
                throw new Error(data.message);
            }
        } catch (error) {
            console.error('Monte Carlo simulation error:', error);
            this.showError('Kunne ikke kjøre Monte Carlo-simulering');
        }
    }

    // Display Methods
    displayPrediction(prediction) {
        const container = document.getElementById('ml-prediction-results');
        if (!container) return;

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>ML Prediksjon - ${prediction.symbol}</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Nåværende pris:</strong> $${prediction.current_price?.toFixed(2) || 'N/A'}</p>
                            <p><strong>Predikert pris:</strong> $${prediction.predicted_price?.toFixed(2) || 'N/A'}</p>
                            <p><strong>Forventet endring:</strong> ${prediction.price_change_percent?.toFixed(2) || 'N/A'}%</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Konfidens:</strong> ${(prediction.confidence * 100)?.toFixed(1) || 'N/A'}%</p>
                            <p><strong>Trend:</strong> ${prediction.trend || 'N/A'}</p>
                            <p><strong>Volatilitet:</strong> ${prediction.volatility?.toFixed(3) || 'N/A'}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayOptimization(optimization) {
        const container = document.getElementById('portfolio-optimization-results');
        if (!container) return;

        const weightsHtml = Object.entries(optimization.optimal_weights || {})
            .map(([symbol, weight]) => `
                <tr>
                    <td>${symbol}</td>
                    <td>${(weight * 100).toFixed(2)}%</td>
                </tr>
            `).join('');

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Porteføljeoptimalisering</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Optimal Allokering</h6>
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Symbol</th>
                                        <th>Vekt</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${weightsHtml}
                                </tbody>
                            </table>
                        </div>
                        <div class="col-md-6">
                            <h6>Porteføljemetrikker</h6>
                            <p><strong>Forventet avkastning:</strong> ${(optimization.expected_return * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Volatilitet:</strong> ${(optimization.volatility * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Sharpe Ratio:</strong> ${optimization.sharpe_ratio?.toFixed(3) || 'N/A'}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayRiskMetrics(riskMetrics) {
        const container = document.getElementById('risk-analysis-results');
        if (!container) return;

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Risikoanalyse</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Volatilitetsmetrikker</h6>
                            <p><strong>Volatilitet:</strong> ${(riskMetrics.volatility * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Beta:</strong> ${riskMetrics.beta?.toFixed(3) || 'N/A'}</p>
                            <p><strong>Treynor Ratio:</strong> ${riskMetrics.treynor_ratio?.toFixed(3) || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Drawdown Metrikker</h6>
                            <p><strong>Max Drawdown:</strong> ${(riskMetrics.max_drawdown * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>VaR (95%):</strong> ${(riskMetrics.var_95 * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>CVaR (95%):</strong> ${(riskMetrics.cvar_95 * 100)?.toFixed(2) || 'N/A'}%</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayBatchPredictions(predictions) {
        const container = document.getElementById('ml-prediction-results');
        if (!container) return;

        const predictionsHtml = Object.entries(predictions).map(([symbol, prediction]) => `
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title">${symbol}</h6>
                        <p><strong>Nåværende pris:</strong> $${prediction.current_price?.toFixed(2) || 'N/A'}</p>
                        <p><strong>Predikert pris:</strong> $${prediction.predicted_price?.toFixed(2) || 'N/A'}</p>
                        <p><strong>Endring:</strong> <span class="${prediction.price_change_percent >= 0 ? 'text-success' : 'text-danger'}">${prediction.price_change_percent?.toFixed(2) || 'N/A'}%</span></p>
                        <p><strong>Konfidens:</strong> ${(prediction.confidence * 100)?.toFixed(1) || 'N/A'}%</p>
                    </div>
                </div>
            </div>
        `).join('');

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Batch Prediksjoner</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        ${predictionsHtml}
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayMarketAnalysis(analysis) {
        const container = document.getElementById('ml-prediction-results');
        if (!container) return;

        const sectorHtml = Object.entries(analysis.sector_performance || {})
            .map(([sector, performance]) => `
                <tr>
                    <td>${sector}</td>
                    <td class="${performance >= 0 ? 'text-success' : 'text-danger'}">${performance?.toFixed(2) || 'N/A'}%</td>
                </tr>
            `).join('');

        const trendsHtml = (analysis.market_trends || [])
            .map(trend => `<li>${trend}</li>`)
            .join('');

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Markedsanalyse</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Markedsindikatorer</h6>
                            <p><strong>Sentiment:</strong> ${analysis.overall_sentiment || 'N/A'}</p>
                            <p><strong>Volatilitet:</strong> ${(analysis.market_volatility * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Frykt & Grådighet Index:</strong> ${analysis.fear_greed_index || 'N/A'}</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Sektorutvikling</h6>
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Sektor</th>
                                        <th>Utvikling</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${sectorHtml}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="mt-3">
                        <h6>Markedstrender</h6>
                        <ul>
                            ${trendsHtml}
                        </ul>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayEfficientFrontier(frontier) {
        const container = document.getElementById('portfolio-optimization-results');
        if (!container) return;

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Effisient Frontier</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-8">
                            <div id="efficient-frontier-chart" style="height: 400px; background: #f8f9fa; display: flex; align-items: center; justify-content: center;">
                                <p class="text-muted">Grafisk fremstilling av effisient frontier ville vises her</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <h6>Optimal Portefølje</h6>
                            <p><strong>Risiko:</strong> ${(frontier.optimal_portfolio?.risk * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Avkastning:</strong> ${(frontier.optimal_portfolio?.return * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Sharpe Ratio:</strong> ${frontier.optimal_portfolio?.sharpe_ratio?.toFixed(3) || 'N/A'}</p>
                            <small class="text-muted">Basert på ${frontier.data?.length || 0} porteføljer</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayRebalancing(rebalancing) {
        const container = document.getElementById('portfolio-optimization-results');
        if (!container) return;

        const actionsHtml = (rebalancing.actions || [])
            .map(action => `
                <tr>
                    <td>${action.symbol}</td>
                    <td class="${action.action === 'buy' ? 'text-success' : 'text-danger'}">${action.action.toUpperCase()}</td>
                    <td>${action.amount_percent?.toFixed(2) || 'N/A'}%</td>
                    <td>$${action.estimated_cost?.toFixed(2) || 'N/A'}</td>
                </tr>
            `).join('');

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Portefølje Rebalansering</h5>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <p><strong>Totale transaksjoner:</strong> ${rebalancing.total_transactions || 0}</p>
                            <p><strong>Estimert kostnad:</strong> $${rebalancing.estimated_cost?.toFixed(2) || 'N/A'}</p>
                        </div>
                    </div>
                    <h6>Anbefalte handlinger</h6>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Handling</th>
                                <th>Beløp</th>
                                <th>Kostnad</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${actionsHtml}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayVarAnalysis(varAnalysis) {
        const container = document.getElementById('risk-analysis-results');
        if (!container) return;

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>VaR Analyse</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Value at Risk (${(varAnalysis.confidence_level * 100)?.toFixed(0) || 'N/A'}%)</h6>
                            <p><strong>Historisk VaR:</strong> ${(varAnalysis.historical_var * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Parametrisk VaR:</strong> ${(varAnalysis.parametric_var * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Monte Carlo VaR:</strong> ${(varAnalysis.monte_carlo_var * 100)?.toFixed(2) || 'N/A'}%</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Ytterligere Metrikker</h6>
                            <p><strong>Expected Shortfall:</strong> ${(varAnalysis.expected_shortfall * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Tidshorisont:</strong> ${varAnalysis.time_horizon || 'N/A'} dag(er)</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayStressTest(stressTest) {
        const container = document.getElementById('risk-analysis-results');
        if (!container) return;

        const assetImpactsHtml = Object.entries(stressTest.asset_impacts || {})
            .map(([symbol, impact]) => `
                <tr>
                    <td>${symbol}</td>
                    <td class="${impact >= 0 ? 'text-success' : 'text-danger'}">${(impact * 100)?.toFixed(2) || 'N/A'}%</td>
                </tr>
            `).join('');

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Stresstest - ${stressTest.scenario || 'N/A'}</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Scenariodetaljer</h6>
                            <p><strong>Beskrivelse:</strong> ${stressTest.description || 'N/A'}</p>
                            <p><strong>Porteføljeimpakt:</strong> <span class="${stressTest.portfolio_impact >= 0 ? 'text-success' : 'text-danger'}">${(stressTest.portfolio_impact * 100)?.toFixed(2) || 'N/A'}%</span></p>
                            <p><strong>Value at Risk:</strong> ${(stressTest.value_at_risk * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Estimert gjenopprettingstid:</strong> ${stressTest.recovery_time_days || 'N/A'} dager</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Aktivaimpakt</h6>
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Symbol</th>
                                        <th>Påvirkning</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${assetImpactsHtml}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayMonteCarloResults(monteCarlo) {
        const container = document.getElementById('risk-analysis-results');
        if (!container) return;

        const html = `
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Monte Carlo Simulering</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Simuleringsresultater</h6>
                            <p><strong>Antall simuleringer:</strong> ${monteCarlo.simulations || 'N/A'}</p>
                            <p><strong>Tidshorisont:</strong> ${monteCarlo.time_horizon_days || 'N/A'} dager</p>
                            <p><strong>Gjennomsnittlig avkastning:</strong> ${(monteCarlo.mean_return * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Standardavvik:</strong> ${(monteCarlo.std_deviation * 100)?.toFixed(2) || 'N/A'}%</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Sannsynlighetsfordeling</h6>
                            <p><strong>5. persentil:</strong> ${(monteCarlo.percentiles?.['5th'] * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>25. persentil:</strong> ${(monteCarlo.percentiles?.['25th'] * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>Median:</strong> ${(monteCarlo.percentiles?.['50th'] * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>75. persentil:</strong> ${(monteCarlo.percentiles?.['75th'] * 100)?.toFixed(2) || 'N/A'}%</p>
                            <p><strong>95. persentil:</strong> ${(monteCarlo.percentiles?.['95th'] * 100)?.toFixed(2) || 'N/A'}%</p>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col-12">
                            <h6>Risikosannsynligheter</h6>
                            <p><strong>Sannsynlighet for positiv avkastning:</strong> ${(monteCarlo.probability_positive * 100)?.toFixed(1) || 'N/A'}%</p>
                            <p><strong>Sannsynlighet for >5% tap:</strong> ${(monteCarlo.probability_loss_5pct * 100)?.toFixed(1) || 'N/A'}%</p>
                            <p><strong>Sannsynlighet for >10% tap:</strong> ${(monteCarlo.probability_loss_10pct * 100)?.toFixed(1) || 'N/A'}%</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    // Event Handlers
    handleMLPrediction(element) {
        const symbol = element.dataset.symbol;
        const days = parseInt(element.dataset.days) || 30;
        
        if (symbol) {
            this.predictStock(symbol, days);
        }
    }

    handlePortfolioOptimization(element) {
        const symbols = element.dataset.symbols?.split(',') || [];
        const method = element.dataset.method || 'sharpe';
        
        if (symbols.length > 0) {
            this.optimizePortfolio(symbols, null, method);
        }
    }

    handleRiskAnalysis(element) {
        const portfolioData = element.dataset.portfolio;
        
        if (portfolioData) {
            try {
                const portfolio = JSON.parse(portfolioData);
                this.calculatePortfolioRisk(portfolio);
            } catch (error) {
                console.error('Invalid portfolio data:', error);
                this.showError('Ugyldig porteføljedata');
            }
        }
    }

    // Utility Methods
    showError(message) {
        // Show error message to user
        const errorContainer = document.getElementById('error-messages');
        if (errorContainer) {
            errorContainer.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        } else {
            console.error('Error:', message);
        }
    }

    showSuccess(message) {
        // Show success message to user
        const successContainer = document.getElementById('success-messages');
        if (successContainer) {
            successContainer.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.advancedAnalytics = new AdvancedAnalytics();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedAnalytics;
}
