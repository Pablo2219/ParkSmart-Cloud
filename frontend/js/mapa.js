let mapaParkSmart = null;
let marcadorUsuario = null;
let marcadoresEspacios = [];
let watcherUbicacion = null;

const UBICACION_INICIAL = [9.97625, -84.83836];

function inicializarMapa() {
    const contenedor = document.getElementById("mapa");
    if (!contenedor || mapaParkSmart) return;

    if (typeof L === "undefined") {
        mostrarMapaAlternativo(contenedor);
        return;
    }

    mapaParkSmart = L.map("mapa", {
        zoomControl: false,
        attributionControl: false
    }).setView(UBICACION_INICIAL, 15);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19
    }).addTo(mapaParkSmart);

    L.control.zoom({ position: "topright" }).addTo(mapaParkSmart);

    if (window.parkSmartState?.espacios) {
        actualizarMarcadoresMapa(window.parkSmartState.espacios);
    }
}

function mostrarMapaAlternativo(contenedor) {
    contenedor.classList.add("map-fallback");
    contenedor.innerHTML = `
        <span class="fallback-road road-one"></span>
        <span class="fallback-road road-two"></span>
        <button class="fallback-pin" type="button" onclick="mostrarToast('ParkSmart · Sector principal')">
            <strong>P</strong><span>ParkSmart</span>
        </button>
    `;
}

function actualizarMarcadoresMapa(espacios = []) {
    if (!mapaParkSmart || typeof L === "undefined") return;

    marcadoresEspacios.forEach(marcador => marcador.remove());
    marcadoresEspacios = [];

    espacios.slice(0, 8).forEach((espacio, index) => {
        const desplazamientoLat = ((index % 3) - 1) * 0.0018;
        const desplazamientoLng = (Math.floor(index / 3) - 0.5) * 0.0022;
        const coordenadas = [
            UBICACION_INICIAL[0] + desplazamientoLat,
            UBICACION_INICIAL[1] + desplazamientoLng
        ];

        const icono = L.divIcon({
            className: "parksmart-marker-wrapper",
            html: `<span class="parksmart-marker">${espacio.codigoEspacio}</span>`,
            iconSize: [44, 44],
            iconAnchor: [22, 38]
        });

        const marcador = L.marker(coordenadas, { icon: icono })
            .addTo(mapaParkSmart)
            .bindPopup(`<strong>Espacio ${espacio.codigoEspacio}</strong><br>${formatearTipoEspacioMapa(espacio.tipoEspacio)}`);

        marcador.on("click", () => {
            if (typeof abrirReserva === "function") abrirReserva(espacio.idEspacio);
        });

        marcadoresEspacios.push(marcador);
    });
}

function formatearTipoEspacioMapa(tipo = "REGULAR") {
    const nombres = {
        REGULAR: "Automóvil",
        MOTOCICLETA: "Motocicleta",
        DISCAPACIDAD: "Accesible",
        ELECTRICO: "Carga eléctrica",
        VIP: "VIP"
    };
    return nombres[tipo] || tipo;
}

function ubicarUsuario() {
    inicializarMapa();

    const texto = document.getElementById("ubicacionTexto");
    if (!navigator.geolocation) {
        texto.textContent = "Tu navegador no permite obtener la ubicación.";
        return;
    }

    texto.textContent = "Buscando tu ubicación...";

    if (watcherUbicacion) navigator.geolocation.clearWatch(watcherUbicacion);

    watcherUbicacion = navigator.geolocation.watchPosition(
        posicion => {
            const coordenadas = [posicion.coords.latitude, posicion.coords.longitude];
            const precision = Math.round(posicion.coords.accuracy);

            if (mapaParkSmart && typeof L !== "undefined") {
                if (!marcadorUsuario) {
                    marcadorUsuario = L.circleMarker(coordenadas, {
                        radius: 8,
                        color: "#ffffff",
                        weight: 3,
                        fillColor: "#2962ff",
                        fillOpacity: 1
                    }).addTo(mapaParkSmart);
                } else {
                    marcadorUsuario.setLatLng(coordenadas);
                }

                mapaParkSmart.setView(coordenadas, 16);
            }

            texto.textContent = `Ubicación encontrada · precisión aproximada de ${precision} m`;
            document.getElementById("ubicacionHeader").textContent = "Mi ubicación";
            guardarSesion("ultimaLatitud", coordenadas[0]);
            guardarSesion("ultimaLongitud", coordenadas[1]);
        },
        () => {
            texto.textContent = "No se pudo obtener la ubicación. Revisá el permiso del navegador.";
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 30000 }
    );
}
