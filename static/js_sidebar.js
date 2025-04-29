function toggleMenu() {
    let menu = document.getElementById("menuDesplegable");
    menu.classList.toggle("activo");
}

function toggleMenu1() {
    let menu1 = document.getElementById("menuDesplegable1");
    let menu2 = document.getElementById("menuDesplegable2");
    menu1.classList.toggle("activo");
    menu2.classList.remove("activo");
}

function toggleMenu2() {
    let menu1 = document.getElementById("menuDesplegable1");
    let menu2 = document.getElementById("menuDesplegable2");
    menu1.classList.remove("activo");
    menu2.classList.toggle("activo");
}

let sidebar = document.getElementById("sidebar");
let botonMostrar = document.getElementById("mostrarMenuBoton");
let backdrop = document.getElementById("backdrop");

function toggleSidebar() {
    sidebar.classList.toggle("collapsed");
    botonMostrar.classList.toggle("collapsed");

    if (sidebar.classList.contains("collapsed")) {
        backdrop.style.display = "none";
    } else {
        backdrop.style.display = "block";
    }
}

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

ajustarSidebar();

window.addEventListener("resize", ajustarSidebar);

function openDialog() {
    let dialog = document.getElementById("logoutDialog");
    dialog.showModal();
}

function closeDialog() {
    let dialog = document.getElementById("logoutDialog");
    dialog.close();
}

document.addEventListener("DOMContentLoaded", function () {
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
