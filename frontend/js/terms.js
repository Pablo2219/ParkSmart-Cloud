document.addEventListener("DOMContentLoaded", () => {
    const description = document.querySelector('[data-auth-view="login"] .auth-description');
    if (description) description.textContent = "Ingresá con tu cuenta de cliente, proveedor o administrador.";
});

function instalarAceptacionTerminos() {
    const form = document.getElementById("registerForm");
    if (!form || document.getElementById("registerTerms")) return;
    const label = document.createElement("label");
    label.className = "privacy-consent";
    label.innerHTML = '<input id="registerTerms" type="checkbox" required><span>Acepto los <a href="terminos.html" target="_blank" rel="noopener">Términos y condiciones</a> de ParkSmart, versión 1.0.</span>';
    const button = document.getElementById("registerButton");
    form.insertBefore(label, button);

    form.addEventListener("submit", async (evento) => {
        if (!document.getElementById("registerTerms")?.checked) return;
        evento.preventDefault();
        evento.stopImmediatePropagation();
        const proveedor = document.getElementById("registerRole").value === "PROVEEDOR";
        const boton = document.getElementById("registerButton");
        boton.disabled = true; boton.textContent = "Creando cuenta...";
        const datos = {
            nombreUsuario: document.getElementById("registerUsername").value.trim(),
            correoElectronico: document.getElementById("registerEmail").value.trim(),
            contrasena: document.getElementById("registerPassword").value,
            rol: proveedor ? "PROVEEDOR" : "CLIENTE",
            aceptaPrivacidad: document.getElementById("registerPrivacy")?.checked === true,
            aceptaTerminos: true,
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
        } catch (error) { mostrarMensajeAuth(error.message, "error"); }
        finally { boton.disabled = false; boton.textContent = "Crear cuenta"; }
    }, true);
}

const observerTerminos = new MutationObserver(() => instalarAceptacionTerminos());
observerTerminos.observe(document.body, { childList: true, subtree: true });
