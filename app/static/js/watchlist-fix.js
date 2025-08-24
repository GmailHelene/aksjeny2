/**
 * Watchlist functionality and state management
 */

// Add stock to watchlist with enhanced error handling
async function addToWatchlist(symbol, name) {
    try {
        // Show loading state
        const button = document.querySelector(`[data-add-watchlist="${symbol}"]`);
        if (button) {
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Legger til...';
        }

        // Call API to add to watchlist
        const response = await fetch('/watchlist/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': window.csrfToken
            },
            body: JSON.stringify({ symbol, name })
        });

        const data = await response.json();

        if (response.ok) {
            // Update UI
            if (button) {
                button.innerHTML = '<i class="fas fa-check"></i> Lagt til';
                button.classList.remove('btn-primary');
                button.classList.add('btn-success');
            }
            
            // Show success message
            showToast('Aksjen er lagt til i din overvåkningsliste', 'success');
            
            // Update watchlist count if it exists
            const countElement = document.querySelector('#watchlist-count');
            if (countElement) {
                const currentCount = parseInt(countElement.textContent) || 0;
                countElement.textContent = currentCount + 1;
            }

            // Update achievement stats
            fetch('/achievements/api/update_stat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': window.csrfToken
                },
                body: JSON.stringify({
                    type: 'favorites',
                    increment: 1
                })
            });

            return true;
        } else {
            throw new Error(data.error || 'Kunne ikke legge til i overvåkningsliste');
        }
    } catch (error) {
        console.error('Error adding to watchlist:', error);
        
        // Reset button state
        if (button) {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-plus"></i> Legg til';
        }
        
        // Show error message
        showToast(error.message || 'Kunne ikke legge til i overvåkningsliste. Prøv igjen senere.', 'error');
        
        return false;
    }
}

