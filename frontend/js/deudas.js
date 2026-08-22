async function cargarDeudas() {
    activarBoton("btnDeudas");

    const titulo = document.getElementById("tituloSeccion");
    const descripcion = document.getElementById("descripcionSeccion");
    const contenedor = document.getElementById("contenedor");

    titulo.textContent = "Deudas";
    descripcion.textContent = "Consulta de deudas registradas.";

    contenedor.innerHTML = `<p>Cargando deudas...</p>`;

    try {
        const deudas = await obtenerDatos("/deudas/");

        if (deudas.length === 0) {
            contenedor.innerHTML = `<div class="card empty">No hay deudas registradas.</div>`;
            return;
        }

        const columnas = Object.keys(deudas[0]);

        contenedor.innerHTML = `
            <div class="card">
                <h3>Listado de deudas</h3>

                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                ${columnas.map(columna => `<th>${columna}</th>`).join("")}
                            </tr>
                        </thead>
                        <tbody>
                            ${deudas.map(deuda => `
                                <tr>
                                    ${columnas.map(columna => `
                                        <td>${deuda[columna] ?? "-"}</td>
                                    `).join("")}
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

    } catch (error) {
        mostrarError(contenedor, "No se pudieron cargar las deudas.");
    }
}