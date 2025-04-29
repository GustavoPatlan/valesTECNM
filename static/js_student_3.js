var socket = io();

socket.on('solicitudes', function (data) {
    if (data.identificacion === usuarioSesion) {
        console.log("Sesión válida. Actualizando solicitudes...");
        location.reload();
    } else {
        console.warn("Sesión inválida o no coincide.");
    }
});

/*
Abre el diálogo modal que muestra los detalles de una solicitud.
*/
function openDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo modal de detalles de solicitud.
*/
function closeDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Abre el diálogo de confirmación para cancelar una solicitud.
*/
function openDialogClose(id) {
    let dialog = document.getElementById(`dialog-close-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo de confirmación de cancelación.
*/
function closeDialogClose(id) {
    let dialog = document.getElementById(`dialog-close-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Elimina una solicitud del sistema y actualiza la interfaz.
*/
function deleteSolicitud(id) {
    // Obtiene elementos relacionados.
    let row = document.getElementById(`solicitud-${id}`);
    let dialog = document.getElementById(`dialog-${id}`);
    if (row) {
        // Envía solicitud al servidor.
        fetch('/estudiante/historial/eliminar', {
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
                    case 'alerta':  // Eliminación exitosa.
                        // Elimina la fila de la tabla y cierra diálogos.
                        row.remove();
                        closeDialogClose(id);
                        dialog.remove();

                        // Muestra notificación de éxito.
                        mostrarNotificacionRequest('Alerta', data.mensaje, 'goldenrod', 'error');
                        break;
                };
            });
    };
};