// Create price alert with enhanced validation
async function createPriceAlert(symbol, currentPrice) {
    try {
        // Get price from user with validation
        const price = parseFloat(prompt(`Sett prisvarsel for ${symbol}\nNåværende kurs: ${currentPrice} NOK\n\nAngi målpris:`));
        
        if (isNaN(price) || price <= 0) {
            showToast('Vennligst angi en gyldig pris', 'warning');
            return;
        }

        // Validate price is different enough from current
        const priceDiff = Math.abs(price - currentPrice) / currentPrice;
        if (priceDiff < 0.01) { // 1% minimum difference
            showToast('Prisvarsel må være minst 1% forskjellig fra nåværende kurs', 'warning');
            return;
        }

        // Create alert
        const response = await fetch('/alerts/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': window.csrfToken
            },
            body: JSON.stringify({
                symbol,
                target_price: price,
                type: price > currentPrice ? 'above' : 'below'
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast(`Prisvarsel opprettet for ${symbol} ved ${price} NOK`, 'success');
            
            // Update alert count if it exists
            const countElement = document.querySelector('#alert-count');
            if (countElement) {
                const currentCount = parseInt(countElement.textContent) || 0;
                countElement.textContent = currentCount + 1;
            }
            
            return true;
        } else {
            throw new Error(data.error || 'Kunne ikke opprette prisvarsel');
        }
    } catch (error) {
        console.error('Error creating price alert:', error);
        showToast(error.message || 'Kunne ikke opprette prisvarsel. Prøv igjen senere.', 'error');
        return false;
    }
}

// Watchlist state management
class WatchlistStateManager {
    constructor() {
        this.isLoading = false;
        this.lastUpdateTime = 0;
        this.updateCooldown = 5000; // 5 seconds between updates
        this.navigationInProgress = false;
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Prevent multiple rapid reloads
        window.addEventListener('beforeunload', () => {
            this.navigationInProgress = true;
        });

        // Handle page visibility changes to prevent unnecessary reloads
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseAutoRefresh();
            } else {
                this.resumeAutoRefresh();
            }
        });

        // Override any existing watchlist refresh functions
        this.overrideRefreshFunctions();
    }

    overrideRefreshFunctions() {
        // Safely wrap reload function
        const originalReload = window.location.reload.bind(window.location);
        window.safeReload = (...args) => {
            if (this.shouldAllowReload()) {
                console.log('WatchlistStateManager: Allowing page reload');
                originalReload(...args);
            } else {
                console.log('WatchlistStateManager: Preventing unnecessary reload');
            }
        };

        // Ensure setTimeout-based refresh loops are safely overridden
        const originalSetTimeout = window.setTimeout;
        window.setTimeout = (callback, delay, ...args) => {
            const callbackStr = callback.toString();
            if ((callbackStr.includes('reload') || callbackStr.includes('location.href')) && 
                !this.shouldAllowReload()) {
                console.log('Preventing reload in setTimeout');
            } else {
                originalSetTimeout(callback, delay, ...args);
            }
        };

        // Intercept location.href changes safely
        try {
            let locationHref = window.location.href;
            const originalLocation = window.location;
            
            // Store original location.href setter if available
            const descriptor = Object.getOwnPropertyDescriptor(window.location, 'href') || 
                             Object.getOwnPropertyDescriptor(Object.getPrototypeOf(window.location), 'href');
            
            if (descriptor && descriptor.set && !window._locationIntercepted) {
                window._locationIntercepted = true;
                
                const originalSetter = descriptor.set;
                Object.defineProperty(window.location, 'href', {
                    set: function(value) {
                        if (value === locationHref) {
                            console.log('WatchlistStateManager: Preventing reload to same URL');
                            return;
                        }
                        originalSetter.call(this, value);
                    },
                    get: descriptor.get,
                    configurable: true
                });
            }
        } catch (e) {
            console.log('Could not intercept location.href, continuing without interception:', e.message);
        }
    }

    shouldAllowReload() {
        const now = Date.now();
        
        // Don't allow reload if we're already loading
        if (this.isLoading) {
            return false;
        }

        // Don't allow reload if we're navigating
        if (this.navigationInProgress) {
            return false;
        }

        // Check cooldown period
        if (now - this.lastUpdateTime < this.updateCooldown) {
            return false;
        }

        this.lastUpdateTime = now;
        return true;
    }

    pauseAutoRefresh() {
        this.isLoading = true;
        console.log('WatchlistStateManager: Auto-refresh paused');
    }

    resumeAutoRefresh() {
        // Wait a bit before resuming to prevent immediate reload
        setTimeout(() => {
            this.isLoading = false;
            console.log('WatchlistStateManager: Auto-refresh resumed');
        }, 2000);
    }

    // Provide safe methods for watchlist updates
    async safeUpdateWatchlist(watchlistId) {
        if (!this.shouldAllowReload()) {
            console.log('WatchlistStateManager: Update blocked by cooldown');
            return false;
        }

        this.isLoading = true;

        try {
            // Use AJAX instead of page reload
            const response = await fetch(`/watchlist/api/refresh/${watchlistId}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.updateWatchlistDOM(data);
                return true;
            } else {
                throw new Error('Failed to update watchlist');
            }
        } catch (error) {
            console.error('WatchlistStateManager: Update failed:', error);
            return false;
        } finally {
            this.isLoading = false;
        }
    }

    updateWatchlistDOM(data) {
        // Update specific parts of the watchlist without full page reload
        const watchlistContainer = document.querySelector('[data-watchlist-content]');
        if (watchlistContainer && data.html) {
            watchlistContainer.innerHTML = data.html;
        }

        // Update any price displays
        if (data.prices) {
            Object.keys(data.prices).forEach(symbol => {
                const priceElements = document.querySelectorAll(`[data-symbol="${symbol}"] .price`);
                priceElements.forEach(element => {
                    element.textContent = data.prices[symbol];
                });
            });
        }
    }

    getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }
}

// Initialize the state manager when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.watchlistStateManager = new WatchlistStateManager();
    console.log('WatchlistStateManager: Initialized');
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WatchlistStateManager;
}
