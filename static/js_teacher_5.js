let dialogSalon = document.getElementById("seleccionSalon");
let botonMaterial = document.getElementById('botonAbrirMaterial');

/*
Abre el diálogo modal para seleccionar salón.
*/
function openDialogSalon() {
    dialogSalon.showModal();
};

/*
Cierra el diálogo de salón sin realizar cambios.
*/
function closeDialogSalon() {
    dialogSalon.close();
};

/*
Selecciona un salón de la lista y configura la interfaz según el tipo:
1. Actualiza el input de salón con estilos visuales.
2. Muestra el botón para agregar materiales.
3. Configura qué lista de materiales mostrar según el salón seleccionado.
4. Limpia la tabla de materiales existentes.
5. Cierra el diálogo.
*/
function selectSalon(element) {
    let selectedSalon = element.textContent;
    let salonInput = document.getElementById('valeSalonInput');
    document.querySelector('.seccionMTabla').innerHTML = '';
    salonInput.value = selectedSalon;
    salonInput.style.color = '#333'
    salonInput.style.fontWeight = '500'
    botonMaterial.style.display = 'flex';

    // Configuración de listas de materiales según salón.
    if (selectedSalon === 'Y1' || selectedSalon === 'Y2') {
        document.getElementById('potList').style.display = 'block';
        document.getElementById('adList').style.display = 'none';
        document.getElementById('sdList').style.display = 'none';
    }
    else if (selectedSalon === 'Y6' || selectedSalon === 'Y7') {
        document.getElementById('potList').style.display = 'none';
        document.getElementById('adList').style.display = 'block';
        document.getElementById('sdList').style.display = 'none';
    }
    else if (selectedSalon === 'Y8') {
        document.getElementById('potList').style.display = 'none';
        document.getElementById('adList').style.display = 'none';
        document.getElementById('sdList').style.display = 'block';
    }
    dialogSalon.close();
};

/*
Cancela la selección de salón:
1. Limpia el input y la tabla de materiales.
2. Oculta todas las listas de materiales.
3. Oculta el botón para agregar materiales.
4. Cierra el diálogo.
*/
function closeDialogSalonCancelada() {
    let salonInput = document.getElementById('valeSalonInput');
    document.querySelector('.seccionMTabla').innerHTML = '';
    salonInput.value = '';
    document.getElementById('potList').style.display = 'none';
    document.getElementById('adList').style.display = 'none';
    document.getElementById('sdList').style.display = 'none';
    botonMaterial.style.display = 'none';
    dialogSalon.close();
};

let dialogMaterial = document.getElementById("seleccionMaterial");

/*
Abre el diálogo modal para seleccionar material.
*/
function openDialogMaterial() {
    dialogMaterial.showModal();
};

/*
Cierra el diálogo de material sin realizar cambios.
*/
function closeDialogMaterial() {
    selectedItemName = '';
    dialogMaterial.close();
};

/*
Filtra las listas de materiales según el texto ingresado:
1. Convierte el texto de búsqueda a minúsculas.
2. Recorre todas las listas de materiales.
3. Muestra solo los elementos que coincidan con la búsqueda.
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

let selectedItemName = '';
let dialogMaterialCantidad = document.getElementById('seleccionCantidadMaterial');

/*
Selecciona un material de la lista:
1. Almacena el nombre del material seleccionado.
2. Verifica si el material ya fue agregado.
3. Si no existe, abre el diálogo para seleccionar cantidad.
4. Si existe, muestra una alerta temporal.
*/
function selectMaterial(element) {
    selectedItemName = element.textContent;
    let existingItems = document.querySelectorAll('.seccionMTabla .seccionMTValor h5');

    // Verifica si ya existe un elemento con el mismo nombre
    let itemExists = Array.from(existingItems).some(item => item.textContent === selectedItemName);

    if (itemExists) {
        let mensajeAlertaMaterial = document.getElementById('dialogCCAlerta');
        mensajeAlertaMaterial.style.display = "flex";

        setTimeout(() => {
            mensajeAlertaMaterial.style.display = "none";
        }, 4000);
    } else {
        dialogMaterialCantidad.showModal();
    }
}

/*
Agrega un material con su cantidad a la tabla:
1. Crea la estructura HTML para mostrar el material y su cantidad.
2. Incluye un botón para eliminar el material.
3. Agrega el elemento a la tabla.
4. Cierra los diálogos de material y cantidad.
*/
function selectMaterialCantidad(element) {
    let quantity = element.textContent;

    // Crear el contenedor principal.
    let container = document.createElement('div');
    container.classList.add('seccionMTCasilla');

    // Crear el div para la información.
    let infoDiv = document.createElement('div');
    infoDiv.classList.add('seccionMTValor');

    // Crear y asignar el nombre seleccionado.
    let nameElement = document.createElement('h5');
    nameElement.textContent = selectedItemName;

    // Crear y asignar la cantidad seleccionada.
    let quantityElement = document.createElement('span');
    quantityElement.textContent = quantity;

    // Agregar elementos al contenedor de información.
    infoDiv.appendChild(nameElement);
    infoDiv.appendChild(quantityElement);

    // Crear y configurar el botón de eliminación.
    let deleteButton = document.createElement('button');
    deleteButton.textContent = 'X';
    deleteButton.onclick = function () {
        container.remove(); // Eliminar el contenedor al hacer click.
    };

    // Agregar todo al contenedor principal.
    container.appendChild(infoDiv);
    container.appendChild(deleteButton);

    // Agregar el nuevo elemento a la secciónMTabla.
    let sectionTable = document.querySelector('.seccionMTabla');
    sectionTable.appendChild(container);

    // Cerrar el diálogo.
    dialogMaterial.close();
    dialogMaterialCantidad.close();
};

