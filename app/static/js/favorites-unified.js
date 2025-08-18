/**
 * Unified Favorites System for Aksjeradar
 * Handles star/favorites buttons consistently across all stock list pages
 */

// Global favorites management
window.favoritesManager = {
    
    // Initialize favorites system
    init: function() {
        console.log('Initializing unified favorites system...');
        this.bindEventListeners();
        this.loadFavoriteStates();
    },
    
    // Bind event listeners to favorite buttons
    bindEventListeners: function() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-star-favorite, .btn-star-favorite *')) {
                e.preventDefault();
                e.stopPropagation();
                
                const button = e.target.closest('.btn-star-favorite');
                if (button) {
                    const symbol = button.dataset.ticker || button.getAttribute('onclick')?.match(/toggleFavorite\('([^']+)'/)?.[1];
                    if (symbol) {
                        this.toggleFavorite(symbol, button);
                    }
                }
            }
        });
    },
    
    // Load favorite states for all visible buttons
    loadFavoriteStates: function() {
        const buttons = document.querySelectorAll('.btn-star-favorite');
        buttons.forEach(btn => {
            const symbol = btn.dataset.ticker || btn.getAttribute('onclick')?.match(/toggleFavorite\('([^']+)'/)?.[1];
            if (symbol) {
                this.checkFavoriteStatus(symbol, btn);
            }
        });
    },
    
    // Check if a symbol is favorited
    checkFavoriteStatus: async function(symbol, button) {
        try {
            const response = await fetch(`/stocks/api/favorites/check/${symbol}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.updateButtonState(button, data.favorited, symbol);
            }
        } catch (error) {
            console.warn('Could not check favorite status for', symbol, ':', error);
        }
    },
    
    // Toggle favorite status
    toggleFavorite: async function(symbol, button) {
        if (!symbol) {
            console.error('No symbol provided for favorite toggle');
            return;
        }
        
        console.log('Toggling favorite for symbol:', symbol);
        
        try {
            // Show loading state
            const originalContent = button.innerHTML;
            button.innerHTML = '<i class="spinner-border spinner-border-sm"></i>';
            button.disabled = true;
            
            // Use the unified API endpoint with CSRF helper
            const response = await window.csrfHelper.fetch('/api/watchlist/toggle', {
                method: 'POST',
                body: JSON.stringify({ symbol: symbol })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const isAdded = data.action === 'added';
                this.updateButtonState(button, isAdded, symbol);
                this.showToast(data.message || `${symbol} ${isAdded ? 'lagt til' : 'fjernet fra'} favoritter`, 'success');
            } else {
                // Restore button state
                button.innerHTML = originalContent;
                button.disabled = false;
                this.showToast(data.message || 'Kunne ikke oppdatere favoritter', 'error');
            }
            
        } catch (error) {
            console.error('Error toggling favorite:', error);
            // Restore button state
            button.innerHTML = originalContent;
            button.disabled = false;
            this.showToast('Teknisk feil ved oppdatering av favoritter', 'error');
        }
    },
    
    // Update button visual state
    updateButtonState: function(button, isFavorited, symbol) {
        if (!button) return;
        
        if (isFavorited) {
            // Favorited state - filled star, yellow background
            button.innerHTML = '<i class="bi bi-star-fill"></i>';
            button.classList.remove('text-white');
            button.classList.add('btn-warning');
            button.style.background = '#ffc107';
            button.style.border = '1px solid #ffc107';
            button.title = `Fjern ${symbol} fra favoritter`;
        } else {
            // Not favorited state - empty star, blue background
            button.innerHTML = '<i class="bi bi-star"></i>';
            button.classList.add('text-white');
            button.classList.remove('btn-warning');
            button.style.background = '#007bff';
            button.style.border = '1px solid #007bff';
            button.title = `Legg ${symbol} til favoritter`;
        }
        
        button.disabled = false;
    },
    
    // Show toast notification
    showToast: function(message, type = 'info') {
        // Try to use existing toast function if available
        if (window.showToast && typeof window.showToast === 'function') {
            window.showToast(message, type);
            return;
        }
        
        // Fallback: create our own toast
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        // Add to toast container or create one
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
        
        container.appendChild(toast);
        
        // Initialize Bootstrap toast if available
        if (window.bootstrap && bootstrap.Toast) {
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
            
            // Remove after hidden
            toast.addEventListener('hidden.bs.toast', () => toast.remove());
        } else {
            // Fallback: show for 3 seconds
            toast.style.display = 'block';
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.favoritesManager.init();
});

// Legacy support for existing onclick handlers
window.toggleFavorite = function(symbol, button) {
    if (button && window.favoritesManager) {
        window.favoritesManager.toggleFavorite(symbol, button);
    } else {
        console.warn('Legacy toggleFavorite called without proper setup');
    }
};
