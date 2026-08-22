async function cargarReservas() {
    activarBoton("btnReservas");

    const titulo = document.getElementById("tituloSeccion");
    const descripcion = document.getElementById("descripcionSeccion");
    const contenedor = document.getElementById("contenedor");

    titulo.textContent = "Reservas";
    descripcion.textContent = "Reservas realizadas dentro del sistema.";

    contenedor.innerHTML = `<p>Cargando reservas...</p>`;

    try {
        const reservas = await obtenerDatos("/reservas/");

        if (reservas.length === 0) {
            contenedor.innerHTML = `<div class="card empty">No hay reservas registradas.</div>`;
            return;
        }

        contenedor.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3>Listado de reservas</h3>
                    <button class="btn">Nueva reserva</button>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Código</th>
                                <th>Cliente</th>
                                <th>Vehículo</th>
                                <th>Espacio</th>
                                <th>Inicio</th>
                                <th>Fin</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${reservas.map(r => `
                                <tr>
                                    <td>${r.idReserva}</td>
                                    <td>${r.codigoReserva}</td>
                                    <td>${r.idCliente}</td>
                                    <td>${r.idVehiculo}</td>
                                    <td>${r.idEspacio}</td>
                                    <td>${formatearFecha(r.fechaInicioReserva)}</td>
                                    <td>${formatearFecha(r.fechaFinReserva)}</td>
                                    <td>${badge(r.estado)}</td>
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

    } catch (error) {
        mostrarError(contenedor, "No se pudieron cargar las reservas.");
    }
}