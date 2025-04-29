/*
Sistema de notificaciones visuales para la interfaz de usuario.

Componentes:
 - notificacionAccion: Contenedor principal de la notificación.
 - iconoForma: Icono que cambia según el tipo de mensaje.
 - iconoColor: Elemento que muestra el color de acento.
 - notificacionTitulo: Campo para el título de la notificación.
 - notificacionInfo: Campo para el mensaje detallado.
*/
let notificacion = document.getElementById("notificacionAccion");
let icono_forma = document.getElementById("iconoForma");
let icono = document.getElementById("iconoColor");
let titulo = document.getElementById("notificacionTitulo");
let mensaje = document.getElementById("notificacionInfo");

/*
Muestra una notificación en la interfaz.
*/
function mostrarNotificacionRequest(tituloT, texto, color, iconoNombre) {
    // Configurar contenido.
    mensaje.innerText = texto;
    titulo.innerText = tituloT;
    icono.style.background = color;
    notificacion.style.borderLeftColor = color;
    icono_forma.setAttribute('name', iconoNombre);

    // Mostrar notificación.
    notificacion.style.display = "flex";

    // Ocultar automáticamente después de 4 segundos.
    setTimeout(() => {
        notificacion.style.display = "none";
    }, 4000);
}

/*
Cierra manualmente la notificación visible.
*/
function cerrarNotificacion() {
    document.getElementById("notificacionAccion").style.display = "none";
};

/*
Al cargar la página, verificar si hay mensajes pendientes en sessionStorage.
*/
document.addEventListener("DOMContentLoaded", function () {
    let mensaje = sessionStorage.getItem("notificacion_mensaje");

    if (mensaje) {
        // Mostrar notificación.
        mostrarNotificacionRequest('Excelente', mensaje, 'lawngreen', 'check')

        // Limpiar el mensaje para que no reaparezca.
        sessionStorage.removeItem("notificacion_mensaje");
    }
});