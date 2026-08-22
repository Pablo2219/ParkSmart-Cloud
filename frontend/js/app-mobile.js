let CLIENTE_ACTUAL_ID = Number(localStorage.getItem("parksmart_cliente_id")) || 1;
const ESTADOS_RESERVA_ACTIVA = ["PENDIENTE", "CONFIRMADA"];
const TARIFA_REFERENCIA = 700;

const parkSmartState = {
    online: false,
    demo: false,
    cliente: null,
    espacios: [],
    catalogoEspacios: [],
    sectores: [],
    reservas: [],
    vehiculos: [],
    pagos: [],
    notificaciones: [],
    qrs: new Map(),
    filtroEspacio: "TODOS",
    filtroReserva: "ACTIVAS",
    ordenAscendente: true
};

window.parkSmartState = parkSmartState;

document.addEventListener("DOMContentLoaded", async () => {
    aplicarTemaGuardado();
    configurarEventos();

    const autenticado = await inicializarAutenticacion();
    if (!autenticado) return;

    CLIENTE_ACTUAL_ID = Number(window.parkSmartSession.usuario?.idCliente)
        || Number(localStorage.getItem("parksmart_cliente_id"))
        || 1;
    localStorage.setItem("parksmart_cliente_id", String(CLIENTE_ACTUAL_ID));

    const vistaGuardada = obtenerSesion("vistaActual", "vistaInicio");
    const navGuardado = obtenerSesion("navActual", "navInicio");
    cambiarVista(vistaGuardada, navGuardado, false);

    await recargarDatos(true);
});

function configurarEventos() {
    document.getElementById("buscarEspacio").addEventListener("input", renderEspacios);

    document.querySelectorAll("[data-filter]").forEach(boton => {
        boton.addEventListener("click", () => {
            document.querySelectorAll("[data-filter]").forEach(item => item.classList.remove("active"));
            boton.classList.add("active");
            parkSmartState.filtroEspacio = boton.dataset.filter;
            renderEspacios();
        });
    });

    document.querySelectorAll("[data-reservation-filter]").forEach(boton => {
        boton.addEventListener("click", () => {
            document.querySelectorAll("[data-reservation-filter]").forEach(item => item.classList.remove("active"));
            boton.classList.add("active");
            parkSmartState.filtroReserva = boton.dataset.reservationFilter;
            renderReservas();
        });
    });

    document.getElementById("reservaForm").addEventListener("submit", confirmarReserva);
    document.getElementById("reservaInicio").addEventListener("change", actualizarTotalReserva);
    document.getElementById("reservaFin").addEventListener("change", actualizarTotalReserva);

    document.querySelectorAll("dialog").forEach(dialogo => {
        dialogo.addEventListener("click", evento => {
            if (evento.target === dialogo) cerrarDialogo(dialogo.id);
        });
    });
}

async function recargarDatos(silencioso = false) {
    if (!silencioso) mostrarToast("Actualizando información...");
    establecerEstadoApi("loading");

    try {
        await verificarApi();

        const resultados = await Promise.allSettled([
            apiGet(`/clientes/${CLIENTE_ACTUAL_ID}`),
            apiGet("/espacios/disponibles"),
            apiGet("/espacios/"),
            apiGet("/espacios/sectores"),
            apiGet(`/reservas/cliente/${CLIENTE_ACTUAL_ID}`),
            apiGet(`/vehiculos/cliente/${CLIENTE_ACTUAL_ID}`),
            apiGet(`/notificaciones/cliente/${CLIENTE_ACTUAL_ID}`)
        ]);

        const [cliente, espacios, catalogo, sectores, reservas, vehiculos, notificaciones] = resultados;

        if (cliente.status !== "fulfilled" || espacios.status !== "fulfilled") {
            throw new Error("No se pudieron obtener los datos principales.");
        }

        parkSmartState.cliente = cliente.value;
        parkSmartState.espacios = espacios.value || [];
        parkSmartState.catalogoEspacios = catalogo.status === "fulfilled" ? catalogo.value : [...parkSmartState.espacios];
        parkSmartState.sectores = sectores.status === "fulfilled" ? sectores.value : [];
        parkSmartState.reservas = reservas.status === "fulfilled" ? reservas.value : [];
        parkSmartState.vehiculos = vehiculos.status === "fulfilled" ? vehiculos.value : [];
        parkSmartState.notificaciones = notificaciones.status === "fulfilled" ? notificaciones.value : [];
        parkSmartState.pagos = await cargarPagosDelCliente(parkSmartState.reservas);
        parkSmartState.online = true;
        parkSmartState.demo = false;
        establecerEstadoApi("online");
    } catch (error) {
        console.warn("ParkSmart API no disponible; se usa la vista de demostración.", error);
        Object.assign(parkSmartState, crearDatosDemo(), {
            online: false,
            demo: true,
            qrs: new Map()
        });
        parkSmartState.catalogoEspacios = [
            ...parkSmartState.espacios,
            { idEspacio: 8, idSector: 1, codigoEspacio: "A-08", tipoEspacio: "REGULAR", estado: "RESERVADO", descripcion: "Junto a la entrada" },
            { idEspacio: 1, idSector: 1, codigoEspacio: "A-01", tipoEspacio: "REGULAR", estado: "OCUPADO", descripcion: "Entrada principal" }
        ];
        establecerEstadoApi("offline");
    }

    renderAplicacion();

    if (!silencioso) {
        mostrarToast(parkSmartState.online ? "Datos actualizados" : "Mostrando datos de demostración");
    }
}

