
/**
 * Enhanced Portfolio Actions Manager for Aksjeradar
 * Handles favorites, portfolio actions, and watchlist functionality
 */

if (typeof PortfolioActionsManager === 'undefined') {
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
        console.log('🔍 Found favorite buttons:', favoriteButtons.length);
        
        favoriteButtons.forEach(btn => {
            console.log('🎯 Setting up favorite button:', btn.id, btn.dataset.ticker);
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const ticker = btn.dataset.ticker;
                console.log('👆 Favorite button clicked for ticker:', ticker);
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
        console.log('🔍 Found portfolio buttons:', portfolioButtons.length);
        
        portfolioButtons.forEach(btn => {
            console.log('🎯 Setting up portfolio button:', btn.id, btn.dataset.ticker);
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const ticker = btn.dataset.ticker;
                console.log('👆 Portfolio button clicked for ticker:', ticker);
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
        if (!ticker || !button) {
            console.error('Missing required parameters for toggleFavorite');
            window.showToast('Manglende informasjon for favoritt-endring', 'error');
            return;
        }

        const originalText = button.innerHTML;
        try {
            // Disable button and show loading state
            button.disabled = true;
            button.innerHTML = '<i class="spinner-border spinner-border-sm me-1"></i>Oppdaterer...';

            // Get CSRF token
            const csrfToken = this.getCSRFToken();
            if (!csrfToken) {
                throw new Error('CSRF token not found');
            }

            // Make API request
            const response = await fetch(`/api/favorites/toggle/${ticker}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            // Handle non-200 responses
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                // Update button state and show success message
                this.updateFavoriteButtonState(button, data.favorited);
                window.showToast(data.favorited ? 
                    `${ticker} lagt til i favoritter` : 
                    `${ticker} fjernet fra favoritter`, 
                    'success'
                );
            } else {
                throw new Error(data.error || 'Kunne ikke oppdatere favoritt-status');
            }
        } catch (error) {
            console.error('Error toggling favorite:', error);
            
            // Show user-friendly error message
            window.showToast(
                error.message === 'CSRF token not found' ?
                'Sikkerhetsfeil: Vennligst last siden på nytt' :
                'Kunne ikke oppdatere favoritt-status. Prøv igjen senere.',
                'error'
            );

            // Restore original button state
            button.innerHTML = originalText;
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
            return data.favorited || false;
        } catch (error) {
            console.error('Error checking favorite status:', error);
            return false;
        }
    }

    /**
     * Initialize favorite button states on page load
     */
    async initializeFavoriteButtonStates() {
        const favoriteButtons = document.querySelectorAll('#add-to-watchlist, .favorite-btn, .watchlist-btn, .btn-star-favorite');
        
        for (const button of favoriteButtons) {
            const ticker = button.dataset.ticker || button.onclick?.toString().match(/'([^']+)'/)?.[1];
            if (ticker) {
                try {
                    const isFavorite = await this.checkFavoriteStatus(ticker);
                    this.updateFavoriteButtonState(button, isFavorite);
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
        button.disabled = false; // Always re-enable the button
        if (isFavorite) {
            button.innerHTML = '<i class="bi bi-star-fill"></i> I favoritter';
            button.className = 'btn btn-warning';
        } else {
            button.innerHTML = '<i class="bi bi-star"></i> Favoritt';
            button.className = 'btn btn-outline-warning';
        }
    }

    /**
     * Update favorite button state (for different button types)
     */
    updateFavoriteButtonState(button, isFavorite) {
        button.disabled = false; // Always re-enable the button
        if (button.classList.contains('btn-star-favorite')) {
            // Handle star buttons in stock list
            if (isFavorite) {
                button.innerHTML = '<i class="bi bi-star-fill"></i>';
                button.classList.add('btn-warning');
                button.classList.remove('text-white');
            } else {
                button.innerHTML = '<i class="bi bi-star"></i>';
                button.classList.remove('btn-warning');
                button.classList.add('text-white');
            }
        } else {
            // Handle regular favorite buttons
            this.updateFavoriteButton(button, isFavorite);
        }
    }

    /**
     * Add stock to portfolio (full implementation)
     */
    async addToPortfolio(ticker, button) {
        try {
            console.log(`🎯 Adding ${ticker} to portfolio`);
            
            button.disabled = true;
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="spinner-border spinner-border-sm me-1"></i>Legger til...';

            // Get CSRF token
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            
            const response = await fetch('/portfolio/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    ticker: ticker,
                    shares: 1,
                    price: 'current'
                })
            });

            const data = await response.json();
            console.log('📊 Portfolio API response:', data);

            if (response.ok && data.success) {
                this.showNotification(`✅ ${ticker} lagt til i portefølje`, 'success');
                button.innerHTML = '<i class="bi bi-check-circle"></i> I portefølje';
                button.classList.remove('btn-outline-success');
                button.classList.add('btn-success');
                button.disabled = false; // Re-enable the button
            } else {
                throw new Error(data.message || 'Kunne ikke legge til i portefølje');
            }
        } catch (error) {
            console.error('Error adding to portfolio:', error);
            button.innerHTML = originalText;
            button.disabled = false;
            this.showNotification(`Feil ved å legge ${ticker} til portefølje: ${error.message}`, 'error');
        }
    }

    /**
     * Show notification to user using unified toast system
     */
    showNotification(message, type = 'info') {
        if (typeof window.showToast === 'function') {
            // Use the global toast system
            window.showToast(message, type);
            return;
        }

        // Log message for debugging
        console.log(`${type.toUpperCase()}: ${message}`);
        
        // Create fallback toast if global system is not available
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white border-0 position-fixed';
        toast.style.cssText = 'bottom: 1rem; right: 1rem; z-index: 9999;';
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        // Set background color based on type
        switch(type) {
            case 'success':
                toast.classList.add('bg-success');
                break;
            case 'error':
                toast.classList.add('bg-danger');
                break;
            case 'warning':
                toast.classList.add('bg-warning');
                break;
            default:
                toast.classList.add('bg-info');
        }

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Lukk"></button>
            </div>
        `;

        // Create container if it doesn't exist
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'position-fixed bottom-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }

        container.appendChild(toast);

        // Initialize Bootstrap toast
        const bsToast = new bootstrap.Toast(toast, {
            animation: true,
            autohide: true,
            delay: 3000
        });

        bsToast.show();

        // Remove from DOM after hiding
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
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
if (!window.portfolioActionsManager) {
    window.portfolioActionsManager = new PortfolioActionsManager();
}

// Global function for onclick handlers
window.toggleFavorite = async function(ticker, button) {
    return await window.portfolioActionsManager.toggleFavorite(ticker, button);
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PortfolioActionsManager;
}
}
