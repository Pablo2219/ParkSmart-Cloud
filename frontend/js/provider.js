let proveedorMapa = null;
let proveedorMarkerLayer = null;
let proveedorCatalogo = { sectores: [], espacios: [] };
let proveedorPendiente = null;
let proveedorPerfil = null;
let proveedorVista = "operacion";

window.inicializarPanelProveedor = async function () {
    const app = document.getElementById("appShell");
    const contenido = document.querySelector(".app-content");
    if (!app || !contenido) return;

    document.body.classList.add("provider-session");
    document.body.classList.remove("admin-session");
    document.querySelector(".bottom-nav")?.classList.add("hidden");

    contenido.innerHTML = `
        <section id="vistaProveedor" class="provider-view">
            <div class="provider-heading">
                <div>
                    <span class="section-kicker">CENTRO DE OPERACIONES</span>
                    <h1 id="providerTitle">Mi parqueo</h1>
                    <p id="providerBusinessName">Cargando perfil...</p>
                </div>
                <button class="provider-logout" type="button" onclick="cerrarSesion()">Cerrar sesión</button>
            </div>

            <div class="provider-tabs" role="tablist">
                <button class="active" type="button" data-provider-tab="operacion" onclick="cambiarVistaProveedor('operacion')">Operación</button>
                <button type="button" data-provider-tab="reservas" onclick="cambiarVistaProveedor('reservas')">Reservas</button>
                <button type="button" data-provider-tab="billetera" onclick="cambiarVistaProveedor('billetera')">Billetera</button>
                <button type="button" data-provider-tab="perfil" onclick="cambiarVistaProveedor('perfil')">Mi perfil</button>
            </div>

            <div id="providerOperationView">
                <div class="provider-stats">
                    <article><strong id="providerSectorCount">0</strong><span>Sectores</span></article>
                    <article><strong id="providerSpaceCount">0</strong><span>Espacios</span></article>
                    <article><strong id="providerAvailableCount">0</strong><span>Disponibles</span></article>
                    <article><strong id="providerReservationCount">0</strong><span>Reservas</span></article>
                </div>

                <section class="provider-card">
                    <div class="provider-card-head">
                        <div><span class="section-kicker">OFERTA</span><h2>Registrar parqueo</h2><p>El sector y sus espacios se guardan en una sola operación. Primero ubicá el sector y luego cada espacio sobre el mapa.</p></div>
                        <button type="button" class="provider-refresh" onclick="cancelarParqueoPendiente(); seleccionarModoProveedor('PARQUEO')">+ Nuevo parqueo</button>
                    </div>
                    <div id="providerPendingPanel" class="provider-pending hidden"></div>
                    <div class="provider-tools">
                        <button id="providerModeParqueo" class="provider-mode active" type="button" onclick="seleccionarModoProveedor('PARQUEO')">+ Parqueo</button>
                        <button class="provider-mode" type="button" onclick="cancelarParqueoPendiente(); cargarCatalogoProveedor()">↻ Actualizar</button>
                    </div>
                    <div id="providerMap" class="provider-map"></div>
                    <p id="providerMapHint" class="provider-map-hint">Tocá el mapa para comenzar un nuevo parqueo. La ubicación queda registrada con coordenadas reales.</p>
                </section>

                <section class="provider-card">
                    <div class="provider-card-head"><div><span class="section-kicker">CATÁLOGO</span><h2>Mi oferta activa</h2><p>Todo lo que aparece aquí se publica automáticamente para los clientes.</p></div></div>
                    <div id="providerCatalogList" class="provider-list"></div>
                </section>
            </div>

            <div id="providerReservationsView" class="provider-panel-view hidden">
                <section class="provider-card"><div class="provider-card-head"><div><span class="section-kicker">DEMANDA</span><h2>Reservas recibidas</h2><p>Reservas hechas sobre tus espacios y sectores.</p></div><button class="provider-refresh" onclick="cargarReservasProveedor()">Actualizar</button></div><div id="providerReservationsList" class="provider-list"></div></section>
            </div>

            <div id="providerWalletView" class="provider-panel-view hidden">
                <section class="provider-card"><div class="provider-card-head"><div><span class="section-kicker">INGRESOS</span><h2>Billetera del proveedor</h2><p>Pagos registrados por reservas de tus espacios.</p></div><button class="provider-refresh" onclick="cargarBilleteraProveedor()">Actualizar</button></div><div class="provider-wallet-total"><small>Total cobrado</small><strong id="providerWalletTotal">₡0.00</strong><span id="providerWalletCount">0 pagos</span></div><div id="providerWalletList" class="provider-list"></div></section>
            </div>

            <div id="providerProfileView" class="provider-panel-view hidden">
                <section class="provider-card"><div class="provider-card-head"><div><span class="section-kicker">IDENTIDAD COMERCIAL</span><h2>Mi perfil</h2><p>Actualizá los datos que utilizan los clientes y el sistema.</p></div></div><form id="providerProfileForm" class="provider-form"><label>Nombre comercial<input id="providerProfileBusiness" required maxlength="120"></label><label>Teléfono<input id="providerProfilePhone" required maxlength="20"></label><label>Correo<input id="providerProfileEmail" type="email" required maxlength="120"></label><label>Dirección<input id="providerProfileAddress" maxlength="250"></label><div class="provider-form-grid"><label>Latitud<input id="providerProfileLat" type="number" step="0.0000001" min="-90" max="90"></label><label>Longitud<input id="providerProfileLng" type="number" step="0.0000001" min="-180" max="180"></label></div><button class="provider-primary" type="submit">Guardar cambios</button></form></section>
            </div>
        </section>`;

    insertarEstilosProveedor();
    inicializarMapaProveedor();
    document.getElementById("providerProfileForm")?.addEventListener("submit", actualizarPerfilProveedor);
    await cargarPerfilProveedor();
    await cargarCatalogoProveedor();
    await cargarReservasProveedor();
};

