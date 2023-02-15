function showCancelModal(name, link) {
    document.getElementById("delete-treatment-text").innerHTML = "Cancel order with order ID '" + decodeURIComponent(name) + "'?"
    document.getElementById("delete-treatment-link").href = link
    var deleteModel = new bootstrap.Modal(document.getElementById("deleteModal"), {});

    deleteModel.show()
}

$(document).ready( function () {
    $('#orders').DataTable({
        responsive: true
    });
} );