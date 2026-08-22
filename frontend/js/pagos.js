async function cargarPagos() {
    activarBoton("btnPagos");

    const titulo = document.getElementById("tituloSeccion");
    const descripcion = document.getElementById("descripcionSeccion");
    const contenedor = document.getElementById("contenedor");

    titulo.textContent = "Pagos";
    descripcion.textContent = "Consulta y confirmación de pagos.";

    contenedor.innerHTML = `<p>Cargando pagos...</p>`;

    try {
        const pagos = await obtenerDatos("/pagos/");

        if (pagos.length === 0) {
            contenedor.innerHTML = `<div class="card empty">No hay pagos registrados.</div>`;
            return;
        }

        contenedor.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3>Listado de pagos</h3>
                </div>

                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Ocupación</th>
                                <th>Código</th>
                                <th>Monto</th>
                                <th>Método</th>
                                <th>Estado</th>
                                <th>Fecha pago</th>
                                <th>Acción</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${pagos.map(p => `
                                <tr>
                                    <td>${p.idPago}</td>
                                    <td>${p.idOcupacion}</td>
                                    <td>${p.codigoPago}</td>
                                    <td>₡${p.montoTotal}</td>
                                    <td>${p.metodoPago || "-"}</td>
                                    <td>${badge(p.estado)}</td>
                                    <td>${formatearFecha(p.fechaPago)}</td>
                                    <td>
                                        ${p.estado === "PENDIENTE" 
                                            ? `<button class="btn" onclick="confirmarPago(${p.idPago})">Confirmar</button>`
                                            : `<span>-</span>`
                                        }
                                    </td>
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                </div>
            </div>
        `;

    } catch (error) {
        mostrarError(contenedor, "No se pudieron cargar los pagos.");
    }
}

async function confirmarPago(idPago) {
    try {
        await enviarDatos(`/pagos/${idPago}/confirmar`, "PUT");
        await cargarPagos();
    } catch (error) {
        alert("No se pudo confirmar el pago.");
    }
}