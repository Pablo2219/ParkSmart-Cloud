function guardarPreferencia(nombre, valor) {
    localStorage.setItem(nombre, valor);
}

function obtenerPreferencia(nombre, valorDefault = null) {
    return localStorage.getItem(nombre) || valorDefault;
}

function guardarSesion(nombre, valor) {
    sessionStorage.setItem(nombre, valor);
}

function obtenerSesion(nombre, valorDefault = null) {
    return sessionStorage.getItem(nombre) || valorDefault;
}

function guardarCookie(nombre, valor, dias = 7) {
    const fecha = new Date();
    fecha.setTime(fecha.getTime() + dias * 24 * 60 * 60 * 1000);

    document.cookie = `${nombre}=${valor}; expires=${fecha.toUTCString()}; path=/; SameSite=Lax`;
}

function obtenerCookie(nombre) {
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        const [clave, valor] = cookie.trim().split("=");

        if (clave === nombre) {
            return valor;
        }
    }

    return null;
}

const TEMAS_PARKSMART = {
    claro: {
        clase: null,
        etiqueta: "Tema claro",
        colorNavegador: "#f4f6fa"
    },

    oscuro: {
        clase: "dark-mode",
        etiqueta: "Tema oscuro",
        colorNavegador: "#050b14"
    },

    pastel: {
        clase: "pastel-mode",
        etiqueta: "Modo amigable pastel",
        colorNavegador: "#fff8fc"
    },

    primavera: {
        clase: "spring-mode",
        etiqueta: "Primavera cálida",
        colorNavegador: "#fffaf1"
    }
};


function aplicarTema(tema) {
    const temaSeleccionado = TEMAS_PARKSMART[tema]
        ? tema
        : "claro";

    const configuracion = TEMAS_PARKSMART[temaSeleccionado];

    const clasesTemas = [
        "dark-mode",
        "pastel-mode",
        "spring-mode"
    ];

    document.body.classList.remove(...clasesTemas);

    if (configuracion.clase) {
        document.body.classList.add(configuracion.clase);
    }

    document.documentElement.style.backgroundColor =
        configuracion.colorNavegador;

    const metaTema = document.querySelector(
        'meta[name="theme-color"]'
    );

    if (metaTema) {
        metaTema.setAttribute(
            "content",
            configuracion.colorNavegador
        );
    }

    const etiquetaTema =
        document.getElementById("temaActual");

    if (etiquetaTema) {
        etiquetaTema.textContent =
            configuracion.etiqueta;
    }
}


function aplicarTemaGuardado() {
    const temaGuardado =
        obtenerPreferencia("tema", "claro");

    aplicarTema(temaGuardado);
}