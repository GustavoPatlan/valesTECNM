/*
    Filtra las solicitudes en la tabla según el texto de búsqueda.
    - Muestra solo las filas que coincidan con el texto ingresado
    - Oculta las no coincidentes con animación suave
    */
function filterList() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const rows = document.querySelectorAll('tbody tr');

    // Usar requestAnimationFrame para minimizar reflujos
    requestAnimationFrame(() => {
        rows.forEach(tr => {
            const text = tr.textContent.toLowerCase();
            const isVisible = text.includes(input);
            // Aplicar cambios de clase en lugar de estilos directos
            tr.classList.toggle('hidden-row', !isVisible);
            tr.classList.toggle('visible-row', isVisible);
        });
    });
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