let proveedorMapa = null;
let proveedorModoMapa = "SECTOR";
let proveedorCatalogo = { sectores: [], espacios: [] };
let proveedorMarkerLayer = null;

window.inicializarPanelProveedor = async function () {
    const app = document.getElementById("appShell");
    if (!app) return;

    document.body.classList.add("provider-session");
    document.querySelector(".bottom-nav")?.classList.add("hidden");
    const contenido = document.querySelector(".app-content");
    if (!contenido) return;

    contenido.innerHTML = `
        <section id="vistaProveedor" class="provider-view">
            <div class="provider-heading">
                <div>
                    <span class="section-kicker">PANEL DEL PROVEEDOR</span>
                    <h1>Administrá tu oferta de parqueo</h1>
                    <p id="providerBusinessName">Cargando proveedor...</p>
                </div>
                <button class="provider-logout" type="button" onclick="cerrarSesion()">Cerrar sesión</button>
            </div>

            <div class="provider-stats">
                <article><strong id="providerSectorCount">0</strong><span>Sectores</span></article>
                <article><strong id="providerSpaceCount">0</strong><span>Espacios</span></article>
                <article><strong id="providerReservationCount">0</strong><span>Reservas</span></article>
            </div>

            <section class="provider-card">
                <div class="provider-card-head">
                    <div><span class="section-kicker">UBICACIÓN</span><h2>Mapa de tus parqueos</h2><p>Elegí un modo y tocá el mapa. Guardamos coordenadas reales de OpenStreetMap.</p></div>
                    <button type="button" class="provider-refresh" onclick="cargarCatalogoProveedor()">Actualizar</button>
                </div>
                <div class="provider-tools">
                    <button id="providerModeSector" class="provider-mode active" type="button" onclick="seleccionarModoProveedor('SECTOR')">+ Sector</button>
                    <button id="providerModeSpace" class="provider-mode" type="button" onclick="seleccionarModoProveedor('ESPACIO')">+ Espacio</button>
                    <select id="providerSectorSelect" aria-label="Sector para nuevo espacio"><option value="">Seleccioná un sector</option></select>
                </div>
                <div id="providerMap" class="provider-map"></div>
                <p id="providerMapHint" class="provider-map-hint">Modo sector: tocá el mapa para registrar la ubicación del sector.</p>
            </section>

            <section class="provider-grid">
                <article class="provider-card">
                    <div class="provider-card-head"><div><span class="section-kicker">CATÁLOGO</span><h2>Sectores y espacios</h2></div></div>
                    <div id="providerCatalogList" class="provider-list"></div>
                </article>
                <article class="provider-card">
                    <div class="provider-card-head"><div><span class="section-kicker">OPERACIÓN</span><h2>Reservas recibidas</h2><p>Solo aparecen reservas hechas sobre tus espacios.</p></div></div>
                    <div id="providerReservationsList" class="provider-list"></div>
                </article>
            </section>
        </section>`;

    insertarEstilosProveedor();
    document.getElementById("providerMap")?.addEventListener("click", () => {});
    inicializarMapaProveedor();
    await cargarCatalogoProveedor();
    await cargarReservasProveedor();
};

