function openDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

function closeDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.close();
    }
};

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

function openDialogAceptar(id) {
    let dialog = document.getElementById(`dialog-accept-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

function closeDialogAceptar(id) {
    let dialog = document.getElementById(`dialog-accept-${id}`);
    if (dialog) {
        dialog.close();
    }
};

function openDialogCancelar(id) {
    let dialog = document.getElementById(`dialog-cancel-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

function closeDialogCancelar(id) {
    let dialog = document.getElementById(`dialog-cancel-${id}`);
    if (dialog) {
        dialog.close();
    }
};

function aceptarSolicitud(id) {
    let row = document.getElementById(`solicitud-${id}`);
    let dialog1 = document.getElementById(`dialog-${id}`);
    let dialog2 = document.getElementById(`dialog-accept-${id}`);
    let dialog3 = document.getElementById(`dialog-cancel-${id}`);
    if (row) {
        fetch('/maestro/firma/aceptar', {
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
                        closeDialogAceptar(id);
                        dialog1.remove();
                        dialog2.remove();
                        dialog3.remove();
                        mostrarNotificacionRequest('Exito', data.mensaje, 'lawngreen', 'check');
                        break;
                };
            });
    };
};

function cancelarSolicitud(id) {
    let row = document.getElementById(`solicitud-${id}`);
    let dialog1 = document.getElementById(`dialog-${id}`);
    let dialog2 = document.getElementById(`dialog-accept-${id}`);
    let dialog3 = document.getElementById(`dialog-cancel-${id}`);
    if (row) {
        fetch('/maestro/firma/cancelar', {
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