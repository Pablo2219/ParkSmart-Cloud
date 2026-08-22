async function cargarVehiculos() {
    activarBoton("btnVehiculos");

    const titulo = document.getElementById("tituloSeccion");
    const descripcion = document.getElementById("descripcionSeccion");
    const contenedor = document.getElementById("contenedor");

    titulo.textContent = "Vehículos";
    descripcion.textContent = "Vehículos asociados a clientes registrados.";

    contenedor.innerHTML = `<p>Cargando vehículos...</p>`;

    try {
        const vehiculos = await obtenerDatos("/vehiculos/");

        if (vehiculos.length === 0) {
            contenedor.innerHTML = `<div class="card empty">No hay vehículos registrados.</div>`;
            return;
        }

        contenedor.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3>Listado de vehículos</h3>
                    <button class="btn">Nuevo vehículo</button>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Cliente</th>
                                <th>Placa</th>
                                <th>Marca</th>
                                <th>Modelo</th>
                                <th>Color</th>
                                <th>Tipo</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${vehiculos.map(v => `
                                <tr>
                                    <td>${v.idVehiculo}</td>
                                    <td>${v.idCliente}</td>
                                    <td>${v.placa}</td>
                                    <td>${v.marca}</td>
                                    <td>${v.modelo}</td>
                                    <td>${v.color}</td>
                                    <td>${v.tipoVehiculo}</td>
                                    <td>${badge(v.estado)}</td>
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

    } catch (error) {
        mostrarError(contenedor, "No se pudieron cargar los vehículos.");
    }
}