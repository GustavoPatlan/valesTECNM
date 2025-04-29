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

    // Crear el contenedor principal
    let container = document.createElement('div');
    container.classList.add('seccionMTCasilla');

    // Crear el div para la información
    let infoDiv = document.createElement('div');
    infoDiv.classList.add('seccionMTValor');

    let nameElement = document.createElement('h5');
    nameElement.textContent = nombre;

    let quantityElement = document.createElement('span');
    quantityElement.textContent = cantidad;

    infoDiv.appendChild(nameElement);
    infoDiv.appendChild(quantityElement);

    let deleteButton = document.createElement('button');
    deleteButton.textContent = 'X';
    deleteButton.onclick = function () {
        container.remove();
    };

    container.appendChild(infoDiv);
    container.appendChild(deleteButton);

    document.querySelector('.seccionMTabla').appendChild(container);
    dialogMaterial.close();
}

function openDialogEnviarMaestro() {
    let laboratorio = document.getElementById('valeSalonInput').value;
    let items = document.querySelectorAll(".seccionMTabla .seccionMTCasilla");

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

function enviarValeMaestro() {
    let laboratorio = document.getElementById('valeSalonInput').value;
    let items = document.querySelectorAll(".seccionMTabla .seccionMTCasilla");

    let materialList = [];
    items.forEach(item => {
        let name = item.querySelector(".seccionMTValor h5").textContent.trim();
        let quantity = item.querySelector(".seccionMTValor span").textContent.trim();

        materialList.push([name, quantity]);
    });
    
    fetch('/maestro/solicitud/enviar', {
        method: 'POST',
        body: JSON.stringify({ laboratorio: laboratorio, items: materialList }),
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            switch (data.status) {
                case 'error':
                    mostrarNotificacionRequest('Error', data.mensaje, 'crimson', 'bug');
                    break;
                case 'redirect':
                    sessionStorage.setItem("notificacion_mensaje", data.mensaje);
                    window.location.href = data.url;
                    break;
            };
        });
};