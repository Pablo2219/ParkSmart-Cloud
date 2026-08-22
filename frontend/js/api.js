const API_BASE_URL = (
    window.PARKSMART_CONFIG && window.PARKSMART_CONFIG.apiBaseUrl
        ? window.PARKSMART_CONFIG.apiBaseUrl
        : "http://localhost:8000"
).replace(/\/$/, "");

function explicarErrorRed(error, endpoint) {
    if (error instanceof TypeError && /fetch/i.test(error.message || "")) {
        return `No se pudo conectar con ParkSmart API (${API_BASE_URL}). Verificá que Docker tenga la API en ejecución y que el frontend esté autorizado por CORS. Endpoint: ${endpoint}`;
    }
    return error?.message || "No se pudo conectar con el servidor.";
}

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

    let response;
    try {
        response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });
    } catch (error) {
        throw new Error(explicarErrorRed(error, endpoint));
    }

    if (response.status === 401) {
        localStorage.removeItem('parksmart_token');
        localStorage.removeItem('parksmart_access_token');
        localStorage.removeItem('parksmart_user');
        localStorage.removeItem('parksmart_auth_user');
        throw new Error("Sesión expirada o inválida");
    }

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        const detalle = err.detail;
        if (Array.isArray(detalle)) {
            throw new Error(detalle.map(item => item?.msg || "Dato inválido").join(" | "));
        }
        throw new Error(detalle || `Error HTTP ${response.status}`);
    }

    const texto = await response.text();
    if (!texto) return null;

    try {
        return JSON.parse(texto);
    } catch {
        return texto;
    }
}