function insertarEstilosProveedor() {
    if (document.getElementById("providerStyles")) return;
    const style = document.createElement("style");
    style.id = "providerStyles";
    style.textContent = `
        .provider-view{max-width:1180px;margin:0 auto;padding:10px 0 40px}.provider-heading{display:flex;justify-content:space-between;gap:20px;align-items:flex-start;margin-bottom:20px}.provider-heading h1{margin:4px 0 6px;font-size:clamp(28px,4vw,44px)}.provider-heading p{margin:0;color:#718096}.provider-logout,.provider-refresh{border:1px solid #d7dee8;background:#fff;border-radius:12px;padding:10px 14px;cursor:pointer}.provider-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:18px}.provider-stats article{background:#fff;border:1px solid #e5eaf0;border-radius:16px;padding:16px;box-shadow:0 8px 24px rgba(10,25,41,.05)}.provider-stats strong{display:block;font-size:28px}.provider-stats span{color:#718096;font-size:13px}.provider-card{background:#fff;border:1px solid #e5eaf0;border-radius:20px;padding:18px;margin-bottom:18px;box-shadow:0 10px 30px rgba(10,25,41,.05)}.provider-card-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:14px}.provider-card h2{margin:3px 0}.provider-card p{color:#718096;margin:4px 0;font-size:14px}.provider-tools{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}.provider-mode{border:1px solid #d7dee8;background:#fff;border-radius:10px;padding:9px 13px;cursor:pointer}.provider-mode.active{background:#07111f;color:#fff;border-color:#07111f}.provider-tools select{border:1px solid #d7dee8;border-radius:10px;padding:9px;min-width:220px}.provider-map{height:480px;border-radius:16px;overflow:hidden;border:1px solid #dfe5ec}.provider-map-hint{padding:10px 12px;background:#f7f9fb;border-radius:10px}.provider-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.provider-list{display:grid;gap:9px;max-height:430px;overflow:auto}.provider-list-item{border:1px solid #e5eaf0;border-radius:12px;padding:12px}.provider-list-item strong{display:block}.provider-list-item small{color:#718096}.provider-reservation{display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:center}.provider-badge{font-size:11px;border-radius:999px;padding:5px 8px;background:#edf4ff}.provider-empty{padding:22px;text-align:center;color:#718096;border:1px dashed #d7dee8;border-radius:12px}@media(max-width:800px){.provider-heading{display:block}.provider-logout{margin-top:12px}.provider-stats{grid-template-columns:1fr}.provider-grid{grid-template-columns:1fr}.provider-map{height:390px}}
    `;
    document.head.appendChild(style);
}

function inicializarMapaProveedor() {
    if (typeof L === "undefined") {
        document.getElementById("providerMapHint").textContent = "Leaflet no está disponible. Revisá la conexión a Internet para cargar el mapa.";
        return;
    }
    proveedorMapa = L.map("providerMap").setView([9.9347, -84.0875], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 20, attribution: "© OpenStreetMap" }).addTo(proveedorMapa);
    proveedorMarkerLayer = L.layerGroup().addTo(proveedorMapa);
    proveedorMapa.on("click", gestionarClickMapaProveedor);
}

function seleccionarModoProveedor(modo) {
    proveedorModoMapa = modo;
    document.getElementById("providerModeSector")?.classList.toggle("active", modo === "SECTOR");
    document.getElementById("providerModeSpace")?.classList.toggle("active", modo === "ESPACIO");
    const hint = document.getElementById("providerMapHint");
    if (hint) hint.textContent = modo === "SECTOR" ? "Modo sector: tocá el mapa para registrar la ubicación del sector." : "Modo espacio: elegí un sector y tocá el mapa para registrar un espacio.";
}

async function gestionarClickMapaProveedor(evento) {
    const { lat, lng } = evento.latlng;
    if (proveedorModoMapa === "SECTOR") {
        const nombre = prompt("Nombre del sector:", `Sector ${proveedorCatalogo.sectores.length + 1}`);
        if (!nombre?.trim()) return;
        const descripcion = prompt("Descripción (opcional):", "Parqueo administrado por el proveedor") || null;
        try {
            await fetchAPI("/proveedores/sectores", { method: "POST", body: JSON.stringify({ nombreSector: nombre.trim(), descripcion, ubicacion: `${lat.toFixed(6)}, ${lng.toFixed(6)}`, latitud: lat, longitud: lng }) });
            mostrarToast("Sector registrado en el mapa.");
            await cargarCatalogoProveedor();
        } catch (error) { mostrarToast(error.message); }
        return;
    }

    const sectorId = Number(document.getElementById("providerSectorSelect")?.value);
    if (!sectorId) return mostrarToast("Seleccioná primero el sector del nuevo espacio.");
    const codigo = prompt("Código del espacio:", `A-${proveedorCatalogo.espacios.length + 1}`);
    if (!codigo?.trim()) return;
    const tipo = (prompt("Tipo: REGULAR, MOTOCICLETA, DISCAPACIDAD, ELECTRICO o VIP", "REGULAR") || "REGULAR").toUpperCase();
    if (!["REGULAR", "MOTOCICLETA", "DISCAPACIDAD", "ELECTRICO", "VIP"].includes(tipo)) return mostrarToast("Tipo de espacio inválido.");
    try {
        await fetchAPI("/proveedores/espacios", { method: "POST", body: JSON.stringify({ idSector: sectorId, codigoEspacio: codigo.trim(), tipoEspacio: tipo, latitud: lat, longitud: lng }) });
        mostrarToast("Espacio registrado en el mapa.");
        await cargarCatalogoProveedor();
    } catch (error) { mostrarToast(error.message); }
}