async function cargarPagosDelCliente(reservas) {
    const ocupaciones = [];
    const respuestasOcupaciones = await Promise.allSettled(
        reservas.map(reserva => apiGet(`/ocupaciones/reserva/${reserva.idReserva}`))
    );

    respuestasOcupaciones.forEach(resultado => {
        if (resultado.status === "fulfilled") ocupaciones.push(...resultado.value);
    });

    const respuestasPagos = await Promise.allSettled(
        ocupaciones.map(ocupacion => apiGet(`/pagos/ocupacion/${ocupacion.idOcupacion}`))
    );

    return respuestasPagos.flatMap(resultado => resultado.status === "fulfilled" ? resultado.value : []);
}

function crearDatosDemo() {
    const inicioProximo = nuevaFechaRelativa(2);
    const finProximo = nuevaFechaRelativa(4);
    const fechaAyer = nuevaFechaRelativa(-24);

    return {
        cliente: {
            idCliente: 1,
            nombre: "Carlos",
            primerApellido: "Aguirre",
            segundoApellido: "",
            correoElectronico: "carlos.prueba@parksmart.com",
            telefono: "8888-9999",
            estado: "ACTIVO"
        },
        sectores: [
            { idSector: 1, nombreSector: "Sector Central", ubicacion: "Entrada principal", estado: "ACTIVO" },
            { idSector: 2, nombreSector: "Sector Norte", ubicacion: "Acceso lateral", estado: "ACTIVO" }
        ],
        espacios: [
            { idEspacio: 2, idSector: 1, codigoEspacio: "A-02", tipoEspacio: "REGULAR", estado: "DISPONIBLE", descripcion: "Cerca de la entrada principal" },
            { idEspacio: 3, idSector: 1, codigoEspacio: "A-03", tipoEspacio: "MOTOCICLETA", estado: "DISPONIBLE", descripcion: "Zona cubierta" },
            { idEspacio: 4, idSector: 2, codigoEspacio: "B-01", tipoEspacio: "ELECTRICO", estado: "DISPONIBLE", descripcion: "Punto de carga disponible" },
            { idEspacio: 5, idSector: 2, codigoEspacio: "B-04", tipoEspacio: "VIP", estado: "DISPONIBLE", descripcion: "Acceso preferencial" }
        ],
        reservas: [
            {
                idReserva: 9001,
                idCliente: 1,
                idVehiculo: 1,
                idEspacio: 8,
                codigoReserva: "RES-DEMO-2026",
                fechaInicioReserva: inicioProximo,
                fechaFinReserva: finProximo,
                estado: "CONFIRMADA",
                observaciones: "Reserva de demostración"
            },
            {
                idReserva: 9000,
                idCliente: 1,
                idVehiculo: 1,
                idEspacio: 1,
                codigoReserva: "RES-ANTERIOR",
                fechaInicioReserva: fechaAyer,
                fechaFinReserva: nuevaFechaRelativa(-22),
                estado: "UTILIZADA",
                observaciones: null
            }
        ],
        vehiculos: [
            { idVehiculo: 1, idCliente: 1, placa: "ABC123", marca: "Toyota", modelo: "RAV4", color: "Gris", tipoVehiculo: "AUTOMOVIL", estado: "ACTIVO" }
        ],
        pagos: [
            { idPago: 1, codigoPago: "PAG-DEMO-001", montoTotal: 1400, metodoPago: "TARJETA", estado: "PAGADO", fechaPago: fechaAyer, fechaGeneracion: fechaAyer }
        ],
        notificaciones: [
            { idNotificacion: 1, titulo: "Reserva confirmada", mensaje: "Tu espacio estará listo 10 minutos antes de la hora seleccionada.", tipoNotificacion: "RESERVA", canal: "APP", estado: "ENVIADA", fechaCreacion: nuevaFechaRelativa(-1) },
            { idNotificacion: 2, titulo: "Bienvenido a ParkSmart", mensaje: "Ya podés encontrar y reservar espacios desde la app.", tipoNotificacion: "SISTEMA", canal: "APP", estado: "LEIDA", fechaCreacion: fechaAyer }
        ]
    };
}

function nuevaFechaRelativa(horas) {
    return new Date(Date.now() + horas * 60 * 60 * 1000).toISOString();
}

function renderAplicacion() {
    renderPerfil();
    renderInicio();
    renderEspacios();
    renderReservas();
    renderPagos();
    renderVehiculos();
    renderNotificaciones();

    if (mapaParkSmart) actualizarMarcadoresMapa(parkSmartState.espacios);
}

