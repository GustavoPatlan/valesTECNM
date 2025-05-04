// Variable para guardar la fila a eliminar.
let usuarioActuar = null;

// Función. para eliminar filas.
function actualizarUsuario(id) {
    usuarioActuar = id;
    openDialog('actualizar');
};

// Función. para eliminar filas.
function eliminarUsuario(id) {
    usuarioActuar = id;
    openDialog('eliminar');
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

        // Validar que el valor esté en la lista de días
        if (!carrerasDisponibles.includes(valores[3])) {
            mostrarNotificacionRequest('Error', 'Carrera Invalida', 'crimson', 'bug');
            return;
        }

        fetch('/administrador/estudiantes/actualizar', {
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
        fetch('/administrador/estudiantes/eliminar', {
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
                        closeDialog('eliminar')
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
function confirmarEliminacionCompleta() {
    let llave = document.getElementById(`borrarEstudiantesInput`).value;

    if (!llave) {
        mostrarNotificacionRequest('Error', 'Contraseña Ausente', 'crimson', 'bug');
        return;
    }

    fetch('/administrador/estudiantes/borrar', {
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

/*
Abre el diálogo modal que muestra los detalles de una solicitud.
*/
function openDialog(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.showModal();
    };
};

/*
Cierra el diálogo modal de detalles de solicitud.
*/
function closeDialog(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        usuarioActuar = null;
        dialog.close();
    };
};