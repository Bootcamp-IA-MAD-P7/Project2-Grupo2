avaScript
/**
 * ui.js - Funciones de interfaz y utilidad para Iron Pulse
 */

// --- Gestión de Estados de Carga ---
function showLoading() {
    const loader = document.getElementById('global-loader');
    if (loader) loader.classList.remove('d-none');
}

function hideLoading() {
    const loader = document.getElementById('global-loader');
    if (loader) loader.classList.add('d-none');
}

// --- Notificaciones (Usando Toast o Alert de Bootstrap) ---
function showSuccess(message) {
    alert(`✅ Éxito: ${message}`); 
    // Recomendación: Cambiar por Toasts de Bootstrap para una mejor estética
}

function showError(message) {
    alert(`❌ Error: ${message}`);
}

// --- Formateadores de Datos ---
/**
 * Formatea moneda a formato local (Euro por defecto)
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount || 0);
}

/**
 * Formatea fechas ISO a legible
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

/**
 * Limpia y reinicia formularios
 */
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) form.reset();
}