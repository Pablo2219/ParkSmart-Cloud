window.PARKSMART_CONFIG = window.PARKSMART_CONFIG || {
    apiBaseUrl: "http://localhost:8000"
};

// Carga mejoras de autenticación/consentimiento sin acoplarlas al HTML principal.
const termsScript = document.createElement("script");
termsScript.src = "js/terms.js";
termsScript.defer = true;
document.head.appendChild(termsScript);

// Sincronización ligera de la oferta para clientes. Evita que un parqueo recién
// publicado por un proveedor quede invisible hasta recargar manualmente.
window.addEventListener("load", () => {
    const sincronizar = async () => {
        const usuario = window.parkSmartSession?.usuario;
        if (!usuario || usuario.rol !== "CLIENTE" || !window.parkSmartState || typeof fetchAPI !== "function") return;
        try {
            const [espacios, sectores] = await Promise.all([
                fetchAPI("/espacios/disponibles"),
                fetchAPI("/espacios/sectores")
            ]);
            window.parkSmartState.espacios = espacios || [];
            window.parkSmartState.catalogoEspacios = [...window.parkSmartState.espacios];
            window.parkSmartState.sectores = sectores || [];
            window.parkSmartState.online = true;
            window.parkSmartState.demo = false;
            if (typeof renderAplicacion === "function") renderAplicacion();
            if (typeof actualizarMarcadoresMapa === "function") actualizarMarcadoresMapa(window.parkSmartState.espacios, window.parkSmartState.sectores);
        } catch (error) {
            console.warn("No se pudo sincronizar la oferta pública:", error);
        }
    };
    setTimeout(sincronizar, 2500);
    setInterval(sincronizar, 15000);
});