/*
Cancela la selección de cantidad de material:
1. Limpia el nombre del material seleccionado.
2. Cierra los diálogos de material y cantidad.
*/
function closeQuantityDialog() {
    let dialogMaterialCantidad = document.getElementById('seleccionCantidadMaterial');
    selectedItemName = '';
    dialogMaterial.close();
    dialogMaterialCantidad.close();
};


let dialogEnviar = document.getElementById("seleccionEnviar");

/*
Cierra el diálogo de confirmación de envío sin realizar acciones.
*/
function closeDialogEnviar() {
    dialogEnviar.close();
};

/*
Selecciona un material predefinido:
1. Extrae nombre y cantidad del texto del elemento.
2. Verifica si ya existe un material idéntico en la tabla.
3. Si existe, muestra alerta temporal.
4. Si no existe, crea y agrega el elemento a la tabla.
5. Cierra el diálogo de materiales.
*/
function selectMaterialPredefinido(element) {
    let text = element.textContent;
    let [nombre, cantidad] = text.split(':').map(t => t.trim());

    // Verifica si ya existe un elemento con el mismo nombre y cantidad
    let existentes = document.querySelectorAll('.seccionMTabla .seccionMTCasilla');

    let existe = Array.from(existentes).some(elem => {
        let nombreElem = elem.querySelector('h5')?.textContent.trim();
        let cantidadElem = elem.querySelector('span')?.textContent.trim();
        return nombreElem === nombre && cantidadElem === cantidad;
    });

    if (existe) {
        let mensajeAlertaMaterial = document.getElementById('dialogCCAlerta');
        mensajeAlertaMaterial.style.display = "flex";
        setTimeout(() => {
            mensajeAlertaMaterial.style.display = "none";
        }, 4000);
        return;
    }

    // Crear el contenedor principal.
    let container = document.createElement('div');
    container.classList.add('seccionMTCasilla');

    // Crear el div para la información.
    let infoDiv = document.createElement('div');
    infoDiv.classList.add('seccionMTValor');

    // Crear y asignar el nombre seleccionado.
    let nameElement = document.createElement('h5');
    nameElement.textContent = nombre;

    // Crear y asignar la cantidad seleccionada.
    let quantityElement = document.createElement('span');
    quantityElement.textContent = cantidad;

    // Agregar elementos al contenedor de información.
    infoDiv.appendChild(nameElement);
    infoDiv.appendChild(quantityElement);

    // Crear y configurar el botón de eliminación.
    let deleteButton = document.createElement('button');
    deleteButton.textContent = 'X';
    deleteButton.onclick = function () {
        container.remove();
    };

    // Agregar todo al contenedor principal.
    container.appendChild(infoDiv);
    container.appendChild(deleteButton);

    // Agregar el nuevo elemento a la secciónMTabla.
    document.querySelector('.seccionMTabla').appendChild(container);

    // Cerrar el diálogo.
    dialogMaterial.close();
}

/*
Abre el diálogo de confirmación para enviar el vale del maestro:
1. Verifica que se haya seleccionado un laboratorio.
2. Comprueba que haya al menos un material agregado.
3. Si hay errores, muestra notificación.
4. Si todo es válido, abre el diálogo de confirmación.
*/
function openDialogEnviarMaestro() {
    // Obtener valores actuales de todos los campos del formulario.
    let laboratorio = document.getElementById('valeSalonInput').value;

    // Obtener lista de materiales agregados.
    let items = document.querySelectorAll(".seccionMTabla .seccionMTCasilla");

    // Validar campos obligatorios vacíos.
    if (laboratorio === '') {
        mostrarNotificacionRequest('Notificación', 'Falta Información', '#1c336c', 'bell');
    }
    else if (items.length === 0) {
        mostrarNotificacionRequest('Notificación', 'No hay Materiales Agregados', '#1c336c', 'bell');
    }
    else {
        dialogEnviar.showModal();
    }
};

/*
Envía la solicitud del maestro al servidor:
1. Recopila el laboratorio y lista de materiales.
2. Prepara los datos en formato para enviar al servidor.
3. Realiza petición POST al endpoint correspondiente.
4. Maneja la respuesta:
   - En caso de error, muestra notificación.
   - En éxito, redirecciona y guarda mensaje en sessionStorage.
*/
function enviarValeMaestro() {
    // Obtener valores de los campos del formulario.
    let laboratorio = document.getElementById('valeSalonInput').value;

    // Obtener todos los items de materiales agregados.
    let items = document.querySelectorAll(".seccionMTabla .seccionMTCasilla");
    let materialList = [];

    // Recorrer cada item para extraer nombre y cantidad.
    items.forEach(item => {
        let name = item.querySelector(".seccionMTValor h5").textContent.trim();
        let quantity = item.querySelector(".seccionMTValor span").textContent.trim();

        materialList.push([name, quantity]);
    });
    
    // Enviar datos al servidor.
    fetch('/maestro/solicitud/enviar', {
        method: 'POST',
        body: JSON.stringify({ laboratorio: laboratorio, items: materialList }),
        headers: { 'Content-Type': 'application/json' }
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