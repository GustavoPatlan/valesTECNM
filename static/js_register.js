/*
Alterna la visibilidad de la contraseña entre texto plano y puntos.
- Cuando el input es tipo 'password', lo cambia a 'text' (visible).
- Cuando es 'text', lo vuelve 'password' (oculto).
*/
function togglePassword() {
    let passwordInput = document.getElementById("llaveInicio");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    };
};

/*
Abre el diálogo modal de selección de carrera.
- Muestra el diálogo con fondo oscuro.
- Bloquea la interacción con otros elementos mientras está abierto.
*/
let dialogCarrera = document.getElementById("seleccionCarrera");
function openDialogCarrea() {
    dialogCarrera.showModal(); // Muestra el diálogo como modal.
};

function closeDialogCarrea() {
    dialogCarrera.close(); // Cierra el diálogo modal.
};

/*
Filtra la lista de carreras según el texto de búsqueda.
- Convierte la búsqueda y los textos a minúsculas.
- Muestra solo los elementos que coincidan con el criterio de búsqueda.
*/
function filterList() {
    // 1. Obtiene el valor del campo de búsqueda y lo normaliza a minúsculas.
    let input = document.getElementById('searchInput').value.toLowerCase();

    // 2. Selecciona todos los elementos <li> de la lista de carreras.
    let listItems = document.querySelectorAll('#careerList li');

    // 3. Itera sobre cada elemento de la lista.
    listItems.forEach(li => {
        // 4. Obtiene el texto del elemento y lo convierte a minúsculas.
        let text = li.textContent.toLowerCase();

        // 5. Muestra u oculta el elemento según si coincide con la búsqueda.
        li.style.display = text.includes(input) ? 'flex' : 'none';
    });
};

/*
Maneja la selección de una carrera en el diálogo modal.

1. Obtiene el nombre de la carrera desde el texto del elemento seleccionado.
2. Actualiza el texto del botón de selección de carrera.
3. Aplica estilos visuales al texto para indicar selección.
4. Cierra automáticamente el diálogo modal.
*/
function selectCareer(element) {
    // 1. Extrae el nombre de la carrera del elemento seleccionado.
    let selectedCareer = element.textContent;

    // 2. Obtiene referencia al span que muestra la carrera seleccionada.
    let careerSpan = document.getElementById('seccionFECarreraBotonspan');

    // 3. Actualiza el contenido y estilos del span
    careerSpan.textContent = selectedCareer;    // Muestra la carrera seleccionada.
    careerSpan.style.color = '#333' // Cambia color a oscuro.
    careerSpan.style.fontWeight = '600' // Pone texto en negrita.

    // 4. Cierra el diálogo modal de selección.
    closeDialogCarrea();
};

/*
Maneja el cierre del diálogo de selección de carrera cuando se cancela la operación.

1. Restablece el texto del selector de carrera al valor por defecto ("Carrera").
2. Aplica estilos visuales para indicar estado no seleccionado.
3. Cierra el diálogo modal.
*/
function closeDialogCarreraCancelada() {
    // 1. Obtiene referencia al elemento que muestra la carrera seleccionada.
    let careerSpan = document.getElementById('seccionFECarreraBotonspan');

    // 2. Restablece el texto y estilos a los valores por defecto.
    careerSpan.textContent = "Carrera";  // Texto predeterminado.
    careerSpan.style.color = '#acacac'  // Color gris.
    careerSpan.style.fontWeight = '500' // Peso de fuente normal.

    // 3. Cierra el diálogo modal
    dialogCarrera.close();
};

