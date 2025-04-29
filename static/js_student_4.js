/*
Cambia la vista al formulario de cambio de contraseña y actualiza los estilos visuales.
 - Oculta la sección de edición de nombres.
 - Muestra la sección de cambio de contraseña.
 - Actualiza el estado activo de los botones del menú.
 - Cambia la visibilidad de los botones de acción.
*/
function toggleMenuProfile2() {
    // Mostrar/ocultar secciones.
    document.getElementById("seccionIDatosNombres").style.display = 'none';
    document.getElementById("seccionIDatosLLave").style.display = 'flex';

    // Actualizar estado de botones del menú.
    document.getElementById("botonCuenta").classList.remove("botonActivo");
    document.getElementById("botonLlave").classList.add("botonActivo");

    // Cambiar botones de acción visibles.
    document.getElementById("botonCuentaAccion").style.display = 'none';
    document.getElementById("botonLlaveAccion").style.display = 'flex';
}

/*
Cambia la vista al formulario de cambio de contraseña y actualiza los estilos visuales.
 - Oculta la sección de edición de nombres.
 - Muestra la sección de cambio de contraseña.
 - Actualiza el estado activo de los botones del menú.
 - Cambia la visibilidad de los botones de acción.
*/
function toggleMenuProfile1() {
    // Mostrar/ocultar secciones.
    document.getElementById("seccionIDatosNombres").style.display = 'flex';
    document.getElementById("seccionIDatosLLave").style.display = 'none';

    // Actualizar estado de botones del menú.
    document.getElementById("botonCuenta").classList.add("botonActivo");
    document.getElementById("botonLlave").classList.remove("botonActivo");

    // Cambiar botones de acción visibles.
    document.getElementById("botonCuentaAccion").style.display = 'flex';
    document.getElementById("botonLlaveAccion").style.display = 'none';
}


/*
Envía los datos actualizados del perfil (nombres y apellidos) al servidor.
 - Valida que los campos no estén vacíos.
 - Envia los datos mediante una petición.
 - Actualiza la interfaz con la respuesta del servidor.
 - Muestra notificaciones del estado de la operación.
*/
function actualizarDatosGenerales() {
    // Obtener valores de los inputs.
    let nombres = document.getElementById("nombres").value;
    let apellidos = document.getElementById("apellidos").value;

    // Validar campos requeridos.
    if (nombres === '' || apellidos === '') {
        mostrarNotificacionRequest('Notificación', 'Datos Ausentes', '#1c336c', 'bell');
    }
    else {
        // Enviar datos al servidor.
        fetch('/estudiante/perfil/datos', {
            method: 'POST',
            body: JSON.stringify({ nombres: nombres, apellidos: apellidos }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'exito':   // Actualizar interfaz con nuevos datos.
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check');
                        document.getElementById("nombres").value = data.informacion[0];
                        document.getElementById("apellidos").value = data.informacion[1];
                        document.getElementById("nombreSaludo").innerText = data.informacion[0];
                        break;
                };
            });
    };
};

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
        fetch('/estudiante/perfil/llave', {
            method: 'POST',
            body: JSON.stringify({ llave: llave }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'exito':   // Actualizar interfaz con nuevos datos.
                        mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check');
                        break;
                };
            });
    };
};