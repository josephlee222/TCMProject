function showDeleteModal(name, link) {
    document.getElementById("delete-treatment-text").innerHTML = "Delete appointment '" + name + "'?"
    document.getElementById("delete-treatment-link").href = link
    var deleteModel = new bootstrap.Modal(document.getElementById("deleteModal"), {});

    deleteModel.show()
}