function renderPerfil() {
    const cliente = parkSmartState.cliente;
    if (!cliente) return;

    const nombreCompleto = [cliente.nombre, cliente.primerApellido, cliente.segundoApellido]
        .filter(Boolean)
        .join(" ");
    const iniciales = obtenerIniciales(nombreCompleto);

    const usuarioSesion = window.parkSmartSession?.usuario;
    const esAdministrador = usuarioSesion?.rol === "ADMINISTRADOR";
    const nombreCuenta = esAdministrador
        ? (usuarioSesion.nombreUsuario || "Administrador")
        : nombreCompleto;
    const inicialesCuenta = obtenerIniciales(nombreCuenta);

    asignarTexto("nombreUsuario", esAdministrador ? "Administrador" : (cliente.nombre || "Cliente"));
    asignarTexto("avatarIniciales", inicialesCuenta);
    asignarTexto("profileIniciales", inicialesCuenta);
    asignarTexto("profileNombre", nombreCuenta);
    asignarTexto("profileCorreo", usuarioSesion?.correoElectronico || cliente.correoElectronico || "Sin correo registrado");
    asignarTexto("profileRole", esAdministrador ? "Administrador" : "Cliente");
    asignarTexto("walletOwner", (esAdministrador ? "PARKSMART ADMIN" : nombreCompleto).toUpperCase());
}

function renderInicio() {
    const disponibles = parkSmartState.espacios;
    asignarTexto("heroSpaceCode", disponibles[0]?.codigoEspacio || "LIBRE");

    const contenedor = document.getElementById("parqueosInicio");
    if (!disponibles.length) {
        contenedor.innerHTML = estadoVacio("P", "Sin espacios disponibles", "Volvé a revisar en unos minutos.");
    } else {
        contenedor.innerHTML = disponibles.slice(0, 2).map(espacio => tarjetaEspacioPreview(espacio)).join("");
    }

    const reservasActivas = parkSmartState.reservas
        .filter(reserva => ESTADOS_RESERVA_ACTIVA.includes(reserva.estado))
        .sort((a, b) => new Date(a.fechaInicioReserva) - new Date(b.fechaInicioReserva));

    const seccion = document.getElementById("reservaActivaSection");
    const contenedorActiva = document.getElementById("reservaActiva");

    if (!reservasActivas.length) {
        seccion.classList.add("hidden");
    } else {
        seccion.classList.remove("hidden");
        const reserva = reservasActivas[0];
        contenedorActiva.innerHTML = tarjetaReservaActiva(reserva);
    }

    document.getElementById("modeBanner").classList.toggle("hidden", !parkSmartState.demo);
}

function tarjetaEspacioPreview(espacio) {
    const sector = obtenerSector(espacio.idSector);
    return `
        <article class="parking-preview-card">
            <div class="space-thumbnail ${claseTipo(espacio.tipoEspacio)}">${escaparHtml(espacio.codigoEspacio)}</div>
            <div>
                <h3>${escaparHtml(sector?.nombreSector || `Sector ${espacio.idSector}`)}</h3>
                <p>${escaparHtml(espacio.descripcion || sector?.ubicacion || "Espacio disponible")}</p>
                <div class="space-tags"><span class="status-tag">Disponible</span><span class="type-tag">${formatearTipo(espacio.tipoEspacio)}</span></div>
            </div>
            <button class="parking-card-action" type="button" onclick="abrirReserva(${Number(espacio.idEspacio)})">Elegir</button>
        </article>
    `;
}

function tarjetaReservaActiva(reserva) {
    const espacio = obtenerEspacio(reserva.idEspacio);
    const vehiculo = obtenerVehiculo(reserva.idVehiculo);
    return `
        <article class="active-reservation-card">
            <div class="reservation-summary">
                <span class="reservation-icon">${escaparHtml(espacio?.codigoEspacio || "P")}</span>
                <div><h3>${escaparHtml(espacio?.codigoEspacio ? `Espacio ${espacio.codigoEspacio}` : reserva.codigoReserva)}</h3><p>${formatearFechaCorta(reserva.fechaInicioReserva)} · ${escaparHtml(vehiculo?.placa || "Vehículo registrado")}</p></div>
                <div class="reservation-countdown"><strong>${formatearHora(reserva.fechaInicioReserva)}</strong><small>HORA DE ENTRADA</small></div>
            </div>
            <button class="reservation-cta" type="button" onclick="mostrarQrReserva(${Number(reserva.idReserva)})">Ver acceso QR →</button>
        </article>
    `;
}

