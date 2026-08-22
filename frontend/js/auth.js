const AUTH_TOKEN_KEY = "parksmart_access_token";
const AUTH_USER_KEY = "parksmart_auth_user";

window.parkSmartSession = { usuario: null, demo: false };

// Los proveedores usan una interfaz separada. Se intercepta antes de que app-mobile.js
// inicialice la interfaz de cliente cuando ya existe una sesión de proveedor.
document.addEventListener("DOMContentLoaded", (evento) => {
    const usuario = obtenerUsuarioGuardado();
    if (obtenerTokenAcceso() && usuario?.rol === "PROVEEDOR") {
        evento.stopImmediatePropagation();
        activarSesionVisual(usuario, false);
        cargarInterfazProveedor();
    }
}, true);

function obtenerTokenAcceso() {
    return localStorage.getItem(AUTH_TOKEN_KEY) || localStorage.getItem("parksmart_token") || "";
}

function obtenerUsuarioGuardado() {
    try {
        return JSON.parse(localStorage.getItem(AUTH_USER_KEY) || localStorage.getItem("parksmart_user") || "null");
    } catch {
        return null;
    }
}

async function inicializarAutenticacion() {
    configurarEventosAutenticacion();
    eliminarModoDemostracion();

    const tokenReset = new URLSearchParams(window.location.search).get("reset_token");
    if (tokenReset && document.getElementById("resetToken")) {
        mostrarPantallaAuth("reset");
        document.getElementById("resetToken").value = tokenReset;
        return false;
    }

    const token = obtenerTokenAcceso();
    if (!token) {
        mostrarPantallaAuth("login");
        return false;
    }

    try {
        const usuario = await fetchAPI("/auth/me");
        guardarSesionAutenticada(token, usuario);
        if (usuario.rol === "PROVEEDOR") {
            // El login de proveedor siempre termina en una recarga para activar el shell aislado.
            window.location.reload();
            return false;
        }
        activarSesionVisual(usuario, false);
        return true;
    } catch (error) {
        limpiarSesionAutenticada();
        mostrarPantallaAuth("login");
        mostrarMensajeAuth("La sesión expiró. Iniciá sesión nuevamente.", "error");
        return false;
    }
}

function configurarEventosAutenticacion() {
    if (window.authEventsConfigured) return;
    window.authEventsConfigured = true;

    document.getElementById("loginForm")?.addEventListener("submit", iniciarSesion);
    document.getElementById("recoveryForm")?.addEventListener("submit", solicitarRestablecimiento);
    document.getElementById("resetForm")?.addEventListener("submit", restablecerContrasena);
    document.getElementById("changePasswordForm")?.addEventListener("submit", cambiarContrasena);
    document.getElementById("adminUserForm")?.addEventListener("submit", crearUsuarioDesdeAdmin);
    document.getElementById("adminNotificationForm")?.addEventListener("submit", enviarNotificacionDesdeAdmin);
    prepararRegistro();
}

function eliminarModoDemostracion() {
    document.querySelector(".auth-demo-box")?.remove();
    document.querySelector(".auth-credentials")?.remove();
    localStorage.removeItem("parksmart_demo_session");
}

