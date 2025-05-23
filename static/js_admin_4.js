// Variable para guardar la fila a eliminar.
let usuarioActuar = null;

let labsDisponibles = ['Y1-Y2', 'Y6-Y7', 'Y8'];

// Función. para eliminar filas.
function actualizarUsuario(id) {
    usuarioActuar = id;
    openDialogUser('actualizar');
};

// Función. para eliminar filas.
function eliminarUsuario(id) {
    usuarioActuar = id;
    openDialogUser('eliminar');
};

// Función. para eliminar filas.
function agregarUsuario() {
    openDialogUser('abrir');
};

// Función para confirmar la eliminación.
function confirmarActualizacion() {
    if (usuarioActuar) {

        // Array para almacenar todos los valores del formulario.
        let valores = [];

        valores.push(usuarioActuar);
        // Obtener todos los inputs del diálogo.
        let inputs = document.querySelector(`#dialog-${usuarioActuar}`).querySelectorAll("input");

        // Validar cada input individualmente.
        for (let i = 0; i < inputs.length; i++) {
            let valor = inputs[i].value.trim();

            // Validación de campo vacío.
            if (valor === "") {
                mostrarNotificacionRequest('Error', 'Falta Información', 'crimson', 'bug');
                return null; // Detenemos si hay un input vacío
            }
            valores.push(valor);
        };

        // Validar que el valor esté en la lista de laboratorios.
        if (!labsDisponibles.includes(valores[2])) {
            mostrarNotificacionRequest('Error', 'Laboratorio Invalido', 'crimson', 'bug');
            return;
        }

        // Envía la solicitud de eliminación al servidor.
        fetch('/administrador/caseteros/actualizar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(valores)
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
                };
            });
    };
};

// Función para confirmar la eliminación.
function confirmarEliminacion() {
    if (usuarioActuar) {

        // Envía la solicitud de eliminación al servidor..
        fetch('/administrador/caseteros/eliminar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(usuarioActuar)
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'exito':   // Usuario eliminado.
                        document.getElementById(`solicitud-${usuarioActuar}`).remove();
                        document.getElementById(`dialog-${usuarioActuar}`).remove();
                        closeDialogUser('eliminar')
                        mostrarNotificacionRequest('Exito', data.mensaje, 'lawngreen', 'check');
                        break;
                    case 'error':    // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                };
            });
    };
};

// Función para confirmar la eliminación.
function agregarMaestro() {
    // Array para almacenar todos los valores del formulario.
    let valores = [];

    // Obtener todos los inputs del diálogo.
    let inputs = document.querySelector(`#dialog-estudiantes-eliminar`).querySelectorAll("input");

    // Validar cada input individualmente.
    for (let i = 0; i < inputs.length; i++) {
        let valor = inputs[i].value.trim();

        // Validación de campo vacío.
        if (valor === "") {
            mostrarNotificacionRequest('Error', 'Falta Información', 'crimson', 'bug');
            return null; // Detenemos si hay un input vacío
        }
        valores.push(valor);
    };

    // Validar que el valor esté en la lista de laboratorios.
    if (!labsDisponibles.includes(valores[1])) {
        mostrarNotificacionRequest('Error', 'Laboratorio Invalido', 'crimson', 'bug');
        return;
    }

    // Envía la solicitud de eliminación al servidor.
    fetch('/administrador/caseteros/nuevo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(valores)
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

/*
Abre el diálogo modal que muestra los detalles de una solicitud.
*/
function openDialogUser(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.showModal();
    };
};

/*
Cierra el diálogo modal de detalles de solicitud.
*/
function closeDialogUser(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        usuarioActuar = null;
        dialog.close();
    };
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