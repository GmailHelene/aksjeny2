// Warren Buffett Analysis Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get the search input element
    const tickerSearch = document.getElementById('ticker');
    
    if (!tickerSearch) return;
    
    // Enable stock search autocomplete
    setupTickerAutocomplete(tickerSearch);
    
    // Handle form submission
    const analysisForm = tickerSearch.closest('form');
    if (analysisForm) {
        analysisForm.addEventListener('submit', function(event) {
            const ticker = tickerSearch.value.trim();
            if (!ticker) {
                event.preventDefault();
                showErrorToast('Vennligst skriv inn et aksjesymbol');
            }
        });
    }
});

// Setup ticker autocomplete
function setupTickerAutocomplete(inputElement) {
    // Get stock lists from data attributes
    const osloStocks = JSON.parse(document.getElementById('oslo-stocks-data')?.dataset?.stocks || '{}');
    const globalStocks = JSON.parse(document.getElementById('global-stocks-data')?.dataset?.stocks || '{}');
    
    // Create a combined list of stocks for autocomplete
    const allStocks = { ...osloStocks, ...globalStocks };
    
    // Stock suggestions
    let suggestions = [];
    for (const [symbol, data] of Object.entries(allStocks)) {
        suggestions.push({
            symbol: symbol,
            name: data.name,
            sector: data.sector || 'Ukjent',
            display: `${symbol} - ${data.name} (${data.sector || 'Ukjent'})`
        });
    }
    
    // Add event listener for input
    inputElement.addEventListener('input', function() {
        const query = this.value.trim().toUpperCase();
        
        // Hide any existing dropdown
        const existingDropdown = document.querySelector('.ticker-autocomplete-dropdown');
        if (existingDropdown) {
            existingDropdown.remove();
        }
        
        // If input is empty, don't show dropdown
        if (!query) return;
        
        // Filter suggestions based on input
        const filteredSuggestions = suggestions.filter(item => {
            return item.symbol.includes(query) || 
                   item.name.toUpperCase().includes(query) ||
                   item.sector.toUpperCase().includes(query);
        }).slice(0, 7); // Limit to 7 suggestions
        
        // Create dropdown if we have suggestions
        if (filteredSuggestions.length > 0) {
            createSuggestionsDropdown(inputElement, filteredSuggestions);
        }
    });
    
    // Handle click outside to close dropdown
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.ticker-autocomplete-container')) {
            const dropdown = document.querySelector('.ticker-autocomplete-dropdown');
            if (dropdown) dropdown.remove();
        }
    });
}

// Create suggestions dropdown
function createSuggestionsDropdown(inputElement, suggestions) {
    // Create container around input for positioning
    let container = inputElement.closest('.ticker-autocomplete-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'ticker-autocomplete-container position-relative';
        inputElement.parentNode.insertBefore(container, inputElement);
        container.appendChild(inputElement);
    }
    
    // Create dropdown
    const dropdown = document.createElement('div');
    dropdown.className = 'ticker-autocomplete-dropdown position-absolute start-0 end-0 mt-1 bg-white shadow rounded-3 z-index-dropdown';
    dropdown.style.zIndex = 1000;
    
    // Add suggestions
    suggestions.forEach(item => {
        const suggestionItem = document.createElement('div');
        suggestionItem.className = 'p-2 border-bottom ticker-suggestion';
        suggestionItem.style.cursor = 'pointer';
        
        // Hover effect
        suggestionItem.addEventListener('mouseover', () => {
            suggestionItem.classList.add('bg-light');
        });
        suggestionItem.addEventListener('mouseout', () => {
            suggestionItem.classList.remove('bg-light');
        });
        
        // Create inner HTML
        suggestionItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${item.symbol}</strong>
                    <span class="text-muted ms-2">${item.name}</span>
                </div>
                <span class="badge bg-secondary">${item.sector}</span>
            </div>
        `;
        
        // Handle click
        suggestionItem.addEventListener('click', () => {
            inputElement.value = item.symbol;
            dropdown.remove();
        });
        
        dropdown.appendChild(suggestionItem);
    });
    
    // Add to DOM
    container.appendChild(dropdown);
}

// Show error toast
function showErrorToast(message) {
    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast
        const toastElement = document.createElement('div');
        toastElement.className = 'toast align-items-center text-white bg-danger border-0';
        toastElement.setAttribute('role', 'alert');
        toastElement.setAttribute('aria-live', 'assertive');
        toastElement.setAttribute('aria-atomic', 'true');
        
        toastElement.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        toastContainer.appendChild(toastElement);
        
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    } else {
        // Fallback if Bootstrap is not available
        alert(message);
    }
}
