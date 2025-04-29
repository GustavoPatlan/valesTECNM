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
Controla los cambios entre opciones de usuario (Estudiante/Maestro/Casetero/Admin):
1. Muestra u oculta secciones según el tipo de usuario seleccionado.
2. Cambia el placeholder del input de usuario:
    - "Número de Control" para estudiantes.
    - "Identificación" para otros roles.
*/
let radios = document.querySelectorAll('input[name="checkIN"]');
let inputUsuario = document.getElementById('usuarioInicio');

radios.forEach(radio => {
    radio.addEventListener('change', function () {
        let esEstudiante = document.getElementById('Estudiante').checked;

        // Muestra u oculta secciones relevantes.
        document.getElementById('enlacesEstudiantes1').style.display = esEstudiante ? 'flex' : 'none';
        document.getElementById('enlacesEstudiantes2').style.display = esEstudiante ? 'flex' : 'none';
        document.getElementById('enlacesTrabajadores').style.display = esEstudiante ? 'none' : 'flex';

        // Cambiar texto guía del input.
        inputUsuario.placeholder = esEstudiante ? 'Número de Control' : 'Identificación';
    });
});

/*
Valida y procesa el inicio de sesión:
1. Obtiene credenciales (usuario + contraseña + tipo de rol).
2. Valida campos vacíos.
3. Envia datos al servidor y maneja la respuesta:
    - Muestra errores/alertas.
    - Redirige si es exitoso.
*/
function iniciarSesionCheck() {
    // 1. Obtener datos del formulario.
    let identificador = document.getElementById("usuarioInicio").value;
    let llave = document.getElementById("llaveInicio").value;
    let usuario = document.querySelector('input[name="checkIN"]:checked').id;

    // 2. Validación de campos vacíos.
    if (identificador === '') {
        mostrarNotificacionRequest('Notificación', 'Identificación Ausente.', '#1c336c', 'bell');
    }
    else if (llave === '') {
        mostrarNotificacionRequest('Notificación', 'Contraseña Ausente.', '#1c336c', 'bell');
    }
    else {
        // 3. Enviar datos al servidor
        fetch('/inicio/entrar', {
            method: 'POST',
            body: JSON.stringify({ identificador: identificador, llave: llave, usuario: usuario }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':   // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'alerta':  // Notificación de advertencia.
                        mostrarNotificacionRequest('Alerta', data.mensaje, 'goldenrod', 'error');
                        break;
                    case 'redirect':    // Redirección exitosa.
                        sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                        window.location.href = data.url;
                        break;
                };
            });
    };
};