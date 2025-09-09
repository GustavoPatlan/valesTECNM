/*
Envía una nueva contraseña al servidor para actualización.
 - Valida que el campo no esté vacío.
 - Envia la nueva contraseña mediante petición.
 - Muestra notificaciones del estado de la operación.
*/
function actualizarDatosGeneralesLLave() {
    // Obtener nueva contraseña.
    let llave = document.getElementById("llave").value;

    // Validar campo requerido.
    if (llave === '') {
        mostrarNotificacionRequest('Notificación', 'No agregaste Contraseña', '#1c336c', 'bell');
    }
    else {
        // Enviar nueva contraseña al servidor.
        fetch('/maestro/perfil/llave', {
            method: 'POST',
            body: JSON.stringify({ llave: llave }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'exito':   // Actualizar interfaz con nuevos datos.
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check');
                        document.getElementById("llave").value = '';
                        break;
                };
            });
    };
};