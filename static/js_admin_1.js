// Función para abrir el diálogo.
function openDialog(id) {
    let dialog = document.getElementById(id);
    if (dialog) {
        dialog.showModal();
    };
};

// Función para cerrar el diálogo
function closeDialog(id) {
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

const diasValidos = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];
const labsValidos = ["Y1", "Y2", "Y6", "Y7", "Y8"];

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
                    closeDialog('dialog-nuevo-horario');
                    // sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    // window.location.href = data.url;
                    break;
            };
        });
};

// Variable para guardar la fila a eliminar.
let filaAEliminar = null;

// Función. para eliminar filas.
function eliminarHorario(boton) {
    filaAEliminar = boton.closest('tr');
    openDialog('dialog-eliminar-horario');
};

// Función para confirmar la eliminación.
function confirmarEliminacion() {
    if (filaAEliminar) {
        let datos = {
            dia: filaAEliminar.cells[0].textContent,
            lab: filaAEliminar.cells[1].textContent,
            inicio: filaAEliminar.cells[2].textContent,
            fin: filaAEliminar.cells[3].textContent
        };

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
                        closeDialog('dialog-eliminar-horario');
                        mostrarNotificacionRequest('Éxito', data.mensaje, 'lawngreen', 'check');
                        break;
                };
            });
    };
};

function actualizarDatos() {
    let nombres = document.getElementById("name").value;
    let apellidos = document.getElementById("last").value;
    let llave = document.getElementById("llave").value;

    if (!nombres || !apellidos) {
        mostrarNotificacionRequest('Error', 'Faltan datos', 'crimson', 'bug');
        return;
    }
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
                    closeDialog('dialog-actualizar-datos');
                    break;
            };
        });
};