function showDeleteModal(name, link) {
    document.getElementById("delete-treatment-text").innerHTML = "Delete treatment '" + decodeURIComponent(name) + "'?"
    document.getElementById("delete-treatment-link").href = link
    var deleteModel = new bootstrap.Modal(document.getElementById("deleteModal"), {});

    deleteModel.show()
}