async function cargarCatalogoProveedor() {
    try {
        proveedorCatalogo = await fetchAPI("/proveedores/mi-catalogo");
        document.getElementById("providerSectorCount").textContent = proveedorCatalogo.sectores.length;
        document.getElementById("providerSpaceCount").textContent = proveedorCatalogo.espacios.length;
        renderSelectorSectores();
        renderCatalogoProveedor();
        renderMarcadoresProveedor();
    } catch (error) {
        mostrarToast(error.message);
    }
}

function renderSelectorSectores() {
    const select = document.getElementById("providerSectorSelect");
    if (!select) return;
    select.innerHTML = `<option value="">Seleccioná un sector</option>` + proveedorCatalogo.sectores.map(s => `<option value="${s.idSector}">${escaparHtml(s.nombreSector)}</option>`).join("");
}

function renderCatalogoProveedor() {
    const contenedor = document.getElementById("providerCatalogList");
    if (!contenedor) return;
    if (!proveedorCatalogo.sectores.length) {
        contenedor.innerHTML = `<div class="provider-empty">Aún no tenés sectores. Activá “+ Sector” y tocá el mapa.</div>`;
        return;
    }
    contenedor.innerHTML = proveedorCatalogo.sectores.map(sector => {
        const espacios = proveedorCatalogo.espacios.filter(e => e.idSector === sector.idSector);
        return `<div class="provider-list-item"><strong>${escaparHtml(sector.nombreSector)}</strong><small>${escaparHtml(sector.ubicacion || "Sin dirección")}</small><br><small>${espacios.length} espacios · ${espacios.filter(e => e.estado === "DISPONIBLE").length} disponibles</small></div>`;
    }).join("");
}

function renderMarcadoresProveedor() {
    if (!proveedorMapa || !proveedorMarkerLayer || typeof L === "undefined") return;
    proveedorMarkerLayer.clearLayers();
    const bounds = [];

    proveedorCatalogo.sectores.forEach(sector => {
        if (sector.latitud == null || sector.longitud == null) return;
        const marker = L.marker([Number(sector.latitud), Number(sector.longitud)]).bindPopup(`<strong>${escaparHtml(sector.nombreSector)}</strong><br>Sector de parqueo`);
        proveedorMarkerLayer.addLayer(marker);
        bounds.push([Number(sector.latitud), Number(sector.longitud)]);
    });

    proveedorCatalogo.espacios.forEach(espacio => {
        if (espacio.latitud == null || espacio.longitud == null) return;
        const marker = L.circleMarker([Number(espacio.latitud), Number(espacio.longitud)], { radius: 8, weight: 2, fillOpacity: .8 })
            .bindPopup(`<strong>${escaparHtml(espacio.codigoEspacio)}</strong><br>${escaparHtml(espacio.tipoEspacio)} · ${escaparHtml(espacio.estado)}`);
        proveedorMarkerLayer.addLayer(marker);
        bounds.push([Number(espacio.latitud), Number(espacio.longitud)]);
    });

    if (bounds.length) proveedorMapa.fitBounds(bounds, { padding: [30, 30], maxZoom: 17 });
}

async function cargarReservasProveedor() {
    const contenedor = document.getElementById("providerReservationsList");
    try {
        const reservas = await fetchAPI("/proveedores/reservas");
        document.getElementById("providerReservationCount").textContent = reservas.length;
        if (!reservas.length) {
            contenedor.innerHTML = `<div class="provider-empty">Todavía no hay reservas en tus espacios.</div>`;
            return;
        }
        contenedor.innerHTML = reservas.map(r => `<div class="provider-list-item provider-reservation"><span class="provider-badge">${escaparHtml(r.estado)}</span><div><strong>${escaparHtml(r.codigoEspacio)} · ${escaparHtml(r.nombreSector)}</strong><small>Cliente #${r.idCliente} · ${formatearFecha(r.fechaInicioReserva)}</small></div><small>${formatearFecha(r.fechaFinReserva)}</small></div>`).join("");
    } catch (error) {
        contenedor.innerHTML = `<div class="provider-empty">${escaparHtml(error.message)}</div>`;
    }
}