function renderEspacios() {
    const contenedor = document.getElementById("espaciosContenedor");
    const busqueda = document.getElementById("buscarEspacio").value.trim().toLowerCase();

    let espacios = [...parkSmartState.espacios].filter(espacio => {
        const sector = obtenerSector(espacio.idSector);
        const texto = `${espacio.codigoEspacio} ${espacio.tipoEspacio} ${sector?.nombreSector || ""} ${espacio.descripcion || ""}`.toLowerCase();
        const coincideTipo = parkSmartState.filtroEspacio === "TODOS" || espacio.tipoEspacio === parkSmartState.filtroEspacio;
        return coincideTipo && texto.includes(busqueda);
    });

    espacios.sort((a, b) => {
        const comparacion = a.codigoEspacio.localeCompare(b.codigoEspacio, "es", { numeric: true });
        return parkSmartState.ordenAscendente ? comparacion : -comparacion;
    });

    asignarTexto("resultadosConteo", espacios.length);
    asignarTexto("mapAvailableCount", `${parkSmartState.espacios.length} libres`);

    if (!espacios.length) {
        contenedor.innerHTML = estadoVacio("⌕", "No encontramos coincidencias", "Probá con otro sector o tipo de vehículo.");
        return;
    }

    contenedor.innerHTML = espacios.map((espacio, index) => {
        const sector = obtenerSector(espacio.idSector);
        return `
            <article class="space-card">
                <div class="space-thumbnail ${claseTipo(espacio.tipoEspacio)}">${escaparHtml(espacio.codigoEspacio)}</div>
                <div class="space-main">
                    <h3>${escaparHtml(sector?.nombreSector || `Sector ${espacio.idSector}`)}</h3>
                    <p>${escaparHtml(espacio.descripcion || sector?.ubicacion || "Disponible para reservar")}</p>
                    <div class="space-tags"><span class="status-tag">Libre ahora</span><span class="type-tag">${formatearTipo(espacio.tipoEspacio)}</span></div>
                </div>
                <span class="space-distance">${(0.2 + index * 0.15).toFixed(1)} km</span>
                <button class="parking-card-action" type="button" onclick="abrirReserva(${Number(espacio.idEspacio)})">Reservar</button>
            </article>
        `;
    }).join("");
}

function renderReservas() {
    const contenedor = document.getElementById("reservasContenedor");
    const activas = parkSmartState.filtroReserva === "ACTIVAS";
    const reservas = parkSmartState.reservas
        .filter(reserva => activas === ESTADOS_RESERVA_ACTIVA.includes(reserva.estado))
        .sort((a, b) => new Date(b.fechaInicioReserva) - new Date(a.fechaInicioReserva));

    if (!reservas.length) {
        contenedor.innerHTML = estadoVacio("P", activas ? "No tenés reservas próximas" : "Todavía no hay historial", activas ? "Explorá espacios disponibles para crear la primera." : "Tus reservas completadas aparecerán aquí.");
        return;
    }

    contenedor.innerHTML = reservas.map(reserva => {
        const espacio = obtenerEspacio(reserva.idEspacio);
        const vehiculo = obtenerVehiculo(reserva.idVehiculo);
        const activa = ESTADOS_RESERVA_ACTIVA.includes(reserva.estado);
        return `
            <article class="reservation-card">
                <div class="reservation-card-top">
                    <div><h3>${escaparHtml(espacio?.codigoEspacio ? `Espacio ${espacio.codigoEspacio}` : reserva.codigoReserva)}</h3><p>${escaparHtml(reserva.codigoReserva)}</p></div>
                    <span class="state-pill ${reserva.estado.toLowerCase()}">${formatearEstado(reserva.estado)}</span>
                </div>
                <div class="reservation-details">
                    <span><small>Entrada</small><strong>${formatearFechaCorta(reserva.fechaInicioReserva)} · ${formatearHora(reserva.fechaInicioReserva)}</strong></span>
                    <span><small>Salida</small><strong>${formatearFechaCorta(reserva.fechaFinReserva)} · ${formatearHora(reserva.fechaFinReserva)}</strong></span>
                    <span><small>Vehículo</small><strong>${escaparHtml(vehiculo?.placa || `ID ${reserva.idVehiculo}`)}</strong></span>
                    <span><small>Sector</small><strong>${escaparHtml(obtenerSector(espacio?.idSector)?.nombreSector || "ParkSmart")}</strong></span>
                </div>
                ${activa ? `<div class="reservation-actions"><button type="button" onclick="mostrarQrReserva(${Number(reserva.idReserva)})">Mostrar código QR</button><button type="button" onclick="cancelarReserva(${Number(reserva.idReserva)})">Cancelar</button></div>` : ""}
            </article>
        `;
    }).join("");
}

function renderPagos() {
    const contenedor = document.getElementById("pagosContenedor");
    const total = parkSmartState.pagos
        .filter(pago => pago.estado === "PAGADO")
        .reduce((suma, pago) => suma + Number(pago.montoTotal || 0), 0);

    asignarTexto("totalPagado", formatearMoneda(total));

    if (!parkSmartState.pagos.length) {
        contenedor.innerHTML = estadoVacio("₡", "No hay movimientos", "Los pagos vinculados a tus reservas aparecerán aquí.");
        return;
    }

    contenedor.innerHTML = parkSmartState.pagos.map(pago => `
        <article class="payment-item">
            <span class="payment-icon">₡</span>
            <div><h3>${escaparHtml(pago.codigoPago || "Pago ParkSmart")}</h3><p>${formatearFechaCorta(pago.fechaPago || pago.fechaGeneracion)} · ${formatearEstado(pago.metodoPago || "Pendiente")}</p></div>
            <div class="payment-amount"><strong>${formatearMoneda(pago.montoTotal)}</strong><small>${formatearEstado(pago.estado)}</small></div>
        </article>
    `).join("");
}

