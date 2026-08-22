const AUTH_TOKEN_KEY = "parksmart_access_token";
const AUTH_USER_KEY = "parksmart_auth_user";
const AUTH_DEMO_KEY = "parksmart_demo_session";

window.parkSmartSession = {
    usuario: null,
    demo: false
};

function obtenerTokenAcceso() {
    return localStorage.getItem(AUTH_TOKEN_KEY) || "";
}

function obtenerUsuarioGuardado() {
    try {
        return JSON.parse(localStorage.getItem(AUTH_USER_KEY) || "null");
    } catch {
        return null;
    }
}

async function inicializarAutenticacion() {
    configurarEventosAutenticacion();

    const tokenReset = new URLSearchParams(window.location.search).get("reset_token");
    if (tokenReset) {
        mostrarPantallaAuth("reset");
        document.getElementById("resetToken").value = tokenReset;
        return false;
    }

    if (localStorage.getItem(AUTH_DEMO_KEY) === "true") {
        const usuario = obtenerUsuarioGuardado() || crearUsuarioDemo("CLIENTE");
        activarSesionVisual(usuario, true);
        return true;
    }

    const token = obtenerTokenAcceso();
    if (!token) {
        mostrarPantallaAuth("login");
        return false;
    }

    try {
        const usuario = await apiGet("/auth/me");
        guardarSesionAutenticada(token, usuario);
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

    document.getElementById("loginForm").addEventListener("submit", iniciarSesion);
    document.getElementById("recoveryForm").addEventListener("submit", solicitarRestablecimiento);
    document.getElementById("resetForm").addEventListener("submit", restablecerContrasena);
    document.getElementById("changePasswordForm").addEventListener("submit", cambiarContrasena);
    document.getElementById("adminUserForm").addEventListener("submit", crearUsuarioDesdeAdmin);
    document.getElementById("adminNotificationForm").addEventListener("submit", enviarNotificacionDesdeAdmin);
}

function mostrarPantallaAuth(vista = "login") {
    document.getElementById("authScreen").classList.remove("hidden");
    document.getElementById("appShell").classList.add("hidden");
    document.querySelectorAll("[data-auth-view]").forEach(panel => {
        panel.classList.toggle("hidden", panel.dataset.authView !== vista);
    });
    document.getElementById("authMessage").className = "auth-message hidden";
}

function mostrarVistaAuth(vista) {
    mostrarPantallaAuth(vista);
}

function activarSesionVisual(usuario, demo = false) {
    window.parkSmartSession.usuario = usuario;
    window.parkSmartSession.demo = demo;
    document.getElementById("authScreen").classList.add("hidden");
    document.getElementById("appShell").classList.remove("hidden");
    document.body.classList.toggle("admin-session", usuario.rol === "ADMINISTRADOR");
    const roleChip = document.getElementById("profileRole");
    if (roleChip) roleChip.textContent = usuario.rol === "ADMINISTRADOR" ? "Administrador" : "Cliente";
    document.getElementById("adminToolsButton")?.classList.toggle("hidden", usuario.rol !== "ADMINISTRADOR");
}

async function iniciarSesion(evento) {
    evento.preventDefault();
    const boton = document.getElementById("loginButton");
    boton.disabled = true;
    boton.textContent = "Verificando...";
    try {
        const respuesta = await apiPost("/auth/login", {
            usuario: document.getElementById("loginUser").value.trim(),
            contrasena: document.getElementById("loginPassword").value
        });
        guardarSesionAutenticada(respuesta.accessToken, respuesta.usuario);
        localStorage.removeItem(AUTH_DEMO_KEY);
        window.location.reload();
    } catch (error) {
        mostrarMensajeAuth(limpiarMensajeError(error.message), "error");
    } finally {
        boton.disabled = false;
        boton.textContent = "Iniciar sesión";
    }
}

function entrarModoDemo() {
    const rol = document.getElementById("demoRole").value;
    const usuario = crearUsuarioDemo(rol);
    localStorage.setItem(AUTH_DEMO_KEY, "true");
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(usuario));
    localStorage.setItem("parksmart_cliente_id", "1");
    window.location.reload();
}

function crearUsuarioDemo(rol) {
    return rol === "ADMINISTRADOR"
        ? { idUsuario: 0, idCliente: 1, nombreUsuario: "admin-demo", correoElectronico: "admin@parksmart.demo", rol: "ADMINISTRADOR", estado: "ACTIVO" }
        : { idUsuario: 0, idCliente: 1, nombreUsuario: "cliente-demo", correoElectronico: "cliente@parksmart.demo", rol: "CLIENTE", estado: "ACTIVO" };
}

