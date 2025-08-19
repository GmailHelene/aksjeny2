
/**
 * Enhanced Portfolio Actions Manager for Aksjeradar
 * Handles favorites, portfolio actions, and watchlist functionality
 */

class PortfolioActionsManager {
    constructor() {
        this.isInitialized = false;
        this.initializeEventListeners();
    }

    /**
     * Initialize all event listeners for portfolio actions
     */
    initializeEventListeners() {
        console.log('🚀 Initializing Portfolio Actions Manager');
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    /**
     * Initialize the manager
     */
    init() {
        if (this.isInitialized) return;
        
        this.setupFavoriteButtons();
        this.setupPortfolioButtons();
        this.initializeFavoriteButtonStates();
        
        this.isInitialized = true;
        console.log('✅ Portfolio Actions Manager initialized');
    }

    /**
     * Setup favorite/watchlist button functionality
     */
    setupFavoriteButtons() {
        const favoriteButtons = document.querySelectorAll('#add-to-watchlist, .favorite-btn, .watchlist-btn');
        
        favoriteButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const ticker = btn.dataset.ticker;
                if (ticker) {
                    this.toggleFavorite(ticker, btn);
                }
            });
        });
    }

    /**
     * Setup portfolio button functionality
     */
    setupPortfolioButtons() {
        const portfolioButtons = document.querySelectorAll('#add-to-portfolio, .portfolio-btn');
        
        portfolioButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const ticker = btn.dataset.ticker;
                if (ticker) {
                    this.addToPortfolio(ticker, btn);
                }
            });
        });
    }

    /**
     * Toggle favorite status for a stock
     */
    async toggleFavorite(ticker, button) {
        try {
            // Check current status
            const isFavorite = await this.checkFavoriteStatus(ticker);
            
            if (isFavorite) {
                await this.removeFromFavorites(ticker, button);
            } else {
                await this.addToFavorites(ticker, button);
            }
        } catch (error) {
            console.error('Error toggling favorite:', error);
            this.showNotification('Feil ved endring av favoritt-status', 'error');
        }
    }

    /**
     * Add stock to favorites
     */
    async addToFavorites(ticker, button) {
        try {
            button.disabled = true;
            button.innerHTML = '<i class="spinner-border spinner-border-sm me-1"></i>Legger til...';

            const response = await fetch('/stocks/api/favorites/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ symbol: ticker })
            });

            const data = await response.json();

            if (data.success) {
                this.updateFavoriteButton(button, true);
                this.showNotification(`${ticker} lagt til i favoritter!`, 'success');
            } else {
                throw new Error(data.error || 'Failed to add to favorites');
            }
        } catch (error) {
            console.error('Error adding to favorites:', error);
            this.showNotification('Feil ved tillegging til favoritter', 'error');
            this.updateFavoriteButton(button, false);
        } finally {
            button.disabled = false;
        }
    }

    /**
     * Remove stock from favorites
     */
    async removeFromFavorites(ticker, button) {
        try {
            button.disabled = true;
            button.innerHTML = '<i class="spinner-border spinner-border-sm me-1"></i>Fjerner...';

            const response = await fetch('/stocks/api/favorites/remove', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ symbol: ticker })
            });

            const data = await response.json();

            if (data.success) {
                this.updateFavoriteButton(button, false);
                this.showNotification(`${ticker} fjernet fra favoritter!`, 'success');
            } else {
                throw new Error(data.error || 'Failed to remove from favorites');
            }
        } catch (error) {
            console.error('Error removing from favorites:', error);
            this.showNotification('Feil ved fjerning fra favoritter', 'error');
            this.updateFavoriteButton(button, true);
        } finally {
            button.disabled = false;
        }
    }

    /**
     * Check if stock is in favorites
     */
    async checkFavoriteStatus(ticker) {
        try {
            const response = await fetch(`/stocks/api/favorites/check/${ticker}`);
            const data = await response.json();
            return data.is_favorite || false;
        } catch (error) {
            console.error('Error checking favorite status:', error);
            return false;
        }
    }

    /**
     * Initialize favorite button states on page load
     */
    async initializeFavoriteButtonStates() {
        const favoriteButtons = document.querySelectorAll('#add-to-watchlist, .favorite-btn, .watchlist-btn');
        
        for (const button of favoriteButtons) {
            const ticker = button.dataset.ticker;
            if (ticker) {
                try {
                    const isFavorite = await this.checkFavoriteStatus(ticker);
                    this.updateFavoriteButton(button, isFavorite);
                } catch (error) {
                    console.error(`Error initializing favorite state for ${ticker}:`, error);
                }
            }
        }
    }

    /**
     * Update favorite button appearance
     */
    updateFavoriteButton(button, isFavorite) {
        if (isFavorite) {
            button.innerHTML = '<i class="bi bi-star-fill"></i> I favoritter';
            button.className = 'btn btn-warning';
        } else {
            button.innerHTML = '<i class="bi bi-star"></i> Favoritt';
            button.className = 'btn btn-outline-warning';
        }
    }

    /**
     * Add stock to portfolio (simplified implementation)
     */
    async addToPortfolio(ticker, button) {
        try {
            button.disabled = true;
            button.innerHTML = '<i class="spinner-border spinner-border-sm me-1"></i>Legger til...';

            // For now, just show a notification
            // In the future, this could open a modal for quantity/price input
            this.showNotification(`Funksjonalitet for å legge ${ticker} til portefølje kommer snart!`, 'info');
            
            setTimeout(() => {
                button.innerHTML = '<i class="bi bi-briefcase"></i> Portefølje';
                button.disabled = false;
            }, 2000);
        } catch (error) {
            console.error('Error adding to portfolio:', error);
            this.showNotification('Feil ved tillegging til portefølje', 'error');
            button.disabled = false;
        }
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'info') {
        // Try to use existing notification system
        if (typeof window.showNotification === 'function') {
            window.showNotification(message, type);
            return;
        }

        // Fallback to simple alert or console
        if (type === 'error') {
            console.error(message);
        } else {
            console.log(message);
        }
        
        // Show a simple browser notification
        if (type !== 'error') {
            // Create a simple toast notification
            this.createToastNotification(message, type);
        }
    }

    /**
     * Create a simple toast notification
     */
    createToastNotification(message, type) {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="me-2">
                    <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
                </div>
                <div>${message}</div>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;

        document.body.appendChild(toast);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }

    /**
     * Get CSRF token for POST requests
     */
    getCSRFToken() {
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) {
            return metaTag.getAttribute('content');
        }
        
        // Try to get from cookie
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrf_token') {
                return value;
            }
        }
        
        return '';
    }
}

// Create global instance
window.portfolioActionsManager = new PortfolioActionsManager();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PortfolioActionsManager;
}
