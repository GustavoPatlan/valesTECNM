/*
Filtra las solicitudes en la tabla según el texto de búsqueda.
 1. Muestra solo las filas que coincidan con el texto ingresado.
 2. Oculta las no coincidentes con animación suave.
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
Abre el diálogo de confirmación para cancelar una solicitud.
*/
function openDialogCancelar(id) {
    let dialog = document.getElementById(`dialog-cancel-${id}`);
    if (dialog) {
        dialog.showModal();
    }
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
Reporta un problema con un alumno al servidor.
 1. Valida que el campo de reporte no esté vacío.
 2. Realiza petición POST con el texto del reporte.
 3. Maneja dos posibles respuestas del servidor:
   1. Error: Muestra notificación de error.
   2. Éxito: Cierra diálogo y muestra notificación de éxito.
*/
function reportarAlumnoCasetero(id) {
    // Obtiene elementos relacionados.
    let texto = document.getElementById(`reporte-${id}`).value.trim();
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
                    case 'exito':   // Redirección exitosa.
                        closeDialogAceptar(id)
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check')
                        break;
                };
            });
    };
};

/*
Cancela un reporte existente sobre un alumno.
 1. Valida que exista contenido en el campo de reporte.
 2. Realiza petición POST para cancelar el reporte.
 3. Maneja dos posibles respuestas del servidor:
   1. Error: Muestra notificación de error.
   2. Éxito: Limpia el campo y muestra notificación de éxito.
*/
function cancelarReporteAlumnoCasetero(id) {
    // Obtiene elementos relacionados.
    let texto = document.getElementById(`reporte-${id}`);
    let valor = texto.value.trim();

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
                    case 'error':   // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'exito':   // Resetear reporte.
                        texto.value = '';
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check');
                        break;
                }
            });
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
Finaliza un vale de maestro mediante petición al servidor.
 1. Realiza petición POST para finalizar el vale.
 2. Maneja dos posibles respuestas del servidor:
   1. Error: Muestra notificación de error.
   2. Redirect: Almacena mensaje y redirige a URL proporcionada.
*/
function registrarValeMaestro(id) {
    // Enviar datos al servidor.
    fetch('/casetero/vales/maestros/finalizar', {
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

/*
Cierra el diálogo de cancelación de solicitud.
*/
function closeDialogCancelar(id) {
    let dialog = document.getElementById(`dialog-cancel-${id}`);
    if (dialog) {
        dialog.close();
    }
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