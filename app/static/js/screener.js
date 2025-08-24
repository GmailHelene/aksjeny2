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
