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
Abre el diálogo de confirmación para finalizar una solicitud.
*/
function openDialogCancelar(id) {
    let dialog = document.getElementById(`dialog-cancel-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Abre el diálogo de confirmación para reportar una solicitud.
*/
function openDialogAceptar(id) {
    let dialog = document.getElementById(`dialog-accept-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

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
Cierra el diálogo del reporte de solicitud.
*/
function closeDialogAceptar(id) {
    let dialog = document.getElementById(`dialog-accept-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Cierra el diálogo de la finalización de la solicitud.
*/
function closeDialogCancelar(id) {
    let dialog = document.getElementById(`dialog-cancel-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Envía un reporte sobre un alumno al casetero.
1. Valida que el campo de reporte no esté vacío.
2. Envía la información al servidor.
3. Muestra notificación con el resultado de la operación.
*/
function reportarAlumnoCasetero(id) {
    // Obtiene elementos relacionados.
    let texto = document.getElementById(`reporte-${id}`).value.trim();

    // Validar campos obligatorios vacíos.
    if (!texto || texto === "") {
        mostrarNotificacionRequest('Alerta', 'No hay datos en el reporte', 'goldenrod', 'error');
    }
    else {
        // Enviar datos al servidor.
        fetch('/casetero/vales/activos/reporte', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id, reporte: texto }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':   // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'exito':   // Notificación de éxito y cierra el diálogo de reporte.
                        closeDialogAceptar(id)
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check')
                        break;
                };
            });
    };
};

/*
Cancela un reporte sobre una solicitud activa.
1. Valida que exista contenido en el reporte.
2. Envía la solicitud de cancelación al servidor.
3. Muestra notificación con el resultado de la operación.
*/
function cancelarReporteAlumnoCasetero(id) {
    // Obtiene elementos relacionados.
    let texto = document.getElementById(`reporte-${id}`);
    let valor = texto.value.trim();

    // Validar campos obligatorios vacíos.
    if (!valor) {
        mostrarNotificacionRequest('Alerta', 'No hay datos en el reporte', 'goldenrod', 'error');
    } else {
        // Enviar datos al servidor.
        fetch('/casetero/vales/activos/cancelar', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':    // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'exito':   // Notificación de éxito y resetea el reporte.
                        texto.value = '';
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check');
                        break;
                }
            });
    }
};

/*
Registra la finalización de un vale.
1. Envía la solicitud de finalización al servidor.
2. Maneja la respuesta redirigiendo o mostrando notificación según el caso.
*/
function registrarVale(id) {
    // Enviar datos al servidor.
    fetch('/casetero/vales/activos/finalizar', {
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
                case 'redirect':    // Redirección exitosa.
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
            }
        });
};

function selectMaterialCheck(element) {
        // Verificar si ya está seleccionado.
        if (element.textContent.startsWith('✔ ')) {
            // Si ya está seleccionado, volver al estado original.
            element.style.color = '';
            element.style.fontWeight = '';
            element.textContent = element.textContent.substring(2);
        } else {
            // Si no está seleccionado, marcarlo.
            element.style.color = '#168300';
            element.style.fontWeight = '900';
            element.textContent = '✔ ' + element.textContent;
        }
    };