function guardarSesionAutenticada(token, usuario) {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(usuario));
    if (usuario.idCliente) localStorage.setItem("parksmart_cliente_id", String(usuario.idCliente));
    window.parkSmartSession.usuario = usuario;
}

function limpiarSesionAutenticada() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(AUTH_USER_KEY);
    localStorage.removeItem(AUTH_DEMO_KEY);
}

async function cerrarSesion() {
    try {
        if (obtenerTokenAcceso()) await apiPost("/auth/logout", {});
    } catch {
        // El cierre de sesión es local aunque la API no responda.
    }
    limpiarSesionAutenticada();
    sessionStorage.clear();
    window.location.reload();
}

function cambiarCuenta() {
    cerrarSesion();
}

async function solicitarRestablecimiento(evento) {
    evento.preventDefault();
    const boton = document.getElementById("recoveryButton");
    boton.disabled = true;
    boton.textContent = "Enviando...";
    try {
        const respuesta = await apiPost("/auth/solicitar-restablecimiento", {
            usuarioOCorreo: document.getElementById("recoveryIdentity").value.trim(),
            canal: document.getElementById("recoveryChannel").value
        });
        mostrarMensajeAuth(respuesta.mensaje, "success");
        if (respuesta.tokenRestablecimiento) {
            document.getElementById("resetToken").value = respuesta.tokenRestablecimiento;
            mostrarVistaAuth("reset");
            mostrarMensajeAuth("Modo académico: el código se cargó automáticamente.", "success");
        }
    } catch (error) {
        mostrarMensajeAuth(limpiarMensajeError(error.message), "error");
    } finally {
        boton.disabled = false;
        boton.textContent = "Enviar instrucciones";
    }
}

async function restablecerContrasena(evento) {
    evento.preventDefault();
    const nueva = document.getElementById("resetPassword").value;
    const confirmar = document.getElementById("resetPasswordConfirm").value;
    if (nueva !== confirmar) {
        mostrarMensajeAuth("Las contraseñas no coinciden.", "error");
        return;
    }
    try {
        const respuesta = await apiPost("/auth/restablecer-contrasena", {
            token: document.getElementById("resetToken").value.trim(),
            nuevaContrasena: nueva
        });
        window.history.replaceState({}, "", window.location.pathname);
        mostrarVistaAuth("login");
        mostrarMensajeAuth(respuesta.mensaje, "success");
    } catch (error) {
        mostrarMensajeAuth(limpiarMensajeError(error.message), "error");
    }
}

function mostrarMensajeAuth(mensaje, tipo = "success") {
    const elemento = document.getElementById("authMessage");
    elemento.textContent = mensaje;
    elemento.className = `auth-message ${tipo}`;
}

function abrirCambioContrasena() {
    document.getElementById("changePasswordForm").reset();
    abrirDialogo("changePasswordDialog");
}

async function cambiarContrasena(evento) {
    evento.preventDefault();
    const nueva = document.getElementById("newPassword").value;
    const confirmacion = document.getElementById("confirmNewPassword").value;
    if (nueva !== confirmacion) {
        mostrarToast("Las contraseñas nuevas no coinciden.");
        return;
    }
    try {
        const respuesta = await apiPut("/auth/cambiar-contrasena", {
            contrasenaActual: document.getElementById("currentPassword").value,
            nuevaContrasena: nueva
        });
        cerrarDialogo("changePasswordDialog");
        mostrarToast(respuesta.mensaje);
    } catch (error) {
        mostrarToast(limpiarMensajeError(error.message));
    }
}

async function abrirAdministracion() {
    if (window.parkSmartSession.usuario?.rol !== "ADMINISTRADOR") return;
    abrirDialogo("adminDialog");
    await cargarUsuariosAdmin();
}

async function cargarUsuariosAdmin() {
    const contenedor = document.getElementById("adminUsersList");
    contenedor.innerHTML = '<div class="admin-loading">Cargando usuarios...</div>';
    try {
        const usuarios = window.parkSmartSession.demo
            ? [crearUsuarioDemo("ADMINISTRADOR"), crearUsuarioDemo("CLIENTE")]
            : await apiGet("/usuarios/");
        contenedor.innerHTML = usuarios.map(usuario => `
            <article class="admin-user-row">
                <span class="admin-user-avatar">${obtenerIniciales(usuario.nombreUsuario)}</span>
                <div><strong>${escaparHtml(usuario.nombreUsuario)}</strong><small>${escaparHtml(usuario.correoElectronico)}</small></div>
                <span class="role-pill ${usuario.rol === "ADMINISTRADOR" ? "admin" : "client"}">${formatearEstado(usuario.rol)}</span>
            </article>
        `).join("");
    } catch (error) {
        contenedor.innerHTML = estadoVacio("!", "No se pudieron cargar", limpiarMensajeError(error.message));
    }
}

