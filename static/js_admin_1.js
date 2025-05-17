// Función para abrir el diálogo.
function openDialogIn(id) {
    let dialog = document.getElementById(id);
    if (dialog) {
        dialog.showModal();
    };
};

// Función para cerrar el diálogo
function closeDialogIn(id) {
    let dialog = document.getElementById(id);
    if (dialog) {
        dialog.close();
    };
};

// Convertir formato de hora (HH:MM -> hh:mm AM/PM)
function formato12h(hora24) {
    const [horasStr, minutos] = hora24.split(':');
    const horas = parseInt(horasStr);
    const periodo = horas >= 12 ? 'PM' : 'AM';
    const horas12 = horas % 12 || 12;
    // Asegurar 2 dígitos para horas y minutos
    const horasFormateadas = horas12.toString().padStart(2, '0');
    const minutosFormateados = minutos.padStart(2, '0');
    return `${horasFormateadas}:${minutosFormateados} ${periodo}`;
}

// Lista de días válidos para horarios.
const diasValidos = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];

// Lista de laboratorios válidos.
const labsValidos = ["Y1", "Y2", "Y6", "Y7", "Y8"];

// Función para guardar un nuevo horario
function guardarHorario() {
    let inputDia = document.getElementById("input-dia");
    let inputLab = document.getElementById("input-lab");
    let inputHora1 = document.getElementById("input-hora1").value;
    let inputHora2 = document.getElementById("input-hora2").value;

    // Validar que el valor esté en la lista de días
    if (!diasValidos.includes(inputDia.value)) {
        mostrarNotificacionRequest('Error', 'Dia Invalido', 'crimson', 'bug');
        return;
    }

    // Validar que el valor esté en la lista de laboratorios
    if (!labsValidos.includes(inputLab.value)) {
        mostrarNotificacionRequest('Error', 'Laboratorio Invalido', 'crimson', 'bug');
        return;
    }

    if (!labsValidos.includes(inputLab.value)) {
        mostrarNotificacionRequest('Error', 'Laboratorio Invalido', 'crimson', 'bug');
        return;
    }

    // Validación de horarios completos.
    if (!inputHora1 || !inputHora2) {
        mostrarNotificacionRequest('Error', 'Faltan horarios', 'crimson', 'bug');
        return;
    }

    // Si todo está correcto, enviar datos al servidor.
    fetch('/administrador/inicio/nuevo', {
        method: 'POST',
        body: JSON.stringify({
            dia: inputDia.value,
            lab: inputLab.value,
            hora1: formato12h(inputHora1),
            hora2: formato12h(inputHora2)
        }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':   // Notificación de error.
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'exito':    // Notificación exitosa.
                    mostrarNotificacionRequest('Excelente', data.mensaje, 'lawngreen', 'check');

                    // Agrega el horario a la tabla.
                    let tbody = document.querySelector('.table-container tbody');

                    let nuevaFila = document.createElement('tr');
                    nuevaFila.innerHTML = `
                        <td>${inputDia.value}</td>
                        <td>${inputLab.value}</td>
                        <td>${formato12h(inputHora1)}</td>
                        <td>${formato12h(inputHora2)}</td>
                        <td><button onclick="eliminarHorario(this)">X</button></td>
                    `;
                    tbody.appendChild(nuevaFila);

                    // Limpia los valores.
                    inputDia.value = '';
                    inputLab.value = '';

                    // Cerrar el diálogo
                    closeDialogIn('dialog-nuevo-horario');
                    break;
            };
        });
};

// Variable para guardar la fila a eliminar.
let filaAEliminar = null;

// Función. para eliminar filas.
function eliminarHorario(boton) {
    filaAEliminar = boton.closest('tr');
    openDialogIn('dialog-eliminar-horario');
};

// Función para confirmar la eliminación.
function confirmarEliminacion() {
    if (filaAEliminar) {
        // Prepara los datos de la fila a eliminar.
        let datos = {
            dia: filaAEliminar.cells[0].textContent,
            lab: filaAEliminar.cells[1].textContent,
            inicio: filaAEliminar.cells[2].textContent,
            fin: filaAEliminar.cells[3].textContent
        };
        // Envía la solicitud de eliminación al servidor.
        fetch('/administrador/inicio/eliminar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':   // Notificación de error.
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'exito':    // Notificación exitosa.
                        filaAEliminar.remove();
                        filaAEliminar = null;
                        closeDialogIn('dialog-eliminar-horario');
                        mostrarNotificacionRequest('Éxito', data.mensaje, 'lawngreen', 'check');
                        break;
                };
            });
    };
};

// Función para actualizar los datos del administrador.
function actualizarDatos() {
    // Obtiene los valores del formulario.
    let nombres = document.getElementById("name").value;
    let apellidos = document.getElementById("last").value;
    let llave = document.getElementById("llave").value;
    // Validación de campos requeridos.
    if (!nombres || !apellidos) {
        mostrarNotificacionRequest('Error', 'Faltan datos', 'crimson', 'bug');
        return;
    }
    // Envía los datos actualizados al servidor.
    fetch('/administrador/inicio/actualizar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombres: nombres, apellidos: apellidos, llave: llave })
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':   // Notificación de error.
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'exito':    // Notificación exitosa.
                    mostrarNotificacionRequest('Éxito', data.mensaje, 'lawngreen', 'check');
                    document.getElementById("nombre-admin").textContent = nombres;
                    closeDialogIn('dialog-actualizar-datos');
                    break;
            };
        });
};