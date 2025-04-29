let lastClickedElement = null;  // Almacena el elemento que abrió el diálogo

function openDialogMaterial(id, event) {
    let dialog = document.getElementById(`dialog-item-${id}`);
    if (dialog) {
        lastClickedElement = event.target;  // Guarda el elemento que disparó el evento
        dialog.showModal();
    }
}

function closeDialogMaterial(id) {
    let dialog = document.getElementById(`dialog-item-${id}`);
    if (dialog) {
        lastClickedElement = null;
        dialog.close();
    }
}

// Manejo de selección dentro del diálogo
document.querySelectorAll("dialog ul li").forEach(li => {
    li.addEventListener("click", function () {
        if (lastClickedElement) {
            let text = lastClickedElement.textContent;

            // Si ya tiene ":", eliminamos todo lo que viene después
            if (text.includes(":")) {
                text = text.split(":")[0].trim(); // Tomamos solo la parte antes de ":"
            }

            // Agregamos el nuevo valor
            lastClickedElement.textContent = `${text}: ${this.textContent}`;

            // Aplicamos estilos visuales
            lastClickedElement.style.color = "green";
        }

        // Cierra el diálogo
        let dialog = this.closest("dialog");
        if (dialog) {
            lastClickedElement = null;
            dialog.close();
        }
    });
});

function openDialogCantidad(event) {
    let dialog = document.getElementById(`dialog-item-cantidad`);
    if (dialog) {
        lastClickedElement = event.target;  // Guarda el elemento que disparó el evento
        dialog.showModal();
    }
}

function closeDialogCantidad() {
    let dialog = document.getElementById(`dialog-item-cantidad`);
    if (dialog) {
        lastClickedElement = null;
        dialog.close();
    }
}

// Función para eliminar el <span> al hacer clic en el botón "❌"
function removeSpan(event) {
    event.stopPropagation(); // Evita que se dispare el onclick del <span>

    let spanContainer = event.target.closest(".span-container"); // Encuentra el contenedor del span
    if (spanContainer) {
        spanContainer.remove(); // Elimina todo el contenedor (span + botón)
    }
}

function enviarTablasMaterial(id) {
    let tabla = document.querySelector(`.dialog-content-part-material-table[data-id="${id}"]`);
    if (!tabla) {
        mostrarNotificacionRequest('Alerta', 'No hay Materiales en el Vale', 'goldenrod', 'error');
        return;
    };

    let spans = tabla.querySelectorAll("span");
    if (spans.length === 0) {
        mostrarNotificacionRequest('Alerta', 'No hay Materiales en el Vale', 'goldenrod', 'error');
        return;
    }

    let materiales = [];
    let duplicados = new Set();
    let hayErrores = false;
    let mensaje = '';

    spans.forEach(span => {
        let texto = span.textContent.trim();

        if (texto.includes(":")) {
            let [nombre, valor] = texto.split(":").map(t => t.trim());

            if (!valor) {
                hayErrores = true;
                mensaje = 'Faltan Materiales en el Vale';
                return;
            }

            let clave = `${nombre}:${valor}`;
            if (duplicados.has(clave)) {
                hayErrores = true;
                mensaje = 'Elementos Duplicados: Revisa'
                return;
            }

            duplicados.add(clave);
            materiales.push([nombre, valor]);
        } else {
            hayErrores = true;
        }
    });

    if (hayErrores) {
        mostrarNotificacionRequest('Alerta', mensaje, 'goldenrod', 'error');
        return;
    }
    else {
        fetch('/casetero/vales/pendientes/completado', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id, materiales: materiales }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'redirect':
                        sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                        window.location.href = data.url;
                        break;
                };
            });
    };
}

function cancelarSolicitudCasetero(id) {
    let row = document.getElementById(`solicitud-${id}`);
    let dialog1 = document.getElementById(`dialog-${id}`);
    let dialog2 = document.getElementById(`dialog-accept-${id}`);
    let dialog3 = document.getElementById(`dialog-cancel-${id}`);
    if (row) {
        fetch('/casetero/vales/pendientes/cancelado', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'alerta':
                        row.remove();
                        closeDialogCancelar(id);
                        dialog1.remove();
                        dialog2.remove();
                        dialog3.remove();
                        mostrarNotificacionRequest('Exito', data.mensaje, 'lawngreen', 'check');
                        break;
                };
            });
    };
};

function reportarAlumnoCasetero(id) {
    let texto = document.getElementById(`reporte-${id}`).value.trim();
    if (!texto || texto === "") {
        mostrarNotificacionRequest('Alerta', 'No hay datos en el reporte', 'goldenrod', 'error');
    }
    else {
        fetch('/casetero/vales/activos/reporte', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id, reporte: texto }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'exito':
                        closeDialogAceptar(id)
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check')
                        break;
                };
            });
    };
};

function cancelarReporteAlumnoCasetero(id) {
    let texto = document.getElementById(`reporte-${id}`);
    let valor = texto.value.trim();

    if (!valor) {
        mostrarNotificacionRequest('Alerta', 'No hay datos en el reporte', 'goldenrod', 'error');
    } else {
        fetch('/casetero/vales/activos/cancelar', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'exito':
                        texto.value = '';
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check');
                        break;
                }
            });
    }
};

function registrarVale(id) {
    fetch('/casetero/vales/activos/finalizar', {
        method: 'POST',
        body: JSON.stringify({ identificacion: id }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'redirect':
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
            }
        });
};

function registrarValeMaestro(id) {
    fetch('/casetero/vales/maestros/finalizar', {
        method: 'POST',
        body: JSON.stringify({ identificacion: id }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'redirect':
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
            }
        });
};