function renderVehiculos() {
    const contenedor = document.getElementById("vehiculosContenedor");
    if (!parkSmartState.vehiculos.length) {
        contenedor.innerHTML = estadoVacio("+", "No hay vehículos", "Registrá un vehículo desde la API para reservar.");
        return;
    }

    contenedor.innerHTML = parkSmartState.vehiculos.map(vehiculo => `
        <article class="vehicle-item">
            <span class="vehicle-icon">${vehiculo.tipoVehiculo === "MOTOCICLETA" ? "M" : "A"}</span>
            <div><h3>${escaparHtml([vehiculo.marca, vehiculo.modelo].filter(Boolean).join(" ") || formatearTipo(vehiculo.tipoVehiculo))}</h3><p>${escaparHtml(vehiculo.color || "Color no registrado")} · ${formatearEstado(vehiculo.estado)}</p></div>
            <span class="vehicle-plate">${escaparHtml(vehiculo.placa)}</span>
        </article>
    `).join("");
}

function renderNotificaciones() {
    const contenedor = document.getElementById("notificacionesContenedor");
    const noLeidas = parkSmartState.notificaciones.filter(notificacion => notificacion.estado !== "LEIDA").length;
    const badge = document.getElementById("notificationBadge");
    badge.textContent = noLeidas;
    badge.classList.toggle("hidden", noLeidas === 0);

    if (!parkSmartState.notificaciones.length) {
        contenedor.innerHTML = estadoVacio("!", "Todo al día", "No tenés notificaciones nuevas.");
        return;
    }

    contenedor.innerHTML = parkSmartState.notificaciones.map(notificacion => `
        <article class="notification-item ${notificacion.estado !== "LEIDA" ? "unread" : ""}">
            <span class="notification-item-icon">${iconoNotificacion(notificacion.tipoNotificacion)}</span>
            <div><h3>${escaparHtml(notificacion.titulo)}</h3><p>${escaparHtml(notificacion.mensaje)}</p><time>${tiempoRelativo(notificacion.fechaEnvio || notificacion.fechaCreacion)}</time></div>
        </article>
    `).join("");
}

function cambiarVista(idVista, idNav, desplazar = true) {
    const vista = document.getElementById(idVista);
    const nav = document.getElementById(idNav);
    if (!vista || !nav) {
        idVista = "vistaInicio";
        idNav = "navInicio";
    }

    document.querySelectorAll(".view").forEach(elemento => elemento.classList.remove("active-view"));
    document.querySelectorAll(".bottom-nav button").forEach(elemento => elemento.classList.remove("active"));
    document.getElementById(idVista).classList.add("active-view");
    document.getElementById(idNav).classList.add("active");

    guardarSesion("vistaActual", idVista);
    guardarSesion("navActual", idNav);
    if (desplazar) window.scrollTo({ top: 0, behavior: "smooth" });

    if (idVista === "vistaExplorar") {
        setTimeout(() => {
            inicializarMapa();
            mapaParkSmart?.invalidateSize();
            actualizarMarcadoresMapa(parkSmartState.espacios);
        }, 120);
    }
}

function irABusqueda() {
    cambiarVista("vistaExplorar", "navExplorar");
    setTimeout(() => document.getElementById("buscarEspacio").focus(), 280);
}

function abrirReserva(idEspacio) {
    const espacio = obtenerEspacio(idEspacio);
    if (!espacio) {
        mostrarToast("Ese espacio ya no está disponible.");
        return;
    }

    const sector = obtenerSector(espacio.idSector);
    document.getElementById("reservaEspacioId").value = espacio.idEspacio;
    document.getElementById("selectedSpaceSummary").innerHTML = `
        <div class="space-thumbnail ${claseTipo(espacio.tipoEspacio)}">${escaparHtml(espacio.codigoEspacio)}</div>
        <div><h3>${escaparHtml(sector?.nombreSector || "ParkSmart")}</h3><p>${formatearTipo(espacio.tipoEspacio)} · ${escaparHtml(espacio.descripcion || "Disponible")}</p></div>
        <strong>Disponible</strong>
    `;

    const selector = document.getElementById("reservaVehiculo");
    selector.innerHTML = parkSmartState.vehiculos.map(vehiculo => `
        <option value="${Number(vehiculo.idVehiculo)}">${escaparHtml(vehiculo.placa)} · ${escaparHtml([vehiculo.marca, vehiculo.modelo].filter(Boolean).join(" "))}</option>
    `).join("");

    const inicio = redondearProximaMediaHora(new Date());
    const fin = new Date(inicio.getTime() + 60 * 60 * 1000);
    document.getElementById("reservaInicio").value = fechaParaInput(inicio);
    document.getElementById("reservaFin").value = fechaParaInput(fin);
    document.getElementById("reservaInicio").min = fechaParaInput(new Date());
    document.getElementById("reservaFin").min = fechaParaInput(inicio);
    document.getElementById("confirmarReservaButton").disabled = parkSmartState.vehiculos.length === 0;
    actualizarTotalReserva();
    abrirDialogo("reservaDialog");
}

