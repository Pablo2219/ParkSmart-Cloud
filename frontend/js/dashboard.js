async function cargarDashboard() {
    activarBoton("btnDashboard");

    const titulo = document.getElementById("tituloSeccion");
    const descripcion = document.getElementById("descripcionSeccion");
    const contenedor = document.getElementById("contenedor");

    titulo.textContent = "Dashboard";
    descripcion.textContent = "Resumen general del sistema ParkSmart.";

    contenedor.innerHTML = `<p>Cargando resumen...</p>`;

    try {
        const clientes = await obtenerDatos("/clientes/");
        const vehiculos = await obtenerDatos("/vehiculos/");
        const reservas = await obtenerDatos("/reservas/");
        const pagos = await obtenerDatos("/pagos/");
        const notificaciones = await obtenerDatos("/notificaciones/");

        contenedor.innerHTML = `
            <div class="grid">
                <div class="metric-card">
                    <span>Clientes</span>
                    <h3>${clientes.length}</h3>
                </div>

                <div class="metric-card">
                    <span>Vehículos</span>
                    <h3>${vehiculos.length}</h3>
                </div>

                <div class="metric-card">
                    <span>Reservas</span>
                    <h3>${reservas.length}</h3>
                </div>

                <div class="metric-card">
                    <span>Pagos</span>
                    <h3>${pagos.length}</h3>
                </div>
            </div>

            <div class="card">
                <h3>Estado del sistema</h3>
                <p>La API de ParkSmart está conectada correctamente y los módulos principales responden desde Docker.</p>
            </div>

            <div class="card">
                <h3>Últimas notificaciones</h3>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Tipo</th>
                                <th>Canal</th>
                                <th>Título</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${notificaciones.slice(0, 5).map(n => `
                                <tr>
                                    <td>${n.idNotificacion}</td>
                                    <td>${n.tipoNotificacion}</td>
                                    <td>${n.canal}</td>
                                    <td>${n.titulo}</td>
                                    <td>${badge(n.estado)}</td>
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

    } catch (error) {
        mostrarError(contenedor, "No se pudo cargar el dashboard.");
    }
}