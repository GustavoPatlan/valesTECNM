/*
Abre el diálogo modal que muestra los detalles completos de una solicitud.
*/
function openDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo de información de solicitud.
*/
function closeDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Filtra las solicitudes en la tabla según el texto de búsqueda.
 - Muestra solo las filas que coincidan con el texto ingresado
 - Oculta las no coincidentes con animación suave
*/
function filterList() {
    let input = document.getElementById('searchInput').value.toLowerCase();
    let rows = document.querySelectorAll('tbody tr');

    rows.forEach(tr => {
        let text = tr.textContent.toLowerCase();
        if (text.includes(input)) {
            tr.style.visibility = 'visible';
            tr.style.position = 'relative';
            tr.style.height = 'auto';
            tr.style.opacity = '1';
        } else {
            tr.style.visibility = 'hidden';
            tr.style.position = 'absolute';
            tr.style.height = '0px';
            tr.style.opacity = '0';
        }
    });
};

/*
Abre el diálogo de confirmación para aceptar una solicitud.
*/
function openDialogAceptar(id) {
    let dialog = document.getElementById(`dialog-accept-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo de aceptación de solicitud.
*/
function closeDialogAceptar(id) {
    let dialog = document.getElementById(`dialog-accept-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Procesa la aceptación de una solicitud mediante petición al servidor.
*/
function aceptarSolicitud(id) {
    // Obtiene elementos relacionados.
    let row = document.getElementById(`solicitud-${id}`);
    let dialog1 = document.getElementById(`dialog-${id}`);
    let dialog2 = document.getElementById(`dialog-accept-${id}`);
    let dialog3 = document.getElementById(`dialog-cancel-${id}`);
    if (row) {
        // Envía solicitud al servidor.
        fetch('/maestro/firma/aceptar', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':   // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'alerta':  // Modificación exitosa.
                        row.remove();
                        closeDialogAceptar(id);
                        dialog1.remove();
                        dialog2.remove();
                        dialog3.remove();

                        // Muestra notificación de éxito.
                        mostrarNotificacionRequest('Exito', data.mensaje, 'lawngreen', 'check');
                        break;
                };
            });
    };
};

/*
Procesa la cancelación de una solicitud mediante petición al servidor.
*/
function cancelarSolicitud(id) {
    // Obtiene elementos relacionados.
    let row = document.getElementById(`solicitud-${id}`);
    let dialog1 = document.getElementById(`dialog-${id}`);
    let dialog2 = document.getElementById(`dialog-accept-${id}`);
    let dialog3 = document.getElementById(`dialog-cancel-${id}`);
    if (row) {
        // Envía solicitud al servidor.
        fetch('/maestro/firma/cancelar', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':   // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'alerta':  // Modificación exitosa.
                        row.remove();
                        closeDialogCancelar(id);
                        dialog1.remove();
                        dialog2.remove();
                        dialog3.remove();

                        // Muestra notificación de éxito.
                        mostrarNotificacionRequest('Exito', data.mensaje, 'lawngreen', 'check');
                        break;
                };
            });
    };
};

// Revisar donde se usa
function openDialogDescargar() {
    let dialog = document.getElementById(`dialog-download`);
    if (dialog) {
        dialog.showModal();
    }
};

function closeDialogDescargar() {
    let dialog = document.getElementById(`dialog-download`);
    if (dialog) {
        dialog.close();
    }
};

/*
Abre el diálogo modal que muestra los detalles de una solicitud.
*/
function openDialogBorrarRegistros(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.showModal();
    };
};

/*
Cierra el diálogo modal de detalles de solicitud.
*/
function closeDialogBorrarRegistros(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        usuarioActuar = null;
        dialog.close();
    };
};

// Función para confirmar la eliminación.
function confirmarEliminacionCompleta() {
    let llave = document.getElementById(`borrarEstudiantesInput`).value;

    // Envía la solicitud de eliminación masiva al servidor.
    if (!llave) {
        mostrarNotificacionRequest('Error', 'Contraseña Ausente', 'crimson', 'bug');
        return;
    }

    // Envía la solicitud de eliminación al servidor.
    fetch('/administrador/registros/borrar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(llave)
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'redirect':    // Redirección exitosa.
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
                case 'error':    // Notificación de error.
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
            };
        });
};