function prepararRegistro() {
    const loginPanel = document.querySelector('[data-auth-view="login"]');
    if (!loginPanel || document.getElementById("registerLink")) return;

    const link = document.createElement("button");
    link.id = "registerLink";
    link.type = "button";
    link.className = "auth-link";
    link.textContent = "Crear una cuenta nueva";
    link.onclick = () => mostrarVistaAuth("register");
    loginPanel.appendChild(link);

    const panel = document.createElement("div");
    panel.dataset.authView = "register";
    panel.className = "hidden";
    panel.innerHTML = `
        <button class="auth-back" type="button" onclick="mostrarVistaAuth('login')">← Volver</button>
        <span class="auth-kicker">NUEVA CUENTA</span>
        <h1>Elegí cómo usar ParkSmart.</h1>
        <p class="auth-description">Solo podés registrarte como cliente o proveedor. El rol define las funciones disponibles.</p>
        <form id="registerForm" class="auth-form">
            <label class="auth-field"><span>Tipo de cuenta</span>
                <select id="registerRole" required>
                    <option value="CLIENTE">Cliente · reservar parqueos</option>
                    <option value="PROVEEDOR">Proveedor · ofrecer parqueos</option>
                </select>
            </label>
            <label class="auth-field"><span>Usuario</span><input id="registerUsername" minlength="4" maxlength="50" autocomplete="username" required></label>
            <label class="auth-field"><span>Correo</span><input id="registerEmail" type="email" autocomplete="email" required></label>
            <label class="auth-field"><span>Contraseña</span><input id="registerPassword" type="password" minlength="8" autocomplete="new-password" required></label>
            <div id="clientRegisterFields">
                <label class="auth-field"><span>Identificación</span><input id="registerIdentification" maxlength="20" required></label>
                <label class="auth-field"><span>Nombre</span><input id="registerName" maxlength="50" required></label>
                <label class="auth-field"><span>Primer apellido</span><input id="registerLastName" maxlength="50" required></label>
            </div>
            <div id="providerRegisterFields" class="hidden">
                <label class="auth-field"><span>Identificación del proveedor</span><input id="registerProviderIdentification" maxlength="20"></label>
                <label class="auth-field"><span>Nombre comercial</span><input id="registerBusiness" maxlength="120"></label>
            </div>
            <label class="auth-field"><span>Teléfono</span><input id="registerPhone" maxlength="20" autocomplete="tel" required></label>
            <label class="auth-field"><span>Dirección (opcional)</span><input id="registerAddress" maxlength="250"></label>
            <label class="privacy-consent">
                <input id="registerPrivacy" type="checkbox" required>
                <span>Autorizo de forma expresa el tratamiento de mis datos para crear y operar mi cuenta, reservas y servicios ParkSmart. Conozco mis derechos de acceso, rectificación y supresión. <a href="https://www.pgrweb.go.cr/scij/Busqueda/Normativa/Normas/nrm_texto_completo.aspx?nValor1=1&nValor2=70975&param1=NRTC" target="_blank" rel="noopener">Ver Ley 8968</a>.</span>
            </label>
            <button id="registerButton" class="auth-primary" type="submit">Crear cuenta</button>
        </form>`;

    loginPanel.parentElement.appendChild(panel);
    document.getElementById("registerRole").addEventListener("change", alternarCamposRegistro);
    document.getElementById("registerForm").addEventListener("submit", registrarCuenta);
}

function alternarCamposRegistro() {
    const proveedor = document.getElementById("registerRole").value === "PROVEEDOR";
    document.getElementById("clientRegisterFields").classList.toggle("hidden", proveedor);
    document.getElementById("providerRegisterFields").classList.toggle("hidden", !proveedor);
    document.getElementById("registerIdentification").required = !proveedor;
    document.getElementById("registerName").required = !proveedor;
    document.getElementById("registerLastName").required = !proveedor;
    document.getElementById("registerProviderIdentification").required = proveedor;
    document.getElementById("registerBusiness").required = proveedor;
}

async function registrarCuenta(evento) {
    evento.preventDefault();
    const proveedor = document.getElementById("registerRole").value === "PROVEEDOR";
    const boton = document.getElementById("registerButton");
    boton.disabled = true;
    boton.textContent = "Creando cuenta...";

    const datos = {
        nombreUsuario: document.getElementById("registerUsername").value.trim(),
        correoElectronico: document.getElementById("registerEmail").value.trim(),
        contrasena: document.getElementById("registerPassword").value,
        rol: proveedor ? "PROVEEDOR" : "CLIENTE",
        aceptaPrivacidad: document.getElementById("registerPrivacy").checked,
        identificacion: proveedor ? document.getElementById("registerProviderIdentification").value.trim() : document.getElementById("registerIdentification").value.trim(),
        telefono: document.getElementById("registerPhone").value.trim(),
        nombre: proveedor ? null : document.getElementById("registerName").value.trim(),
        primerApellido: proveedor ? null : document.getElementById("registerLastName").value.trim(),
        nombreComercial: proveedor ? document.getElementById("registerBusiness").value.trim() : null,
        direccion: document.getElementById("registerAddress").value.trim() || null
    };

    try {
        const respuesta = await fetchAPI("/auth/register", { method: "POST", body: JSON.stringify(datos) });
        mostrarVistaAuth("login");
        document.getElementById("loginUser").value = respuesta.nombreUsuario;
        document.getElementById("loginPassword").value = datos.contrasena;
        mostrarMensajeAuth("Cuenta creada correctamente. Iniciá sesión para continuar.", "success");
    } catch (error) {
        mostrarMensajeAuth(error.message, "error");
    } finally {
        boton.disabled = false;
        boton.textContent = "Crear cuenta";
    }
}

