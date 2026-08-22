const API_BASE_URL = (
    window.PARKSMART_CONFIG && window.PARKSMART_CONFIG.apiBaseUrl
        ? window.PARKSMART_CONFIG.apiBaseUrl
        : "http://localhost:8000"
).replace(/\/$/, "");

async function fetchAPI(endpoint, options = {}) {
    const token = localStorage.getItem('parksmart_token') || localStorage.getItem('parksmart_access_token');

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    if (options.body instanceof FormData) {
        delete headers['Content-Type'];
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    if (response.status === 401) {
        localStorage.removeItem('parksmart_token');
        localStorage.removeItem('parksmart_access_token');
        localStorage.removeItem('parksmart_user');
        throw new Error("Sesión expirada o inválida");
    }

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Error en el servidor");
    }

    return response.json();
}
