/*
Maneja el envío de un código de verificación al correo electrónico para restablecer la contraseña.

1. Obtiene el correo electrónico ingresado por el usuario.
2. Valida que el campo no esté vacío.
3. Envía el correo al servidor para generar y enviar el código.
4. Maneja la respuesta del servidor:
    - Muestra errores si ocurren.
    - Habilita la sección de código y desactiva temporalmente el botón si es exitoso.
*/
function codigoLlave() {
    // 1. Obtener valor del campo de correo.
    let correo = document.getElementById("correoInicio").value;

    // 2. Validar campo no vacío.
    if (correo === '') {
        mostrarNotificacionRequest('Notificación', 'Falta el correo electrónico.', '#1c336c', 'bell');
    }
    else {
        // 3. Enviar solicitud al servidor.
        fetch('/llave/confirmar', {
            method: 'POST',
            body: JSON.stringify({ correo: correo }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':   // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'notificacion':    // Manejo de éxito - transición a vista de código.
                        mostrarNotificacionRequest('Notificación', data.mensaje, '#1c336c', 'bell');

                        // Mostrar sección de código.
                        document.getElementById("seccionFCambioCode").style.display = "flex";

                        // Deshabilitar campo de correo.
                        document.getElementById("correoInicio").disabled = true;

                        // Actualizar botón principal.
                        let button = document.getElementById("botonInicio");
                        button.innerText = "REENVIAR CODIGO";
                        button.style.textDecoration = "line-through";
                        button.style.pointerEvents = "none";
                        button.disabled = true;

                        // Reactivar botón después de 6 segundos.
                        setTimeout(() => {
                            button.style.textDecoration = "none";
                            button.style.pointerEvents = "auto";
                            button.disabled = false;
                        }, 6000);
                        break;
                };
            });
    };
};

/*
Función para cambiar la contraseña del usuario después de verificar el código de confirmación.

1. Recoge los datos del formulario (correo, nueva contraseña y código de verificación).
2. Valida que todos los campos estén completos.
3. Envía la solicitud al servidor para actualizar la contraseña.
4. Maneja la respuesta del servidor (éxito/error).
*/
function cambiarLlave() {
    // 1. Obtener valores del formulario
    let correo = document.getElementById("correoInicio").value;
    let llave = document.getElementById("llaveInicio").value;
    let codigo = document.getElementById("codigoInicio").value;

    // 2. Validar campos completos.
    if (correo === '' || llave === '' || codigo === '') {
        mostrarNotificacionRequest('Notificación', 'Falta Información.', '#1c336c', 'bell');
    }
    else {
        // 3. Enviar solicitud al servidor.
        fetch('/llave/cambiar', {
            method: 'POST',
            body: JSON.stringify({ correo: correo, llave: llave, codigo: codigo }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':   // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'redirect':    //Registro exitoso - redirección.
                        sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                        window.location.href = data.url;
                        break;
                };
            });
    };
};