function insertarEstilosProveedor() {
    if (document.getElementById("providerStyles")) return;
    const style = document.createElement("style");
    style.id = "providerStyles";
    style.textContent = `
.provider-view{max-width:1180px;margin:0 auto;padding:10px 0 48px}.provider-heading{display:flex;justify-content:space-between;gap:20px;align-items:flex-start;margin-bottom:14px}.provider-heading h1{margin:4px 0 6px;font-size:clamp(28px,4vw,44px)}.provider-heading p{margin:0;color:#718096}.provider-tabs{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:18px}.provider-tabs button{border:1px solid #d7dee8;background:#fff;border-radius:12px;padding:10px 15px;cursor:pointer}.provider-tabs button.active{background:#07111f;color:#fff;border-color:#07111f}.provider-logout,.provider-refresh{border:1px solid #d7dee8;background:#fff;border-radius:12px;padding:10px 14px;cursor:pointer}.provider-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}.provider-stats article{background:#fff;border:1px solid #e5eaf0;border-radius:16px;padding:16px;box-shadow:0 8px 24px rgba(10,25,41,.05)}.provider-stats strong{display:block;font-size:28px}.provider-stats span{color:#718096;font-size:13px}.provider-card{background:#fff;border:1px solid #e5eaf0;border-radius:20px;padding:18px;margin-bottom:18px;box-shadow:0 10px 30px rgba(10,25,41,.05)}.provider-card-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:14px}.provider-card h2{margin:3px 0}.provider-card p{color:#718096;margin:4px 0;font-size:14px}.provider-tools{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}.provider-mode{border:1px solid #d7dee8;background:#fff;border-radius:10px;padding:9px 13px;cursor:pointer}.provider-mode.active{background:#07111f;color:#fff;border-color:#07111f}.provider-map{height:470px;border-radius:16px;overflow:hidden;border:1px solid #dfe5ec}.provider-map-hint{padding:10px 12px;background:#f7f9fb;border-radius:10px}.provider-list{display:grid;gap:9px;max-height:480px;overflow:auto}.provider-list-item{border:1px solid #e5eaf0;border-radius:12px;padding:12px}.provider-list-item strong{display:block}.provider-list-item small{color:#718096}.provider-empty{padding:22px;text-align:center;color:#718096;border:1px dashed #d7dee8;border-radius:12px}.provider-pending{background:#f7f9fb;border:1px solid #dfe5ec;border-radius:14px;padding:12px;margin-bottom:12px}.provider-pending strong{display:block}.provider-pending-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.provider-primary{border:0;background:#07111f;color:#fff;border-radius:12px;padding:12px 16px;cursor:pointer}.provider-form{display:grid;gap:13px}.provider-form label{display:grid;gap:6px;font-size:14px}.provider-form input{border:1px solid #d7dee8;border-radius:10px;padding:11px}.provider-form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.provider-panel-view.hidden,.provider-pending.hidden{display:none}.provider-wallet-total{padding:20px;background:#07111f;color:#fff;border-radius:16px;margin-bottom:15px}.provider-wallet-total small,.provider-wallet-total span{display:block;opacity:.75}.provider-wallet-total strong{display:block;font-size:36px;margin:6px 0}@media(max-width:850px){.provider-stats{grid-template-columns:1fr 1fr}.provider-heading{display:block}.provider-logout{margin-top:12px}}@media(max-width:600px){.provider-stats{grid-template-columns:1fr}.provider-map{height:390px}.provider-form-grid{grid-template-columns:1fr}}
    `;
    document.head.appendChild(style);
}

