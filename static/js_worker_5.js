/*
Abre el diálogo modal para seleccionar condición del material.
*/
function openDialogCondicion(id) {
    let dialog = document.getElementById(`dialog-condition-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo de selección de condición.
*/
function closeDialogCondicion(id) {
    let dialog = document.getElementById(`dialog-condition-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Selecciona y aplica una condición al material especificado.
*/
function selectCondition(element, id) {
    let selectedCondition = element.textContent;
    let conditionSpan = document.getElementById(`condicion-span-${id}`);
    conditionSpan.textContent = selectedCondition;
    closeDialogCondicion(id);
};

/*
Abre el diálogo modal para seleccionar disponibilidad del material.
*/
function openDialogDisponibilidad(id) {
    let dialog = document.getElementById(`dialog-disponibilidad-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo de selección de disponibilidad.
*/
function closeDialogDisponibilidad(id) {
    let dialog = document.getElementById(`dialog-disponibilidad-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Selecciona y aplica una disponibilidad al material especificado.
*/
function selectDisponibilidad(element, id) {
    let selectedDisponible = element.textContent;
    let disponibleSpan = document.getElementById(`disponibilidad-span-${id}`);
    disponibleSpan.textContent = selectedDisponible;
    closeDialogDisponibilidad(id);
};

/*
Obtiene y envía los valores actualizados de un material al servidor.
Realiza validación de campos vacíos antes del envío.
*/
function obtenerValoresMaterial(id) {
    // Busca el diálogo específico usando el ID proporcionado.
    let dialogMaterial = document.querySelector(`#dialog-${id}`);

    // Array para almacenar todos los valores del formulario.
    let valores = [];

    // Obtener todos los inputs del diálogo.
    let inputs = dialogMaterial.querySelectorAll("input");

    // Validar cada input individualmente.
    for (let i = 0; i < inputs.length; i++) {
        let valor = inputs[i].value.trim();

        // Validación de campo vacío.
        if (valor === "") {
            mostrarNotificacionRequest('Error', 'Falta Información', 'crimson', 'bug');
            return null; // Detenemos si hay un input vacío
        }
        valores.push(valor);
    }

    // Condición del material y disponibilidad del material.
    let condicionSpan = document.getElementById(`condicion-span-${id}`);
    let disponibilidadSpan = document.getElementById(`disponibilidad-span-${id}`);

    let condicion = condicionSpan ? condicionSpan.textContent.trim() : "";
    let disponibilidad = disponibilidadSpan ? disponibilidadSpan.textContent.trim() : "";

    valores.push(condicion);
    valores.push(disponibilidad);

    // Textarea
    let textarea = dialogMaterial.querySelector("textarea");
    let observaciones = textarea ? textarea.value.trim() : "";
    valores.push(observaciones);

    // Configuración y ejecución de la petición fetch.
    fetch('/casetero/material/actualizado', {
        method: 'POST',
        body: JSON.stringify({ identificacion: id, valores: valores }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':   // Mostrar error específico del servidor.
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'redirect':    // Redirigir a la URL proporcionada por el servidor.
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
            };
        });
};

/*
Elimina un material mediante petición al servidor.
*/
function borrarMaterial(id) {
    // Configuración y ejecución de la petición fetch.
    fetch('/casetero/material/eliminado', {
        method: 'POST',
        body: JSON.stringify({ identificacion: id }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':   // Mostrar error específico del servidor.
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'redirect':    // Redirigir a la URL proporcionada por el servidor.
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
            };
        });
};

/*
Abre el diálogo para agregar un nuevo material.
*/
function openDialogNuevo() {
    let dialog = document.getElementById(`dialog-nuevo-material`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo de nuevo material.
*/
function closeDialogNuevo() {
    let dialog = document.getElementById(`dialog-nuevo-material`);
    if (dialog) {
        dialog.close();
    }
};

/*
Configura los listeners para los radio buttons de tipo de material.
Controla la visualización de los campos según la selección (Equipo/Componente).
*/
let radios = document.querySelectorAll('input[name="checkIN"]');
let inputUsuario = document.getElementById('equipoComponente');
let inputMaterialSeleccionado = document.getElementById('inputMaterialSeleccionado');

let cantidadBlock = document.querySelectorAll('.dialog-content-material')[1];
let casetaBlock = document.querySelectorAll('.dialog-content-material')[2];

// Listas del dialog para materiales
let potList = document.getElementById('potList');
let adList = document.getElementById('adList');

radios.forEach(radio => {
    radio.addEventListener('change', function () {
        let esEquipo = document.getElementById('Equipo').checked;

        // Cambia el título
        inputUsuario.textContent = esEquipo ? 'EQUIPO:' : 'COMPONENTE:';
        inputMaterialSeleccionado.value = ''

        // Mostrar/ocultar bloques
        if (esEquipo) {
            cantidadBlock.classList.add('activate');
            casetaBlock.classList.remove('activate');
            potList.style.display = 'block';
            adList.style.display = 'none';
        } else {
            cantidadBlock.classList.remove('activate');
            casetaBlock.classList.add('activate');
            potList.style.display = 'none';
            adList.style.display = 'block';
        }
    });
});

/*
Selecciona un material de la lista y lo asigna al campo correspondiente.
*/
function selectMaterial(element) {
    let value = element.textContent.trim();
    let inputField = document.getElementById('inputMaterialSeleccionado');

    if (value === 'NINGUNO') {
        inputField.value = '';
    } else {
        inputField.value = value;
    }

    closeDialogEquipo();
}

/*
Abre el diálogo para seleccionar equipo.
*/
function openDialogEquipo() {
    let dialog = document.getElementById(`dialog-nuevo-equipo`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo de selección de equipo.
*/
function closeDialogEquipo() {
    let dialog = document.getElementById(`dialog-nuevo-equipo`);
    if (dialog) {
        dialog.close();
    }
};

/*
Filtra la lista de materiales según el texto de búsqueda.
Muestra/oculta elementos de las listas potList, adList y sdList.
*/
function filterListMaterial() {
    let input = document.getElementById('searchInputMaterial').value.toLowerCase();
    let lists = ['potList', 'adList', 'sdList'];

    lists.forEach(listId => {
        let listItems = document.querySelectorAll(`#${listId} li`);
        listItems.forEach(li => {
            let text = li.textContent.toLowerCase();
            li.style.display = text.includes(input) ? 'flex' : 'none';
        });
    });
};

/*
Verifica si ya existe un material con el mismo equipo y caseta.
*/
function revisarMaterialAntesDeEnviar(equipo, caseta) {
    // Selecciona todas las filas del cuerpo de la tabla.
    let filas = document.querySelectorAll("tbody tr");
    let coincidencia = false;

    filas.forEach(tr => {
        // Inicializar variables para almacenar los valores de la fila actual.
        let tds = tr.querySelectorAll("td");
        let equipoText = "";
        let casetaText = "";

        // Usa el atributo data-label para identificar qué dato contiene cada celda.
        tds.forEach(td => {
            if (td.getAttribute("data-label") === "Equipo") {
                equipoText = td.textContent.trim();
            }
            if (td.getAttribute("data-label") === "Caseta") {
                casetaText = td.textContent.trim();
            }
        });

        // Verifica si ambos valores coinciden exactamente.
        if (equipoText === equipo && casetaText === caseta) {
            mostrarNotificacionRequest('Error', 'El Equipo y Número de Caseta ya está asignado', 'crimson', 'bug');
            coincidencia = true;
        }
    });

    return coincidencia;
}

/*
Procesa el formulario para agregar un nuevo material.
Realiza validaciones y envía los datos al servidor.
*/
function agregarMaterial() {
    // Obtener valores de todos los campos del formulario.
    let tipoSeleccionado = document.querySelector('input[name="checkIN"]:checked').id;
    let inputMaterial = document.getElementById('inputMaterialSeleccionado').value.trim();
    let marca = document.getElementById('inputMarca').value.trim();
    let modelo = document.getElementById('inputModelo').value.trim();
    let cantidad = document.getElementById('inputCantidad').value.trim();
    let caseta = document.getElementById('inputCaseta').value.trim();
    let serie = document.getElementById('inputSerie').value.trim();
    let inventario = document.getElementById('inputInventario').value.trim();
    let voltaje = document.getElementById('inputVoltaje').value.trim();
    let potencia = document.getElementById('inputPotencia').value.trim();

    // Validación básica: material seleccionado es requerido.
    if (!inputMaterial) {
        mostrarNotificacionRequest('Error', 'Faltan Información', 'crimson', 'bug');
        return;
    }

    // Si existe la coincidencia, detenemos aquí
    let existe = revisarMaterialAntesDeEnviar(inputMaterial, caseta);
    if (existe) return;

    // Envío de datos al servidor.
    fetch('/casetero/material/agregado', {
        method: 'POST',
        body: JSON.stringify({
            radio: tipoSeleccionado,
            equipo: inputMaterial,
            marca: marca,
            modelo: modelo,
            cantidad: cantidad,
            caseta: caseta,
            serie: serie,
            inventario: inventario,
            voltaje: voltaje,
            potencia: potencia
        }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':   // Mostrar error específico del servidor.
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'redirect':    // Redirigir a la URL proporcionada.
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
            }
        });
}

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

// Revisar donde se usa
function openDialogDescargar() {
    let dialog = document.getElementById(`dialog-download`);
    if (dialog) {
        dialog.showModal();
    }
};

function closeDialogDescargar() {
    let dialog = document.getElementById(`dialog-download`);
    if (dialog) {
        dialog.close();
    }
};

/*
Abre el diálogo modal que muestra los detalles completos de una solicitud.
*/
function openDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Abre el diálogo de confirmación para aceptar una solicitud.
*/
function openDialogAceptar(id) {
    let dialog = document.getElementById(`dialog-accept-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Abre el diálogo de confirmación para cancelar una solicitud.
*/
function openDialogCancelar(id) {
    let dialog = document.getElementById(`dialog-cancel-${id}`);
    if (dialog) {
        dialog.showModal();
    }
};

/*
Cierra el diálogo de información de solicitud.
*/
function closeDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Cierra el diálogo de aceptación de solicitud.
*/
function closeDialogAceptar(id) {
    let dialog = document.getElementById(`dialog-accept-${id}`);
    if (dialog) {
        dialog.close();
    }
};

/*
Cierra el diálogo de cancelación de solicitud.
*/
function closeDialogCancelar(id) {
    let dialog = document.getElementById(`dialog-cancel-${id}`);
    if (dialog) {
        dialog.close();
    }
};