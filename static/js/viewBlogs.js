function showDeleteModal(name, link) {
    document.getElementById("delete-treatment-text").innerHTML = "Delete blog article '" + decodeURIComponent(name) + "'?"
    document.getElementById("delete-treatment-link").href = link
    var deleteModel = new bootstrap.Modal(document.getElementById("deleteModal"), {});

    deleteModel.show()
}

$(document).ready( function () {
    $('#blogs').DataTable({
        responsive: true
    });
} );