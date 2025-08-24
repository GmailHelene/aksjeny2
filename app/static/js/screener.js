// Screener functionality for watchlist management
let currentScreenerState = {};

// Available screener presets
const screenerPresets = {
    dividend: {
        name: 'Dividendeaksjer',
        description: 'Aksjer med høy og stabil dividendeutbetaling',
        filters: {
            dividend_yield: { min: 3.0 },
            market_cap: { min: 1000000000 },
            pe_ratio: { max: 20 },
            debt_to_equity: { max: 2.0 }
        }
    },
    growth: {
        name: 'Vekstaksjer',
        description: 'Aksjer med høy vekst og potensial',
        filters: {
            revenue_growth: { min: 15.0 },
            profit_growth: { min: 10.0 },
            market_cap: { min: 500000000 }
        }
    },
    value: {
        name: 'Verdiaksjer',
        description: 'Undervurderte aksjer med god margin of safety',
        filters: {
            pe_ratio: { max: 15 },
            price_to_book: { max: 1.5 },
            debt_to_equity: { max: 1.5 },
            current_ratio: { min: 1.5 }
        }
    },
    momentum: {
        name: 'Momentum',
        description: 'Aksjer med sterk pristrend og momentum',
        filters: {
            price_change_1m: { min: 5.0 },
            price_change_3m: { min: 10.0 },
            volume_change: { min: 20.0 }
        }
    }
};

// Select and apply a screener preset
async function selectPreset(presetName) {
    try {
        // Get the preset configuration
        const preset = screenerPresets[presetName];
        if (!preset) {
            throw new Error('Ukjent preset');
        }

        // Show loading state
        const loadingElement = document.getElementById('screener-loading');
        if (loadingElement) {
            loadingElement.style.display = 'block';
        }

        // Update UI to show selected preset
        const presetButtons = document.querySelectorAll('.preset-button');
        presetButtons.forEach(button => {
            if (button.dataset.preset === presetName) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });

        // Apply the filters from the preset
        await applyFilters(preset.filters);

        // Update filter inputs to match preset
        Object.entries(preset.filters).forEach(([filter, values]) => {
            const minInput = document.querySelector(`[data-filter="${filter}"][data-type="min"]`);
            const maxInput = document.querySelector(`[data-filter="${filter}"][data-type="max"]`);
            
            if (minInput && values.min !== undefined) {
                minInput.value = values.min;
            }
            if (maxInput && values.max !== undefined) {
                maxInput.value = values.max;
            }
        });

        // Update screener state
        currentScreenerState = {
            preset: presetName,
            filters: { ...preset.filters }
        };

        // Show success message
        showToast(`${preset.name} filter anvendt`, 'success');

        // Hide loading state
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }

        return true;
    } catch (error) {
        console.error('Error applying preset:', error);
        showToast('Kunne ikke anvende filter. Prøv igjen senere.', 'error');
        
        // Hide loading state
        const loadingElement = document.getElementById('screener-loading');
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }

        return false;
    }
}

function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    // Create toast content
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    // Add toast to container
    toastContainer.appendChild(toast);

    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        animation: true,
        autohide: true,
        delay: 3000
    });
    bsToast.show();

    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

async function addToWatchlist(symbol, event) {
    if (event) {
        event.preventDefault();
    }

    try {
        // Get CSRF token from meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
        if (!csrfToken) {
            throw new Error('CSRF token not found');
        }

        // Make API call to add to watchlist
        const response = await fetch('/watchlist/api/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ symbol })
        });

        const data = await response.json();

        if (data.success) {
            showToast('Aksje lagt til i favoritter', 'success');
            
            // Update button to show added state
            const button = event.target.closest('button');
            if (button) {
                button.innerHTML = '<i class="bi bi-heart-fill"></i>';
                button.classList.remove('btn-outline-success');
                button.classList.add('btn-success');
            }
        } else {
            throw new Error(data.message || 'Kunne ikke legge til i favoritter');
        }
    } catch (error) {
        console.error('Error adding to watchlist:', error);
        showToast(error.message || 'Teknisk feil ved lagring', 'error');
    }
}

async function saveAsWatchlist(event) {
    event.preventDefault();

    // Get currently filtered stocks from the screener state
    const filteredStocks = getFilteredStocksFromScreener();

    if (!filteredStocks || filteredStocks.length === 0) {
        showToast('Ingen aksjer valgt for lagring', 'warning');
        return;
    }

    // Show save dialog
    const dialog = document.createElement('div');
    dialog.className = 'modal fade';
    dialog.setAttribute('tabindex', '-1');
    dialog.setAttribute('aria-hidden', 'true');
    dialog.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Lagre som watchlist</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label for="watchlistName">Navn på watchlist</label>
                        <input type="text" class="form-control" id="watchlistName" placeholder="F.eks. Mine Tech Aksjer">
                    </div>
                    <div class="form-group mt-3">
                        <label for="watchlistDesc">Beskrivelse (valgfritt)</label>
                        <textarea class="form-control" id="watchlistDesc" rows="3" placeholder="Legg til en beskrivelse..."></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Avbryt</button>
                    <button type="button" class="btn btn-primary" id="saveWatchlistBtn">Lagre watchlist</button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(dialog);
    const modal = new bootstrap.Modal(dialog);
    modal.show();

    // Handle save button click
    document.getElementById('saveWatchlistBtn').addEventListener('click', async () => {
        const name = document.getElementById('watchlistName').value.trim();
        const description = document.getElementById('watchlistDesc').value.trim();

        if (!name) {
            showToast('Vennligst angi navn på watchlist', 'warning');
            return;
        }

        try {
            // Get CSRF token
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            if (!csrfToken) {
                throw new Error('CSRF token not found');
            }

            // Save watchlist via API
            const response = await fetch('/watchlist/api/save_as', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    name,
                    description,
                    stocks: filteredStocks
                })
            });

            const data = await response.json();

            if (data.success) {
                showToast('Watchlist lagret', 'success');
                modal.hide();
            } else {
                throw new Error(data.message || 'Kunne ikke lagre watchlist');
            }
        } catch (error) {
            console.error('Error saving watchlist:', error);
            showToast(error.message || 'Teknisk feil ved lagring', 'error');
        }
    });

    // Clean up when dialog is hidden
    dialog.addEventListener('hidden.bs.modal', () => {
        dialog.remove();
    });
}

// Helper function to get filtered stocks from screener
function getFilteredStocksFromScreener() {
    // Get visible rows from the screener table
    const visibleRows = document.querySelectorAll('#screenerTable tbody tr:not(.d-none)');
    return Array.from(visibleRows).map(row => {
        const symbol = row.querySelector('[data-symbol]')?.dataset.symbol;
        if (symbol) {
            return {
                symbol,
                name: row.querySelector('[data-name]')?.dataset.name || symbol,
                price: row.querySelector('[data-price]')?.dataset.price,
                change: row.querySelector('[data-change]')?.dataset.change
            };
        }
    }).filter(stock => stock && stock.symbol);
}

// Update screener state when filters change
function updateScreenerState(filters) {
    currentScreenerState = {
        ...currentScreenerState,
        filters
    };
}