async function confirmarReserva(evento) {
    evento.preventDefault();
    const boton = document.getElementById("confirmarReservaButton");
    const idEspacio = Number(document.getElementById("reservaEspacioId").value);
    const inicio = document.getElementById("reservaInicio").value;
    const fin = document.getElementById("reservaFin").value;
    const idVehiculo = Number(document.getElementById("reservaVehiculo").value);

    if (new Date(fin) <= new Date(inicio)) {
        mostrarToast("La hora de salida debe ser posterior a la entrada.");
        return;
    }

    boton.disabled = true;
    boton.querySelector("span").textContent = "Creando reserva...";

    try {
        let reserva;
        let qr;

        if (parkSmartState.demo) {
            reserva = {
                idReserva: Date.now(),
                idCliente: CLIENTE_ACTUAL_ID,
                idVehiculo,
                idEspacio,
                codigoReserva: `RES-DEMO-${String(Date.now()).slice(-6)}`,
                fechaInicioReserva: new Date(inicio).toISOString(),
                fechaFinReserva: new Date(fin).toISOString(),
                estado: "CONFIRMADA",
                observaciones: "Reserva creada en modo demostración"
            };
            qr = crearQrDemo(reserva);
        } else {
// La API ahora unificó la transacción. Nos devuelve la reserva y el QR juntos.
            const respuestaUnificada = await apiPost("/reservas/", {
                idCliente: CLIENTE_ACTUAL_ID, // Recuerda cambiar esto para que use el ID del token
                idVehiculo,
                idEspacio,
                fechaInicioReserva: `${inicio}:00`,
                fechaFinReserva: `${fin}:00`,
                observaciones: "Reserva unificada"
            });
            
            reserva = respuestaUnificada.reserva;
            qr = respuestaUnificada.qr;
        }

        const espacioSeleccionado = obtenerEspacio(idEspacio);
        parkSmartState.reservas.unshift(reserva);
        parkSmartState.qrs.set(reserva.idReserva, qr);
        parkSmartState.espacios = parkSmartState.espacios.filter(espacio => espacio.idEspacio !== idEspacio);
        if (espacioSeleccionado) espacioSeleccionado.estado = "RESERVADO";
        cerrarDialogo("reservaDialog");
        renderAplicacion();
        mostrarQr(qr, reserva);
    } catch (error) {
        mostrarToast(`No se pudo reservar: ${limpiarMensajeError(error.message)}`);
    } finally {
        boton.disabled = parkSmartState.vehiculos.length === 0;
        boton.querySelector("span").textContent = "Reservar y generar QR";
    }
}

async function mostrarQrReserva(idReserva) {
    const reserva = parkSmartState.reservas.find(item => item.idReserva === idReserva);
    if (!reserva) return;

    try {
        let qr = parkSmartState.qrs.get(idReserva);

        if (!qr && parkSmartState.demo) {
            qr = crearQrDemo(reserva);
        } else if (!qr) {
            const existentes = await apiGet(`/qrs/reserva/${idReserva}`);
            qr = existentes.find(item => !["ANULADO", "VENCIDO"].includes(item.estado));
            if (!qr) qr = await apiPost("/qrs/", { idReserva });
        }

        parkSmartState.qrs.set(idReserva, qr);
        mostrarQr(qr, reserva);
    } catch (error) {
        mostrarToast(`No se pudo obtener el QR: ${limpiarMensajeError(error.message)}`);
    }
}

function mostrarQr(qr, reserva) {
    const espacio = obtenerEspacio(reserva.idEspacio);
    const canvas = document.getElementById("qrCanvas");
    canvas.innerHTML = "";

    if (typeof QRCode !== "undefined") {
        new QRCode(canvas, {
            text: qr.codigoQr,
            width: 164,
            height: 164,
            colorDark: "#07111f",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H
        });
    } else {
        canvas.innerHTML = `<div class="qr-fallback">${escaparHtml(qr.codigoQr)}</div>`;
    }

    asignarTexto("qrCodeLabel", qr.codigoQr);
    asignarTexto("qrTitle", espacio ? `Espacio ${espacio.codigoEspacio} listo` : "Tu espacio está listo");
    document.getElementById("qrReservationMeta").innerHTML = `
        <span><small>Entrada</small><strong>${formatearFechaCorta(reserva.fechaInicioReserva)} · ${formatearHora(reserva.fechaInicioReserva)}</strong></span>
        <span><small>Válido hasta</small><strong>${formatearHora(reserva.fechaFinReserva)}</strong></span>
    `;
    abrirDialogo("qrDialog");
}

function crearQrDemo(reserva) {
    return {
        idQr: Date.now(),
        idReserva: reserva.idReserva,
        codigoQr: `QR-DEMO-${String(reserva.idReserva).slice(-6)}`,
        tokenQr: `demo-${reserva.idReserva}`,
        fechaValidezInicio: reserva.fechaInicioReserva,
        fechaValidezFin: reserva.fechaFinReserva,
        estado: "GENERADO"
    };
}

async function cancelarReserva(idReserva) {
    const reserva = parkSmartState.reservas.find(item => item.idReserva === idReserva);
    if (!reserva) return;

    if (!window.confirm("¿Querés cancelar esta reserva?")) return;

    try {
        const actualizada = parkSmartState.demo
            ? { ...reserva, estado: "CANCELADA" }
            : await apiPut(`/reservas/${idReserva}/cancelar`);

        Object.assign(reserva, actualizada);
        const espacio = obtenerEspacio(reserva.idEspacio);
        if (espacio && !parkSmartState.espacios.some(item => item.idEspacio === espacio.idEspacio)) {
            espacio.estado = "DISPONIBLE";
            parkSmartState.espacios.push(espacio);
        }
        renderAplicacion();
        mostrarToast("Reserva cancelada correctamente.");
    } catch (error) {
        mostrarToast(`No se pudo cancelar: ${limpiarMensajeError(error.message)}`);
    }
}

