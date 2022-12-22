// Enable Bootstrap tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

//Zoom Functions (DOES NOT WORK PROPERLY ON FIREFOX)
document.body.style.zoom = localStorage.getItem("zoom") ? localStorage.getItem("zoom") : 1.0

function increaseZoom() {
    if (localStorage.getItem("zoom")) {
        localStorage.setItem("zoom", parseFloat(localStorage.getItem("zoom")) + 0.05)
    } else {
        localStorage.setItem("zoom", 1.05)
    }
    document.body.style.zoom = localStorage.getItem("zoom")
    document.body.style["-moz-transform"] = "scale(" + localStorage.getItem("zoom") + ")"
}

function decreaseZoom() {
    if (localStorage.getItem("zoom")) {
        localStorage.setItem("zoom", parseFloat(localStorage.getItem("zoom")) - 0.05)
    } else {
        localStorage.setItem("zoom", 0.95)
    }
    document.body.style.zoom = localStorage.getItem("zoom")
    document.body.style["-moz-transform"] = "scale(" + localStorage.getItem("zoom") + ")"
}

function resetZoom() {
    localStorage.setItem("zoom", 1.0)
    document.body.style.zoom = localStorage.getItem("zoom")
    document.body.style["-moz-transform"] = "scale(1)"
}