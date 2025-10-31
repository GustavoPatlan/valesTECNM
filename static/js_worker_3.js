/*
Memoria cache para manejar solicitudes y materiales
*/
let solicitudActualID = null;
let materialeSolicitudActualID = null;

/*
Filtra las solicitudes en la tabla según el texto de búsqueda.
 1. Muestra solo las filas que coincidan con el texto ingresado.
 2. Oculta las no coincidentes con animación suave.
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

/*
Abre el diálogo de confirmación para cancelar una solicitud.
*/
function openDialogCancelar(id) {
    let dialog = document.getElementById("dialog-cancel");
    if (dialog) {
        solicitudActualID = id; // guarda el ID en memoria
        dialog.showModal();
    };
};

/*
Cierra el diálogo de cancelación de solicitud.
*/
function closeDialogCancelar() {
    let dialog = document.getElementById("dialog-cancel");
    if (dialog) {
        dialog.close();
        solicitudActualID = null; // limpia el valor
    };
};

/*
Procesa la aceptación de una solicitud mediante petición al servidor.
*/
function aceptarSolicitud() {
    // Enviar datos al servidor.
    id = solicitudActualID;
    materiales = materialeSolicitudActualID;

    fetch('/casetero/vales/pendientes/completado', {
        method: 'POST',
        body: JSON.stringify({ identificacion: id, materiales: materiales }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':   // Notificación de error.
                    closeDialogAceptar()
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'redirect':    // Redirección exitosa.
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
            };
        });
};

/*
Cierra el diálogo de aceptación de solicitud.
*/
function closeDialogAceptar() {
    let dialog = document.getElementById("dialog-accept");
    if (dialog) {
        solicitudActualID = null; // limpia el valor
        materialeSolicitudActualID = null; // limpia el valor
        dialog.close();
    };
};

/*
Abre el diálogo modal que muestra los detalles completos de una solicitud.
*/
async function openDialogInfo(id) {
    let dialog = document.getElementById(`dialog-${id}`);
    let materialContainer = document.querySelector(`.dialog-content-part-material-table[data-id="${id}"]`);

    // Si ya cargó materiales antes, no vuelvas a pedirlos
    if (materialContainer.dataset.loaded === "true") {
        if (dialog) {
            dialog.showModal();
        };
        return
    };

    try {
        let response = await fetch(`/casetero/vales/pendientes/api/materiales/${id}`);
        if (!response.ok) throw new Error("Error al cargar materiales");

        let materiales = await response.json();
        renderMaterialVale(materialContainer, materiales);

        materialContainer.dataset.loaded = "true"; // marcar como cargado

        if (dialog) {
            dialog.showModal();
        };
    } catch (err) {
        materialContainer.innerHTML = "<p>Error al cargar materiales</p>";
    }
};