function actualizarTotalReserva() {
    const inicio = new Date(document.getElementById("reservaInicio").value);
    const fin = new Date(document.getElementById("reservaFin").value);
    const horas = Math.max(1, Math.ceil((fin - inicio) / 3600000));
    asignarTexto("reservaTotal", formatearMoneda(horas * TARIFA_REFERENCIA));
}

function ordenarEspacios() {
    parkSmartState.ordenAscendente = !parkSmartState.ordenAscendente;
    renderEspacios();
    mostrarToast(parkSmartState.ordenAscendente ? "Orden A–Z" : "Orden Z–A");
}

function alternarMapaLista() {
    const tarjeta = document.querySelector(".map-card");
    const colapsado = tarjeta.classList.toggle("collapsed");
    asignarTexto("mapToggleButton", colapsado ? "Mostrar mapa" : "Ocultar mapa");
    if (!colapsado) setTimeout(() => mapaParkSmart?.invalidateSize(), 220);
}

function abrirNotificaciones() {
    renderNotificaciones();
    abrirDialogo("notificationsDialog");
}

function abrirSoporte() {
    abrirDialogo("supportDialog");
}

function enviarSoporte(evento) {
    evento.preventDefault();
    const reporte = {
        asunto: document.getElementById("soporteAsunto").value,
        mensaje: document.getElementById("soporteMensaje").value,
        fecha: new Date().toISOString()
    };
    guardarSesion("ultimoReporteSoporte", JSON.stringify(reporte));
    evento.target.reset();
    cerrarDialogo("supportDialog");
    mostrarToast("Solicitud guardada en este dispositivo.");
}

function abrirDialogo(id) {
    const dialogo = document.getElementById(id);
    if (!dialogo.open) dialogo.showModal();
}

function cerrarDialogo(id) {
    const dialogo = document.getElementById(id);
    if (dialogo?.open) dialogo.close();
}

function establecerEstadoApi(estado) {
    const conectado = estado === "online";
    const cargando = estado === "loading";
    document.getElementById("connectionDot").classList.toggle("online", conectado);
    document.getElementById("apiEstadoIcon").classList.toggle("online", conectado);
    asignarTexto("apiEstado", cargando ? "Verificando API" : conectado ? "API conectada" : "Modo demostración");
    asignarTexto("apiMensaje", cargando ? "Conectando con ParkSmart..." : conectado ? "Datos sincronizados con Docker" : "Docker no está respondiendo");
}

function alternarTema() {
    const ordenTemas = [
        "claro",
        "oscuro",
        "pastel",
        "primavera"
    ];

    const temaActual =
        obtenerPreferencia("tema", "claro");

    const indiceActual =
        ordenTemas.indexOf(temaActual);

    const siguienteIndice =
        indiceActual === -1
            ? 0
            : (indiceActual + 1) % ordenTemas.length;

    const nuevoTema =
        ordenTemas[siguienteIndice];

    guardarPreferencia(
        "tema",
        nuevoTema
    );

    guardarCookie(
        "temaParkSmart",
        nuevoTema,
        30
    );

    aplicarTema(nuevoTema);

    const nombreTema =
        TEMAS_PARKSMART[nuevoTema].etiqueta;

    mostrarToast(
        `Apariencia aplicada: ${nombreTema}`
    );
}

function mostrarToast(mensaje) {
    const toast = document.getElementById("toast");
    toast.textContent = mensaje;
    toast.classList.add("show");
    clearTimeout(window.parkSmartToastTimer);
    window.parkSmartToastTimer = setTimeout(() => toast.classList.remove("show"), 3000);
}

function obtenerSector(idSector) {
    return parkSmartState.sectores.find(sector => Number(sector.idSector) === Number(idSector));
}

function obtenerEspacio(idEspacio) {
    return parkSmartState.catalogoEspacios.find(espacio => Number(espacio.idEspacio) === Number(idEspacio))
        || parkSmartState.espacios.find(espacio => Number(espacio.idEspacio) === Number(idEspacio));
}

function obtenerVehiculo(idVehiculo) {
    return parkSmartState.vehiculos.find(vehiculo => Number(vehiculo.idVehiculo) === Number(idVehiculo));
}

function formatearTipo(tipo = "REGULAR") {
    const tipos = { REGULAR: "Automóvil", AUTOMOVIL: "Automóvil", MOTOCICLETA: "Moto", DISCAPACIDAD: "Accesible", ELECTRICO: "Eléctrico", VIP: "VIP" };
    return tipos[tipo] || formatearEstado(tipo);
}

function claseTipo(tipo) {
    return { MOTOCICLETA: "motorcycle", ELECTRICO: "electric", VIP: "vip" }[tipo] || "";
}