async function crearUsuarioDesdeAdmin(evento) {
    evento.preventDefault();
    if (window.parkSmartSession.demo) {
        mostrarToast("En modo demo no se modifica la base de datos.");
        return;
    }
    const rol = document.getElementById("adminUserRole").value;
    const idClienteTexto = document.getElementById("adminUserClientId").value.trim();
    try {
        await apiPost("/usuarios/", {
            nombreUsuario: document.getElementById("adminUsername").value.trim(),
            correoElectronico: document.getElementById("adminUserEmail").value.trim(),
            contrasena: document.getElementById("adminUserPassword").value,
            rol,
            idCliente: idClienteTexto ? Number(idClienteTexto) : null
        });
        evento.target.reset();
        mostrarToast("Usuario creado correctamente.");
        await cargarUsuariosAdmin();
    } catch (error) {
        mostrarToast(limpiarMensajeError(error.message));
    }
}

async function enviarNotificacionDesdeAdmin(evento) {
    evento.preventDefault();
    if (window.parkSmartSession.demo) {
        mostrarToast("Notificación simulada correctamente.");
        evento.target.reset();
        return;
    }
    const destinatario = document.getElementById("adminNotificationRecipient").value.trim();
    try {
        const notificacion = await apiPost("/notificaciones/", {
            idCliente: Number(document.getElementById("adminNotificationClientId").value),
            tipoNotificacion: "SISTEMA",
            canal: document.getElementById("adminNotificationChannel").value,
            titulo: document.getElementById("adminNotificationTitle").value.trim(),
            mensaje: document.getElementById("adminNotificationMessage").value.trim(),
            destinatario: destinatario || null,
            enviarAhora: true
        });
        mostrarToast(`Notificación ${formatearEstado(notificacion.estado)} por ${notificacion.canal}.`);
        evento.target.reset();
    } catch (error) {
        mostrarToast(limpiarMensajeError(error.message));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const user = document.getElementById('loginUser').value;
            const pass = document.getElementById('loginPassword').value;
            const messageEl = document.getElementById('authMessage');
            
            try {
                // Obligatorio para FastAPI OAuth2
                const formData = new FormData();
                formData.append('username', user);
                formData.append('password', pass);

                // Llamar a la ruta segura
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) throw new Error("Credenciales inválidas");

                const data = await response.json();
                
                // Guardar el token
                localStorage.setItem('parksmart_token', data.access_token);
                
                // Cargar datos del usuario real (Elimina el CLIENTE_ACTUAL_ID = 1 fijo)
                await cargarUsuarioActual();
                
                // Transición gráfica: Ocultar auth y mostrar app
                document.getElementById('authScreen').classList.add('hidden');
                document.getElementById('appShell').classList.remove('hidden');

            } catch (error) {
                messageEl.textContent = error.message;
                messageEl.classList.remove('hidden');
            }
        });
    }
    
    // Verificar si ya tenemos sesión iniciada al recargar la página
    verificarSesion();
});

async function verificarSesion() {
    if (localStorage.getItem('parksmart_token')) {
        try {
            await cargarUsuarioActual();
            document.getElementById('authScreen').classList.add('hidden');
            document.getElementById('appShell').classList.remove('hidden');
        } catch (error) {
            document.getElementById('authScreen').classList.remove('hidden');
        }
    } else {
        document.getElementById('authScreen').classList.remove('hidden');
    }
}

async function cargarUsuarioActual() {
    const userData = await fetchAPI('/auth/me');
    localStorage.setItem('parksmart_user', JSON.stringify(userData));
    
    // Actualizar la interfaz
    const nombreEl = document.getElementById('nombreUsuario');
    const profileNombreEl = document.getElementById('profileNombre');
    const profileRoleEl = document.getElementById('profileRole');
    
    if (nombreEl) nombreEl.textContent = userData.nombreUsuario;
    if (profileNombreEl) profileNombreEl.textContent = userData.nombreUsuario;
    if (profileRoleEl) profileRoleEl.textContent = userData.rol;
    
    // Validar visibilidad del panel de Operador/Admin
    if (userData.rol === 'ADMINISTRADOR' || userData.rol === 'OPERADOR') {
        const adminBtn = document.getElementById('adminToolsButton');
        if (adminBtn) adminBtn.classList.remove('hidden');
    }
}

function cambiarCuenta() {
    localStorage.removeItem('parksmart_token');
    localStorage.removeItem('parksmart_user');
    window.location.reload();
}
