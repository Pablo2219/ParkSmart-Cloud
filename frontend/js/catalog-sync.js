let parksmartCatalogSyncTimer = null;

async function sincronizarOfertaPublica() {
    const usuario = window.parkSmartSession?.usuario;
    if (!usuario || usuario.rol !== "CLIENTE" || !window.parkSmartState) return;

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
        console.warn("No se pudo sincronizar la oferta de parqueos:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    clearInterval(parksmartCatalogSyncTimer);
    parksmartCatalogSyncTimer = setInterval(sincronizarOfertaPublica, 15000);
    setTimeout(sincronizarOfertaPublica, 2500);
});