function inicializarMapaProveedor() {
    if (typeof L === "undefined") {
        document.getElementById("providerMapHint").textContent = "Leaflet no está disponible. Revisá la conexión a Internet.";
        return;
    }
    proveedorMapa = L.map("providerMap").setView([9.9347, -84.0875], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 20, attribution: "© OpenStreetMap" }).addTo(proveedorMapa);
    proveedorMarkerLayer = L.layerGroup().addTo(proveedorMapa);
    proveedorMapa.on("click", gestionarClickMapaProveedor);
}

function seleccionarModoProveedor(modo) {
    if (modo === "PARQUEO") {
        proveedorPendiente = null;
        renderPendienteParqueo();
        document.getElementById("providerMapHint").textContent = "Tocá el mapa en la ubicación del parqueo para crear el sector y luego agregá los espacios.";
    }
}

function cancelarParqueoPendiente() {
    proveedorPendiente = null;
    renderPendienteParqueo();
    if (document.getElementById("providerMapHint")) document.getElementById("providerMapHint").textContent = "Tocá el mapa para comenzar un nuevo parqueo.";
}

async function gestionarClickMapaProveedor(evento) {
    const { lat, lng } = evento.latlng;
    if (!proveedorPendiente) {
        const nombre = prompt("Nombre del sector / parqueo:", `Parqueo ${proveedorCatalogo.sectores.length + 1}`);
        if (!nombre?.trim()) return;
        const descripcion = prompt("Descripción (opcional):", "Parqueo administrado por ParkSmart") || null;
        proveedorPendiente = { nombreSector: nombre.trim(), descripcion, ubicacion: `${lat.toFixed(6)}, ${lng.toFixed(6)}`, latitud: lat, longitud: lng, espacios: [] };
        renderPendienteParqueo();
        document.getElementById("providerMapHint").textContent = "Ahora tocá el mapa para ubicar cada espacio. Podés agregar varios y guardar todo el parqueo en una sola operación.";
        return;
    }

    const codigo = prompt("Código del espacio:", `A-${proveedorPendiente.espacios.length + 1}`);
    if (!codigo?.trim()) return;
    const tipo = (prompt("Tipo: REGULAR, MOTOCICLETA, DISCAPACIDAD, ELECTRICO o VIP", "REGULAR") || "REGULAR").toUpperCase();
    if (!["REGULAR", "MOTOCICLETA", "DISCAPACIDAD", "ELECTRICO", "VIP"].includes(tipo)) return mostrarToast("Tipo de espacio inválido.");
    const descripcion = prompt("Descripción del espacio (opcional):", "") || null;
    proveedorPendiente.espacios.push({ codigoEspacio: codigo.trim().toUpperCase(), tipoEspacio: tipo, descripcion, latitud: lat, longitud: lng });
    renderPendienteParqueo();
}

function renderPendienteParqueo() {
    const panel = document.getElementById("providerPendingPanel");
    if (!panel) return;
    if (!proveedorPendiente) {
        panel.classList.add("hidden");
        return;
    }
    panel.classList.remove("hidden");
    panel.innerHTML = `<strong>${escaparHtml(proveedorPendiente.nombreSector)}</strong><small>${proveedorPendiente.espacios.length} espacios preparados para guardar</small><div class="provider-pending-actions"><button class="provider-primary" type="button" onclick="guardarParqueoProveedor()">Guardar parqueo completo</button><button class="provider-refresh" type="button" onclick="cancelarParqueoPendiente()">Cancelar</button></div>`;
}