function mostrarPantallaAuth(vista = "login") {
    document.getElementById("authScreen").classList.remove("hidden");
    document.getElementById("appShell").classList.add("hidden");
    document.querySelectorAll("[data-auth-view]").forEach(panel => panel.classList.toggle("hidden", panel.dataset.authView !== vista));
    document.getElementById("authMessage").className = "auth-message hidden";
}

function mostrarVistaAuth(vista) { mostrarPantallaAuth(vista); }

function activarSesionVisual(usuario, demo = false) {
    window.parkSmartSession.usuario = usuario;
    window.parkSmartSession.demo = false;
    document.getElementById("authScreen")?.classList.add("hidden");
    document.getElementById("appShell")?.classList.remove("hidden");
    document.body.classList.toggle("admin-session", usuario.rol === "ADMINISTRADOR");
    const roleChip = document.getElementById("profileRole");
    if (roleChip) roleChip.textContent = usuario.rol === "ADMINISTRADOR" ? "Administrador" : usuario.rol === "PROVEEDOR" ? "Proveedor" : "Cliente";
    document.getElementById("adminToolsButton")?.classList.toggle("hidden", usuario.rol !== "ADMINISTRADOR");
    const nombre = document.getElementById("nombreUsuario");
    if (nombre) nombre.textContent = usuario.nombreUsuario || "Usuario";
}

async function iniciarSesion(evento) {
    evento.preventDefault();
    const boton = document.getElementById("loginButton");
    boton.disabled = true;
    boton.textContent = "Verificando...";
    try {
        const formData = new FormData();
        formData.append("username", document.getElementById("loginUser").value.trim());
        formData.append("password", document.getElementById("loginPassword").value);
        const respuesta = await fetchAPI("/auth/login", { method: "POST", body: formData });
        guardarSesionAutenticada(respuesta.access_token, respuesta.usuario);
        window.location.reload();
    } catch (error) {
        mostrarMensajeAuth(error.message || "Credenciales inválidas", "error");
    } finally {
        boton.disabled = false;
        boton.textContent = "Iniciar sesión";
    }
}

function guardarSesionAutenticada(token, usuario) {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
    localStorage.setItem("parksmart_token", token);
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(usuario));
    localStorage.setItem("parksmart_user", JSON.stringify(usuario));
    if (usuario.idCliente) localStorage.setItem("parksmart_cliente_id", String(usuario.idCliente));
    window.parkSmartSession.usuario = usuario;
}

function limpiarSesionAutenticada() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem("parksmart_token");
    localStorage.removeItem(AUTH_USER_KEY);
    localStorage.removeItem("parksmart_user");
}

async function cerrarSesion() {
    limpiarSesionAutenticada();
    sessionStorage.clear();
    window.location.reload();
}

function cambiarCuenta() { cerrarSesion(); }

function mostrarMensajeAuth(mensaje, tipo = "success") {
    const elemento = document.getElementById("authMessage");
    if (!elemento) return;
    elemento.textContent = mensaje;
    elemento.className = `auth-message ${tipo}`;
}

async function solicitarRestablecimiento(evento) {
    evento.preventDefault();
    try {
        const respuesta = await fetchAPI("/auth/solicitar-restablecimiento", { method: "POST", body: JSON.stringify({ usuarioOCorreo: document.getElementById("recoveryIdentity").value.trim(), canal: document.getElementById("recoveryChannel").value }) });
        mostrarMensajeAuth(respuesta.mensaje, "success");
    } catch (error) { mostrarMensajeAuth(error.message, "error"); }
}

