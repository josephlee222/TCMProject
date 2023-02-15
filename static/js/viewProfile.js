function showDeleteModal(name, link) {
    document.getElementById("delete-treatment-text").innerHTML = "Cancel the appointment '" + decodeURI(name) + "'?"
    document.getElementById("delete-treatment-link").href = link
    var deleteModel = new bootstrap.Modal(document.getElementById("deleteModal"), {});

    deleteModel.show()
}