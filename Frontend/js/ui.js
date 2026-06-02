/**
 * ui.js - Funciones de interfaz y utilidad para Iron Pulse
 */

// --- Gestión de Estados de Carga ---
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-3 text-muted">Loading data...</p>
            </div>`;
    }
}

function showError(containerId, message = "Something went wrong.") {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>${message}
            </div>`;
    }
}

// --- Notificaciones de éxito ---
function showSuccess(message) {
    const alertContainer = document.getElementById("alert-container");
    if (alertContainer) {
        alertContainer.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="bi bi-check-circle-fill me-2"></i>${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>`;
    }
}

// --- Formateadores de Datos ---
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount || 0);
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) form.reset();
}