function renderMaterialVale(container, materiales) {
    // Limpia cualquier contenido anterior
    container.innerHTML = "";

    materiales.forEach(item => {
        // Cada item debe tener formato [nombre, cantidad, esEquipo]
        const [nombre, cantidad, esEquipo] = item;

        // Verifica si el material es de tipo equipo
        if (esEquipo && esEquipo.toUpperCase() === "SI") {
            const cantidadInt = parseInt(cantidad) || 1;

            for (let i = 0; i < cantidadInt; i++) {
                const div = document.createElement("div");
                div.classList.add("span-container");

                const btn = document.createElement("button");
                btn.classList.add("remove-btn");
                btn.textContent = "x";
                btn.onclick = e => removeSpan(e);

                const span = document.createElement("span");
                span.textContent = `${nombre}:`;
                span.onclick = e => openDialogMaterial(nombre, e);

                div.appendChild(btn);
                div.appendChild(span);
                container.appendChild(div);
            }
        } else {
            // Material normal (no es equipo)
            const div = document.createElement("div");
            div.classList.add("span-container");

            const btn = document.createElement("button");
            btn.classList.add("remove-btn");
            btn.textContent = "x";
            btn.onclick = e => removeSpan(e);

            const span = document.createElement("span");
            span.textContent = `${nombre}: ${cantidad}`;
            span.onclick = e => openDialogCantidad(e);

            div.appendChild(btn);
            div.appendChild(span);
            container.appendChild(div);
        }
    });
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
Abre el diálogo de selección de material específico.
 1. Recibe el ID del material y el evento como parámetros.
 2. Almacena el elemento clickeado en lastClickedElement.
 3. Muestra el diálogo modal correspondiente al material.
*/
let lastClickedElement = null;  // Almacena el elemento que abrió el diálogo

function openDialogMaterial(id, event) {
    let dialog = document.getElementById(`dialog-item-${id}`);
    if (dialog) {
        lastClickedElement = event.target;  // Guarda el elemento que disparó el evento
        dialog.showModal();
    }
}

/*
Cierra el diálogo de selección de material.
 1. Recibe el ID del material como parámetro.
 2. Limpia la referencia al último elemento clickeado.
 3. Cierra el diálogo modal correspondiente.
*/
function closeDialogMaterial(id) {
    let dialog = document.getElementById(`dialog-item-${id}`);
    if (dialog) {
        lastClickedElement = null;
        dialog.close();
    }
}

/*
Configura los listeners para los items de diálogo.
 1. Agrega eventos click a todos los elementos <li> dentro de diálogos.
 2. Actualiza el texto del elemento que abrió el diálogo con la selección.
 3. Aplica estilo visual (color verde) a la selección.
 4. Cierra el diálogo después de la selección.
*/
document.querySelectorAll("dialog ul li").forEach(li => {
    li.addEventListener("click", function () {
        if (lastClickedElement) {
            let text = lastClickedElement.textContent;

            // Si ya tiene ":", eliminamos todo lo que viene después
            if (text.includes(":")) {
                text = text.split(":")[0].trim(); // Tomamos solo la parte antes de ":"
            }

            // Agregamos el nuevo valor
            lastClickedElement.textContent = `${text}: ${this.textContent}`;

            // Aplicamos estilos visuales
            lastClickedElement.style.color = "green";
        }

        // Cierra el diálogo
        let dialog = this.closest("dialog");
        if (dialog) {
            lastClickedElement = null;
            dialog.close();
        }
    });
});

/*
Abre el diálogo de selección de cantidad.
 - Recibe el evento como parámetro.
 - Almacena el elemento clickeado en lastClickedElement.
 - Muestra el diálogo modal de cantidades.
*/
function openDialogCantidad(event) {
    let dialog = document.getElementById(`dialog-item-cantidad`);
    if (dialog) {
        lastClickedElement = event.target;  // Guarda el elemento que disparó el evento
        dialog.showModal();
    }
}

/*
Cierra el diálogo de selección de cantidad.
 - Limpia la referencia al último elemento clickeado.
 - Cierra el diálogo modal de cantidades.
*/
function closeDialogCantidad() {
    let dialog = document.getElementById(`dialog-item-cantidad`);
    if (dialog) {
        lastClickedElement = null;
        dialog.close();
    }
}

/*
Elimina un elemento span y su contenedor.
 1. Recibe el evento como parámetro.
 2. Detiene la propagación del evento para evitar conflictos.
 3. Encuentra y elimina el contenedor padre del botón clickeado.
*/
function removeSpan(event) {
    event.stopPropagation(); // Evita que se dispare el onclick del <span>

    let spanContainer = event.target.closest(".span-container"); // Encuentra el contenedor del span
    if (spanContainer) {
        spanContainer.remove(); // Elimina todo el contenedor (span + botón)
    }
}

/*
Envía los materiales asociados a un vale al servidor.
 1. Valida la existencia de materiales antes de enviar.
 2. Verifica que todos los materiales tengan formato correcto.
 3. Detecta y reporta materiales duplicados.
 4. Realiza petición POST al servidor con los datos validados.
 5. Maneja respuestas de error y redirección.
*/
function enviarTablasMaterial(id) {
    // Verificar existencia de tabla y materiales.
    let tabla = document.querySelector(`.dialog-content-part-material-table[data-id="${id}"]`);
    if (!tabla) {
        mostrarNotificacionRequest('Alerta', 'No hay Materiales en el Vale', 'goldenrod', 'error');
        return;
    };

    // Obtener todos los elementos span que contienen los materiales.
    let spans = tabla.querySelectorAll("span");
    if (spans.length === 0) {
        mostrarNotificacionRequest('Alerta', 'No hay Materiales en el Vale', 'goldenrod', 'error');
        return;
    }

    // Procesamiento de materiales.
    let materiales = [];
    let duplicados = new Set();
    let hayErrores = false;
    let mensaje = '';

    // Iterar sobre cada material para validar y procesar.
    spans.forEach(span => {
        let texto = span.textContent.trim();

        // Validar formato nombre:cantidad.
        if (texto.includes(":")) {
            let [nombre, valor] = texto.split(":").map(t => t.trim());

            // Validar que la cantidad no esté vacía.
            if (!valor) {
                hayErrores = true;
                mensaje = 'Faltan Materiales en el Vale';
                return;
            }

            // Control de duplicados.
            let clave = `${nombre}:${valor}`;
            if (duplicados.has(clave)) {
                hayErrores = true;
                mensaje = 'Elementos Duplicados: Revisa'
                return;
            }

            // Almacenar material validado.
            duplicados.add(clave);
            materiales.push([nombre, valor]);
        } else {
            hayErrores = true;
        }
    });

    // Manejo de resultados.
    if (hayErrores) {
        mostrarNotificacionRequest('Alerta', mensaje, 'goldenrod', 'error');
        return;
    }
    else {
        materialeSolicitudActualID = materiales;
        openDialogAceptar(id);
    };
};

/*
Cancela una solicitud de vale mediante petición al servidor.
 1. Realiza petición POST para cancelar la solicitud.
 2. Elimina la fila de la tabla y los diálogos asociados al completarse.
 3. Maneja dos posibles respuestas del servidor:
   1. Error: Muestra notificación de error.
   2. Alerta: Elimina elementos y muestra notificación de éxito.
*/
function cancelarSolicitudCasetero() {
    // Obtiene elementos relacionados.
    id = solicitudActualID;
    let row = document.getElementById(`solicitud-${id}`);
    let dialog1 = document.getElementById(`dialog-${id}`);

    if (row) {
        // Enviar datos al servidor.
        fetch('/casetero/vales/pendientes/cancelado', {
            method: 'POST',
            body: JSON.stringify({ identificacion: id }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                switch (data.status) {
                    case 'error':   // Notificación de error.
                        closeDialogCancelar();
                        mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                        break;
                    case 'alerta':  // Remover solicitud.
                        row.remove();
                        closeDialogCancelar();
                        dialog1.remove();
                        mostrarNotificacionRequest('Exito', data.mensaje, 'lawngreen', 'check');
                        break;
                };
            });
    };
};

/*
Abre el diálogo de confirmación para aceptar una solicitud.
*/
function openDialogAceptar(id) {
    let dialog = document.getElementById("dialog-accept");
    if (dialog) {
        solicitudActualID = id; // guarda el ID en memoria
        dialog.showModal();
    };
};