window.PARKSMART_CONFIG = window.PARKSMART_CONFIG || {
    apiBaseUrl: "http://localhost:8000"
};

// Carga mejoras de autenticación/consentimiento sin acoplarlas al HTML principal.
const termsScript = document.createElement("script");
termsScript.src = "js/terms.js";
termsScript.defer = true;
document.head.appendChild(termsScript);
