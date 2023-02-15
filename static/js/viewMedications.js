function showDeleteModal(name, link) {
    document.getElementById("delete-treatment-text").innerHTML = "Delete medication '" + decodeURIComponent(name) + "'?"
    document.getElementById("delete-treatment-link").href = link
    var deleteModel = new bootstrap.Modal(document.getElementById("deleteModal"), {});

    deleteModel.show()
}

$(document).ready( function () {
    $('#medications').DataTable({
        responsive: true
    });
} );