async function guardarParqueoProveedor() {
    if (!proveedorPendiente) return;
    if (!proveedorPendiente.espacios.length) return mostrarToast("Agregá al menos un espacio antes de guardar el parqueo.");
    try {
        const resultado = await fetchAPI("/proveedores/parqueos", { method: "POST", body: JSON.stringify(proveedorPendiente) });
        mostrarToast(resultado.mensaje || "Parqueo guardado.");
        proveedorPendiente = null;
        renderPendienteParqueo();
        await cargarCatalogoProveedor();
    } catch (error) {
        mostrarToast(error.message);
    }
}

async function cargarPerfilProveedor() {
    try {
        proveedorPerfil = await fetchAPI("/proveedores/perfil");
        document.getElementById("providerBusinessName").textContent = proveedorPerfil.nombreComercial;
        document.getElementById("providerTitle").textContent = proveedorPerfil.nombreComercial || "Mi parqueo";
        document.getElementById("providerProfileBusiness").value = proveedorPerfil.nombreComercial || "";
        document.getElementById("providerProfilePhone").value = proveedorPerfil.telefono || "";
        document.getElementById("providerProfileEmail").value = proveedorPerfil.correoElectronico || "";
        document.getElementById("providerProfileAddress").value = proveedorPerfil.direccion || "";
        document.getElementById("providerProfileLat").value = proveedorPerfil.latitud ?? "";
        document.getElementById("providerProfileLng").value = proveedorPerfil.longitud ?? "";
    } catch (error) { mostrarToast(error.message); }
}

async function actualizarPerfilProveedor(evento) {
    evento.preventDefault();
    try {
        await fetchAPI("/proveedores/perfil", { method: "PUT", body: JSON.stringify({ nombreComercial: document.getElementById("providerProfileBusiness").value.trim(), telefono: document.getElementById("providerProfilePhone").value.trim(), correoElectronico: document.getElementById("providerProfileEmail").value.trim(), direccion: document.getElementById("providerProfileAddress").value.trim() || null, latitud: Number(document.getElementById("providerProfileLat").value) || null, longitud: Number(document.getElementById("providerProfileLng").value) || null }) });
        await cargarPerfilProveedor();
        mostrarToast("Perfil actualizado.");
    } catch (error) { mostrarToast(error.message); }
}

async function cargarCatalogoProveedor() {
    try {
        proveedorCatalogo = await fetchAPI("/proveedores/mi-catalogo");
        const resumen = await fetchAPI("/proveedores/resumen");
        document.getElementById("providerSectorCount").textContent = resumen.sectores;
        document.getElementById("providerSpaceCount").textContent = resumen.espacios;
        document.getElementById("providerAvailableCount").textContent = resumen.disponibles;
        document.getElementById("providerReservationCount").textContent = resumen.reservas;
        renderCatalogoProveedor();
        renderMarcadoresProveedor();
    } catch (error) { mostrarToast(error.message); }
}

function renderCatalogoProveedor() {
    const contenedor = document.getElementById("providerCatalogList");
    if (!contenedor) return;
    if (!proveedorCatalogo.sectores.length) {
        contenedor.innerHTML = `<div class="provider-empty">Todavía no tenés oferta. Usá “+ Nuevo parqueo” y registrá el sector con sus espacios.</div>`;
        return;
    }
    contenedor.innerHTML = proveedorCatalogo.sectores.map(sector => {
        const espacios = proveedorCatalogo.espacios.filter(e => e.idSector === sector.idSector);
        return `<article class="provider-list-item"><strong>${escaparHtml(sector.nombreSector)}</strong><small>${escaparHtml(sector.ubicacion || "Sin dirección")}</small><div style="margin-top:8px">${espacios.map(e => `<span class="provider-badge">${escaparHtml(e.codigoEspacio)} · ${escaparHtml(e.tipoEspacio)} · ${escaparHtml(e.estado)}</span>`).join(" ")}</div></article>`;
    }).join("");
}

