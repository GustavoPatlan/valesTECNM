/*
Controla la visualización del menú desplegable de vales de estudiantes.
Alterna la clase 'activo' que muestra/oculta el submenú.
*/
function toggleMenu1() {
    let menu1 = document.getElementById("menuDesplegable1");
    let menu2 = document.getElementById("menuDesplegable2");
    menu1.classList.toggle("activo");
    menu2.classList.remove("activo");
}

/*
Controla la visualización del menú desplegable de vales personales.
Alterna la clase 'activo' que muestra/oculta el submenú.
*/
function toggleMenu2() {
    let menu1 = document.getElementById("menuDesplegable1");
    let menu2 = document.getElementById("menuDesplegable2");
    menu1.classList.remove("activo");
    menu2.classList.toggle("activo");
}

/*
Alterna el estado del sidebar (expandido/colapsado).
 - Aplica estilos al sidebar y botón de control.
 - Controla la capa de fondo (backdrop).
*/
let sidebar = document.getElementById("sidebar");
let botonMostrar = document.getElementById("mostrarMenuBoton");
let backdrop = document.getElementById("backdrop");

function toggleSidebar() {
    sidebar.classList.toggle("collapsed");
    botonMostrar.classList.toggle("collapsed");

    // Mostrar/ocultar backdrop según estado.
    if (sidebar.classList.contains("collapsed")) {
        backdrop.style.display = "none";
    } else {
        backdrop.style.display = "block";
    }
}

/*
Ajusta el sidebar según el tamaño de pantalla.
 - Colapsa automáticamente en pantallas.
 - Muestra backdrop solo en versión expandida.
*/
function ajustarSidebar() {
    if (window.innerWidth <= 900) {
        sidebar.classList.add("collapsed");
        backdrop.style.display = "none";
        botonMostrar.classList.add("collapsed");
    } else {
        sidebar.classList.remove("collapsed");
        backdrop.style.display = "block";
        botonMostrar.classList.remove("collapsed");
    }
}

/*
Configuración inicial.
*/
ajustarSidebar();

/*
Cambios de tamaño de ventana.
*/
window.addEventListener("resize", ajustarSidebar);

/*
Muestra el diálogo de confirmación para cerrar sesión.
*/
function openDialog() {
    let dialog = document.getElementById("logoutDialog");
    dialog.showModal();
}

/*
Cierra el diálogo de confirmación.
*/
function closeDialog() {
    let dialog = document.getElementById("logoutDialog");
    dialog.close();
}

// Al cargar la página.
document.addEventListener("DOMContentLoaded", function () {

    // Marcar como activo el enlace correspondiente a la ruta actual.
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll(".li_link");

    links.forEach(link => {
        const pathsAttr = link.getAttribute("data-path");

        if (pathsAttr) {
            const paths = pathsAttr.split(',');
            if (paths.includes(currentPath)) {
                link.classList.add("active");
            }
        }
    });
});