// Enable Bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

//Zoom Functions
document.body.style.zoom = localStorage.getItem("zoom") ? localStorage.getItem("zoom") : 1.0

function increaseZoom() {
    if (localStorage.getItem("zoom")) {
        localStorage.setItem("zoom", parseFloat(localStorage.getItem("zoom")) + 0.25)
    } else {
        localStorage.setItem("zoom", 1.25)
    }
    document.body.style.zoom = localStorage.getItem("zoom")
}

function decreaseZoom() {
    if (localStorage.getItem("zoom")) {
        localStorage.setItem("zoom", parseFloat(localStorage.getItem("zoom")) - 0.25)
    } else {
        localStorage.setItem("zoom", 0.75)
    }
    document.body.style.zoom = localStorage.getItem("zoom")
}