/*
Valida y procesa el formulario de registro de usuario.

1. Recoge todos los datos del formulario.
2. Realiza validación básica de campos obligatorios.
3. Envia los datos al servidor para generación de código de verificación.
4. Maneja la respuesta del servidor:
    - Muestra errores si existen.
    - Cambia a vista de verificación de código si es exitoso.
    - Deshabilita campos y botón temporalmente.
*/
function registrarCheck() {
    // 1. Obtener valores del formulario.
    let identificador = document.getElementById("usuarioInicio").value;
    let correo = document.getElementById("correoInicio").value;
    let carrera = document.getElementById("seccionFECarreraBotonspan").textContent;
    let nombre = document.getElementById("nombreInicio").value;
    let apellido = document.getElementById("apellidoInicio").value;
    let llave = document.getElementById("llaveInicio").value;

    // 2. Validación de campos obligatorios.
    if (identificador === '' || correo === '' || nombre === '' || apellido === '' || llave === '' || carrera === 'Carrera') {
        mostrarNotificacionRequest('Notificación', 'Falta Información.', '#1c336c', 'bell');
    }
    else {
        // 3. Envío de datos al servidor.
        fetch('/registro/codigo', {
            method: 'POST',
            body: JSON.stringify({ identificador: identificador, correo: correo, carrera: carrera }),
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

                        // Cambio de vistas.
                        document.getElementById("seccionFCambioForm").style.display = "none";
                        document.getElementById("seccionFCambioCode").style.display = "flex";

                        // Deshabilitar campos editables.
                        document.getElementById("seccionFECarreraBoton").disabled = true;
                        document.getElementById("usuarioInicio").disabled = true;
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
Verifica y completa el proceso de registro del usuario validando el código de confirmación.

1. Recoge todos los datos del formulario (incluyendo el código de verificación).
2. Realiza validación de campos obligatorios.
3. Envía los datos completos al servidor para verificación final.
4. Maneja la respuesta del servidor:
    - Muestra errores si el código es incorrecto.
    - Redirige al usuario si la verificación es exitosa.
*/
function registrarAdd() {
    // 1. Obtener todos los valores del formulario.
    let identificador = document.getElementById("usuarioInicio").value;
    let correo = document.getElementById("correoInicio").value;
    let carrera = document.getElementById("seccionFECarreraBotonspan").textContent;
    let nombre = document.getElementById("nombreInicio").value;
    let apellido = document.getElementById("apellidoInicio").value;
    let llave = document.getElementById("llaveInicio").value;
    let codigo = document.getElementById("codigoInicio").value;

    // 2. Validación de campos obligatorios.
    if (identificador === '' || correo === '' || nombre === '' || apellido === '' || llave === '' || carrera === 'Carrera' || codigo === '') {
        mostrarNotificacionRequest('Notificación', 'Falta Información.', '#1c336c', 'bell');
    }
    else {
        // 3. Envío de datos al servidor.
        fetch('/registro/codigo/verificar', {
            method: 'POST',
            body: JSON.stringify({ identificador: identificador, correo: correo, carrera: carrera, nombre: nombre, apellido: apellido, llave: llave, codigo: codigo }),
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

// function codigoLlave() {
//     let correo = document.getElementById("correoInicio").value;

//     if ( correo === '' ) {
//         mostrarNotificacionRequest('Notificación', 'Falta el Correo Electrónico.', '#1c336c', 'bell');
//     }
//     else {
//         fetch('/llave/confirmar', {
//             method: 'POST',
//             body: JSON.stringify({ correo: correo }),
//             headers: { 'Content-Type': 'application/json' }
//         })
//             .then(response => response.json())
//             .then(data => {
//                 switch (data.status) {
//                     case 'error':
//                         mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
//                         break;
//                     case 'notificacion':
//                         mostrarNotificacionRequest('Notificación', data.mensaje, '#1c336c', 'bell');
//                         document.getElementById("seccionFCambioCode").style.display = "flex";
//                         document.getElementById("correoInicio").disabled = true;
//                         let button = document.getElementById("botonInicio");

//                         button.innerText = "REENVIAR CODIGO";
//                         button.style.textDecoration = "line-through";
//                         button.style.pointerEvents = "none";
//                         button.disabled = true;

//                         setTimeout(() => {
//                             button.style.textDecoration = "none";
//                             button.style.pointerEvents = "auto";
//                             button.disabled = false;
//                         }, 6000);
//                         break;
//                 };
//             });
//     };
// };

// function cambiarLlave() {
//     let correo = document.getElementById("correoInicio").value;
//     let llave = document.getElementById("llaveInicio").value;
//     let codigo = document.getElementById("codigoInicio").value;

//     if ( correo === '' || llave === '' || codigo === '') {
//         mostrarNotificacionRequest('Notificación', 'Falta Información.', '#1c336c', 'bell');
//     }
//     else {
//         fetch('/llave/cambiar', {
//             method: 'POST',
//             body: JSON.stringify({ correo: correo, llave: llave, codigo: codigo }),
//             headers: { 'Content-Type': 'application/json' }
//         })
//             .then(response => response.json())
//             .then(data => {
//                 switch (data.status) {
//                     case 'error':
//                         mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
//                         break;
//                     case 'redirect':
//                         sessionStorage.setItem("notificacion_mensaje", data.mensaje);
//                         window.location.href = data.url;
//                         break;
//                 };
//             });
//     };
// };