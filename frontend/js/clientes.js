async function cargarClientes() {
    activarBoton("btnClientes");

    const titulo = document.getElementById("tituloSeccion");
    const descripcion = document.getElementById("descripcionSeccion");
    const contenedor = document.getElementById("contenedor");

    titulo.textContent = "Clientes";
    descripcion.textContent = "Consulta de clientes registrados en ParkSmart.";

    contenedor.innerHTML = `<p>Cargando clientes...</p>`;

    try {
        const clientes = await obtenerDatos("/clientes/");

        if (clientes.length === 0) {
            contenedor.innerHTML = `<div class="card empty">No hay clientes registrados.</div>`;
            return;
        }

        contenedor.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3>Listado de clientes</h3>
                    <button class="btn">Nuevo cliente</button>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Identificación</th>
                                <th>Nombre</th>
                                <th>Apellido</th>
                                <th>Teléfono</th>
                                <th>Correo</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${clientes.map(cliente => `
                                <tr>
                                    <td>${cliente.idCliente}</td>
                                    <td>${cliente.identificacion}</td>
                                    <td>${cliente.nombre}</td>
                                    <td>${cliente.primerApellido}</td>
                                    <td>${cliente.telefono}</td>
                                    <td>${cliente.correoElectronico}</td>
                                    <td>${badge(cliente.estado)}</td>
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

    } catch (error) {
        mostrarError(contenedor, "No se pudieron cargar los clientes.");
    }
}