function formatearEstado(estado = "") {
    return estado.toString().toLowerCase().replaceAll("_", " ").replace(/^./, letra => letra.toUpperCase());
}

function formatearFechaCorta(fecha) {
    if (!fecha) return "Sin fecha";
    return new Intl.DateTimeFormat("es-CR", { day: "numeric", month: "short" }).format(new Date(fecha));
}

function formatearHora(fecha) {
    if (!fecha) return "--:--";
    return new Intl.DateTimeFormat("es-CR", { hour: "numeric", minute: "2-digit" }).format(new Date(fecha));
}

function formatearMoneda(valor) {
    return new Intl.NumberFormat("es-CR", { style: "currency", currency: "CRC", maximumFractionDigits: 0 }).format(Number(valor || 0));
}

function tiempoRelativo(fecha) {
    if (!fecha) return "Ahora";
    const diferencia = Date.now() - new Date(fecha).getTime();
    const minutos = Math.max(0, Math.round(diferencia / 60000));
    if (minutos < 2) return "Ahora";
    if (minutos < 60) return `Hace ${minutos} min`;
    const horas = Math.round(minutos / 60);
    if (horas < 24) return `Hace ${horas} h`;
    return `Hace ${Math.round(horas / 24)} días`;
}

function redondearProximaMediaHora(fecha) {
    const resultado = new Date(fecha);
    resultado.setSeconds(0, 0);
    resultado.setMinutes(resultado.getMinutes() < 30 ? 30 : 60);
    return resultado;
}

function fechaParaInput(fecha) {
    const local = new Date(fecha.getTime() - fecha.getTimezoneOffset() * 60000);
    return local.toISOString().slice(0, 16);
}

function obtenerIniciales(nombre) {
    return nombre.split(/\s+/).filter(Boolean).slice(0, 2).map(parte => parte[0]).join("").toUpperCase() || "PS";
}

function iconoNotificacion(tipo = "") {
    if (tipo.includes("PAGO")) return "₡";
    if (tipo.includes("RESERVA")) return "P";
    return "!";
}

function estadoVacio(icono, titulo, mensaje) {
    return `<div class="empty-state"><span>${escaparHtml(icono)}</span><strong>${escaparHtml(titulo)}</strong><small>${escaparHtml(mensaje)}</small></div>`;
}

function asignarTexto(id, texto) {
    const elemento = document.getElementById(id);
    if (elemento) elemento.textContent = texto;
}

function escaparHtml(valor) {
    return String(valor ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function limpiarMensajeError(mensaje) {
    return String(mensaje || "Error desconocido").replace(/^\[|\]$/g, "").slice(0, 150);
}

// ==========================================
// NUEVA FUNCIÓN PARA EL OPERADOR DE PARQUEO
// ==========================================
async function validarQR(evento) {
    evento.preventDefault();
    const btnSubmit = evento.target.querySelector('button');
    const mensajeEl = document.getElementById('resultadoOperador');
    const codigoQRInput = document.getElementById('operadorCodigoQR').value.trim();

    if(!codigoQRInput){
        return;
    }

    btnSubmit.disabled = true;
    btnSubmit.textContent = "Validando acceso...";
    mensajeEl.classList.add('hidden');
    mensajeEl.classList.remove('success', 'error');

    try {
        // Enviar la petición al nuevo endpoint de uso de QR
        // Nota: Asegúrate de que este endpoint exista en tu backend (ej. POST /qrs/validar-ingreso)
        const resultado = await fetchAPI('/qrs/validar-ingreso', {
            method: 'POST',
            body: JSON.stringify({ codigoQr: codigoQRInput })
        });

        // Mostrar éxito
        mensajeEl.textContent = `¡Acceso concedido! Vehículo ingresado al espacio ${resultado.espacio || 'asignado'}.`;
        mensajeEl.classList.add('success');
        mensajeEl.classList.remove('hidden');
        
        // Limpiar el campo
        document.getElementById('operadorCodigoQR').value = "";

    } catch (error) {
        // Mostrar error (QR inválido, vencido, o ya usado)
        mensajeEl.textContent = `Acceso denegado: ${limpiarMensajeError(error.message)}`;
        mensajeEl.classList.add('error');
        mensajeEl.classList.remove('hidden');
    } finally {
        btnSubmit.disabled = false;
        btnSubmit.textContent = "Validar e Ingresar Vehículo";
    }
}

function cambiarCuenta() {
    // 1. Limpiamos absolutamente todos los datos de sesión y credenciales
    localStorage.removeItem('parksmart_token');
    localStorage.removeItem('parksmart_user');
    localStorage.removeItem('parksmart_cliente_id');

    // 2. Ocultamos toda la interfaz principal de la aplicación (el cascarón)
    document.getElementById('appShell').classList.add('hidden');

    // 3. Mostramos nuevamente la pantalla de inicio de sesión
    document.getElementById('authScreen').classList.remove('hidden');

    // 4. Limpiamos el formulario para que no quede el usuario viejo escrito
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.reset();
    }

    // 5. Mostramos una alerta visual al usuario (aprovechando tu función mostrarToast)
    if (typeof mostrarToast === 'function') {
        mostrarToast("Has cerrado sesión exitosamente.");
    }
}
