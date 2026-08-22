document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("btnDashboard").addEventListener("click", cargarDashboard);
    document.getElementById("btnClientes").addEventListener("click", cargarClientes);
    document.getElementById("btnVehiculos").addEventListener("click", cargarVehiculos);
    document.getElementById("btnReservas").addEventListener("click", cargarReservas);
    document.getElementById("btnPagos").addEventListener("click", cargarPagos);
    document.getElementById("btnDeudas").addEventListener("click", cargarDeudas);
    document.getElementById("btnNotificaciones").addEventListener("click", cargarNotificaciones);

    cargarDashboard();
});