function renderMarcadoresProveedor() {
    if (!proveedorMapa || !proveedorMarkerLayer || typeof L === "undefined") return;
    proveedorMarkerLayer.clearLayers();
    const bounds = [];
    proveedorCatalogo.sectores.forEach(sector => {
        if (sector.latitud == null || sector.longitud == null) return;
        proveedorMarkerLayer.addLayer(L.marker([Number(sector.latitud), Number(sector.longitud)]).bindPopup(`<strong>${escaparHtml(sector.nombreSector)}</strong><br>Sector de parqueo`));
        bounds.push([Number(sector.latitud), Number(sector.longitud)]);
    });
    proveedorCatalogo.espacios.forEach(espacio => {
        if (espacio.latitud == null || espacio.longitud == null) return;
        proveedorMarkerLayer.addLayer(L.circleMarker([Number(espacio.latitud), Number(espacio.longitud)], { radius: 8, weight: 2, fillOpacity: .8 }).bindPopup(`<strong>${escaparHtml(espacio.codigoEspacio)}</strong><br>${escaparHtml(espacio.tipoEspacio)} · ${escaparHtml(espacio.estado)}`));
        bounds.push([Number(espacio.latitud), Number(espacio.longitud)]);
    });
    if (bounds.length) proveedorMapa.fitBounds(bounds, { padding: [30, 30], maxZoom: 17 });
}

async function cargarReservasProveedor() {
    const contenedor = document.getElementById("providerReservationsList");
    if (!contenedor) return;
    try {
        const reservas = await fetchAPI("/proveedores/reservas");
        document.getElementById("providerReservationCount").textContent = reservas.length;
        contenedor.innerHTML = reservas.length ? reservas.map(r => `<div class="provider-list-item"><strong>${escaparHtml(r.codigoEspacio)} · ${escaparHtml(r.nombreSector)}</strong><small>Cliente #${r.idCliente} · ${escaparHtml(r.estado)}</small><br><small>${formatearFecha(r.fechaInicioReserva)} → ${formatearFecha(r.fechaFinReserva)}</small></div>`).join("") : `<div class="provider-empty">Todavía no hay reservas sobre tus espacios.</div>`;
    } catch (error) { contenedor.innerHTML = `<div class="provider-empty">${escaparHtml(error.message)}</div>`; }
}

async function cargarBilleteraProveedor() {
    const lista = document.getElementById("providerWalletList");
    try {
        const billetera = await fetchAPI("/proveedores/billetera");
        document.getElementById("providerWalletTotal").textContent = `₡${Number(billetera.totalPagado || 0).toLocaleString("es-CR", { minimumFractionDigits: 2 })}`;
        document.getElementById("providerWalletCount").textContent = `${billetera.cantidadPagos || 0} pagos`;
        lista.innerHTML = billetera.movimientos.length ? billetera.movimientos.map(m => `<div class="provider-list-item"><strong>${escaparHtml(m.codigoPago)}</strong><small>${escaparHtml(m.estado)} · ${escaparHtml(m.metodoPago || "Pendiente")}</small><br><small>₡${Number(m.montoTotal || 0).toLocaleString("es-CR", { minimumFractionDigits: 2 })} · ${m.fechaPago ? formatearFecha(m.fechaPago) : "Sin fecha"}</small></div>`).join("") : `<div class="provider-empty">Todavía no hay pagos liquidados.</div>`;
    } catch (error) { lista.innerHTML = `<div class="provider-empty">${escaparHtml(error.message)}</div>`; }
}

function cambiarVistaProveedor(vista) {
    proveedorVista = vista;
    document.querySelectorAll("[data-provider-tab]").forEach(tab => tab.classList.toggle("active", tab.dataset.providerTab === vista));
    document.getElementById("providerOperationView")?.classList.toggle("hidden", vista !== "operacion");
    document.getElementById("providerReservationsView")?.classList.toggle("hidden", vista !== "reservas");
    document.getElementById("providerWalletView")?.classList.toggle("hidden", vista !== "billetera");
    document.getElementById("providerProfileView")?.classList.toggle("hidden", vista !== "perfil");
    if (vista === "reservas") cargarReservasProveedor();
    if (vista === "billetera") cargarBilleteraProveedor();
    if (vista === "perfil") cargarPerfilProveedor();
}