async function restablecerContrasena(evento) {
    evento.preventDefault();
    const nueva = document.getElementById("resetPassword").value;
    if (nueva !== document.getElementById("resetPasswordConfirm").value) return mostrarMensajeAuth("Las contraseñas no coinciden.", "error");
    try {
        const respuesta = await fetchAPI("/auth/restablecer-contrasena", { method: "POST", body: JSON.stringify({ token: document.getElementById("resetToken").value.trim(), nuevaContrasena: nueva }) });
        mostrarVistaAuth("login");
        mostrarMensajeAuth(respuesta.mensaje, "success");
    } catch (error) { mostrarMensajeAuth(error.message, "error"); }
}

function abrirCambioContrasena() { document.getElementById("changePasswordForm")?.reset(); abrirDialogo("changePasswordDialog"); }

async function cambiarContrasena(evento) {
    evento.preventDefault();
    const nueva = document.getElementById("newPassword").value;
    if (nueva !== document.getElementById("confirmNewPassword").value) return mostrarToast("Las contraseñas nuevas no coinciden.");
    try {
        const respuesta = await fetchAPI("/auth/cambiar-contrasena", { method: "PUT", body: JSON.stringify({ contrasenaActual: document.getElementById("currentPassword").value, nuevaContrasena: nueva }) });
        cerrarDialogo("changePasswordDialog");
        mostrarToast(respuesta.mensaje);
    } catch (error) { mostrarToast(error.message); }
}

async function abrirAdministracion() {
    if (window.parkSmartSession.usuario?.rol !== "ADMINISTRADOR") return;
    abrirDialogo("adminDialog");
    await cargarUsuariosAdmin();
}

async function cargarUsuariosAdmin() {
    const contenedor = document.getElementById("adminUsersList");
    if (!contenedor) return;
    try {
        const usuarios = await fetchAPI("/usuarios/");
        contenedor.innerHTML = usuarios.map(u => `<article class="admin-user-row"><span class="admin-user-avatar">${obtenerIniciales(u.nombreUsuario)}</span><div><strong>${escaparHtml(u.nombreUsuario)}</strong><small>${escaparHtml(u.correoElectronico)}</small></div><span class="role-pill">${formatearEstado(u.rol)}</span></article>`).join("");
    } catch (error) { contenedor.innerHTML = `<div class="admin-loading">${escaparHtml(error.message)}</div>`; }
}

async function crearUsuarioDesdeAdmin(evento) {
    evento.preventDefault();
    try {
        await fetchAPI("/usuarios/", { method: "POST", body: JSON.stringify({ nombreUsuario: document.getElementById("adminUsername").value.trim(), correoElectronico: document.getElementById("adminUserEmail").value.trim(), contrasena: document.getElementById("adminUserPassword").value, rol: document.getElementById("adminUserRole").value, idCliente: Number(document.getElementById("adminUserClientId").value) || null }) });
        evento.target.reset();
        mostrarToast("Usuario creado correctamente.");
        await cargarUsuariosAdmin();
    } catch (error) { mostrarToast(error.message); }
}

async function enviarNotificacionDesdeAdmin(evento) {
    evento.preventDefault();
    try {
        await fetchAPI("/notificaciones/", { method: "POST", body: JSON.stringify({ idCliente: Number(document.getElementById("adminNotificationClientId").value), tipoNotificacion: "SISTEMA", canal: document.getElementById("adminNotificationChannel").value, titulo: document.getElementById("adminNotificationTitle").value.trim(), mensaje: document.getElementById("adminNotificationMessage").value.trim(), destinatario: document.getElementById("adminNotificationRecipient").value.trim() || null, enviarAhora: true }) });
        evento.target.reset();
        mostrarToast("Notificación enviada.");
    } catch (error) { mostrarToast(error.message); }
}

function cargarInterfazProveedor() {
    const script = document.createElement("script");
    script.src = "js/provider.js";
    script.onload = () => window.inicializarPanelProveedor?.();
    script.onerror = () => mostrarMensajeAuth("No se pudo cargar el panel de proveedor.", "error");
    document.body.appendChild(script);
}
