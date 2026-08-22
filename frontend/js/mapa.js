let mapaParkSmart = null;
let marcadorUsuario = null;
let marcadoresEspacios = [];
let marcadoresSectores = [];
let watcherUbicacion = null;

const UBICACION_INICIAL = [9.9347, -84.0875];

function inicializarMapa() {
    const contenedor = document.getElementById("mapa");
    if (!contenedor || mapaParkSmart) return;
    if (typeof L === "undefined") return mostrarMapaAlternativo(contenedor);

    mapaParkSmart = L.map("mapa", { zoomControl: false, attributionControl: false }).setView(UBICACION_INICIAL, 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "© OpenStreetMap" }).addTo(mapaParkSmart);
    L.control.zoom({ position: "topright" }).addTo(mapaParkSmart);
    actualizarMarcadoresMapa(window.parkSmartState?.espacios || [], window.parkSmartState?.sectores || []);
}

function mostrarMapaAlternativo(contenedor) {
    contenedor.classList.add("map-fallback");
    contenedor.innerHTML = `<span class="fallback-road road-one"></span><span class="fallback-road road-two"></span><button class="fallback-pin" type="button"><strong>P</strong><span>ParkSmart</span></button>`;
}

function actualizarMarcadoresMapa(espacios = [], sectores = []) {
    if (!mapaParkSmart || typeof L === "undefined") return;
    marcadoresEspacios.forEach(m => m.remove());
    marcadoresSectores.forEach(m => m.remove());
    marcadoresEspacios = [];
    marcadoresSectores = [];
    const bounds = [];

    sectores.forEach(sector => {
        if (sector.latitud == null || sector.longitud == null) return;
        const marker = L.circleMarker([Number(sector.latitud), Number(sector.longitud)], { radius: 12, weight: 3, fillOpacity: .15 })
            .addTo(mapaParkSmart)
            .bindPopup(`<strong>${escaparHtml(sector.nombreSector)}</strong><br>Sector de parqueo`);
        marcadoresSectores.push(marker);
        bounds.push([Number(sector.latitud), Number(sector.longitud)]);
    });

    espacios.filter(e => e.estado === "DISPONIBLE" || e.estado === "RESERVADO").forEach(espacio => {
        let coordenadas;
        if (espacio.latitud != null && espacio.longitud != null) {
            coordenadas = [Number(espacio.latitud), Number(espacio.longitud)];
        } else {
            // Compatibilidad con datos antiguos que todavía no tienen coordenadas.
            const index = marcadoresEspacios.length;
            coordenadas = [UBICACION_INICIAL[0] + ((index % 3) - 1) * 0.0018, UBICACION_INICIAL[1] + (Math.floor(index / 3) - 0.5) * 0.0022];
        }

        const icono = L.divIcon({ className: "parksmart-marker-wrapper", html: `<span class="parksmart-marker">${escaparHtml(espacio.codigoEspacio)}</span>`, iconSize: [44, 44], iconAnchor: [22, 38] });
        const marker = L.marker(coordenadas, { icon: icono }).addTo(mapaParkSmart)
            .bindPopup(`<strong>Espacio ${escaparHtml(espacio.codigoEspacio)}</strong><br>${formatearTipoEspacioMapa(espacio.tipoEspacio)}<br>${escaparHtml(espacio.estado)}`);
        marker.on("click", () => { if (typeof abrirReserva === "function") abrirReserva(espacio.idEspacio); });
        marcadoresEspacios.push(marker);
        bounds.push(coordenadas);
    });

    if (bounds.length) mapaParkSmart.fitBounds(bounds, { padding: [24, 24], maxZoom: 17 });
}

function formatearTipoEspacioMapa(tipo = "REGULAR") {
    return { REGULAR: "Automóvil", MOTOCICLETA: "Motocicleta", DISCAPACIDAD: "Accesible", ELECTRICO: "Carga eléctrica", VIP: "VIP" }[tipo] || tipo;
}

function ubicarUsuario() {
    inicializarMapa();
    const texto = document.getElementById("ubicacionTexto");
    if (!navigator.geolocation) return (texto.textContent = "Tu navegador no permite obtener la ubicación.");
    texto.textContent = "Buscando tu ubicación...";
    if (watcherUbicacion) navigator.geolocation.clearWatch(watcherUbicacion);
    watcherUbicacion = navigator.geolocation.watchPosition(
        posicion => {
            const coordenadas = [posicion.coords.latitude, posicion.coords.longitude];
            const precision = Math.round(posicion.coords.accuracy);
            if (mapaParkSmart && typeof L !== "undefined") {
                if (!marcadorUsuario) marcadorUsuario = L.circleMarker(coordenadas, { radius: 8, color: "#ffffff", weight: 3, fillColor: "#2962ff", fillOpacity: 1 }).addTo(mapaParkSmart);
                else marcadorUsuario.setLatLng(coordenadas);
                mapaParkSmart.setView(coordenadas, 16);
            }
            texto.textContent = `Ubicación encontrada · precisión aproximada de ${precision} m`;
            document.getElementById("ubicacionHeader").textContent = "Mi ubicación";
            localStorage.setItem("parksmart_ultima_latitud", String(coordenadas[0]));
            localStorage.setItem("parksmart_ultima_longitud", String(coordenadas[1]));
        },
        () => { texto.textContent = "No se pudo obtener la ubicación. Revisá el permiso del navegador."; },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 30000 }
    );
}
