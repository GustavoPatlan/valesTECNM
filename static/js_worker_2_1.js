function filterListEquipo() {
    let input = document.getElementById('searchInputMaterial').value.toLowerCase();
    let listItems = document.querySelectorAll('#equipoLista li');

    listItems.forEach(li => {
        let text = li.textContent.toLowerCase();
        li.style.display = text.includes(input) ? 'flex' : 'none';
    });
};

function openDialogEnviarEditar() {
    let items = document.querySelectorAll(".seccionMTabla .seccionMTCasilla");
    if (items.length === 0) {
        mostrarNotificacionRequest('Notificación', 'No hay Materiales Agregados', '#1c336c', 'bell');
    }
    else {
        dialogEnviar.showModal();
    }
};

function enviarValeEditar() {
    let items = document.querySelectorAll(".seccionMTabla .seccionMTCasilla");

    let materialList = [];
    items.forEach(item => {
        let name = item.querySelector(".seccionMTValor h5").textContent.trim();
        let quantity = item.querySelector(".seccionMTValor span").textContent.trim();

        materialList.push([name, quantity]);
    });

    fetch('/casetero/vales/activos/editado', {
        method: 'POST',
        body: JSON.stringify({ identificacion: identificacionSolicitud, materiales: materialList, reportados: materialesReportados }),
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

let itemParaEliminar = null;
let botonActualReporte = null;
let nombreMaterialReporte = null;

document.querySelectorAll('.seccionMTCasilla button').forEach(button => {
    button.addEventListener('click', function () {
        itemParaEliminar = this.parentElement;
        botonActualReporte = this;
        nombreMaterialReporte = itemParaEliminar.querySelector("h5").textContent.trim();
        document.getElementById('dialogConfirmarEliminacion').showModal();
    });
});

function confirmarEliminacion() {
    if (itemParaEliminar) {
        itemParaEliminar.remove();
        itemParaEliminar = null;
    }
    cerrarDialog('dialogConfirmarEliminacion');
}

function abrirDialogReportar() {
    document.getElementById('textoReporte').value = '';
    document.getElementById('dialogReportarMaterial').showModal();
}

function cerrarDialog(id) {
    document.getElementById(id).close();
}

let materialesReportados = [];

function enviarReporteMaterial() {
    const comentario = document.getElementById('textoReporte').value.trim();
    if (!comentario) {
        mostrarNotificacionRequest('Error', 'Escribe un motivo para reportar', 'crimson', 'bug');
        return;
    }

    const equipo = botonActualReporte.closest('.seccionMTCasilla').querySelector('h5').textContent.trim();
    const cantidad = botonActualReporte.closest('.seccionMTCasilla').querySelector('span').textContent.trim();

    materialesReportados.push([equipo, cantidad, comentario]);

    botonActualReporte.closest('.seccionMTCasilla').remove();
    cerrarDialog('dialogReportarMaterial');
    cerrarDialog('dialogConfirmarEliminacion');
}

function enviarValeEditarMaestro() {
    let items = document.querySelectorAll(".seccionMTabla .seccionMTCasilla");

    let materialList = [];
    items.forEach(item => {
        let name = item.querySelector(".seccionMTValor h5").textContent.trim();
        let quantity = item.querySelector(".seccionMTValor span").textContent.trim();

        materialList.push([name, quantity]);
    });

    fetch('/casetero/vales/maestros/editado', {
        method: 'POST',
        body: JSON.stringify({ identificacion: identificacionSolicitud, materiales: materialList, reportados: materialesReportados }),
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