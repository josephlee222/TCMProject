import os
import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from classes.Treatment import Treatment
from forms import searchTreatmentsForm, createTreatmentForm, editTreatmentForm, uploadImageForm
from functions import flashFormErrors, adminAccess, allowedFile

adminTreatments = Blueprint("adminTreatments", __name__)


@adminTreatments.route("/admin/treatments")
@adminAccess
def viewAllTreatments():
    form = searchTreatmentsForm(request.form)

    with shelve.open("treatments") as treatments:
        if len(treatments.keys()) == 0:
            flash("No treatments added yet. Add one by clicking 'Create New Treatment'")

        return render_template("admin/shop/viewTreatments.html", form=form, treatments=treatments)


@adminTreatments.route("/admin/treatments/add", methods=['GET', 'POST'])
@adminAccess
def addTreatment():
    form = createTreatmentForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        description = form.description.data
        benefits = form.benefits.data
        price = form.price.data
        salePrice = form.salePrice.data
        onSale = form.onSale.data
        duration = form.duration.data
        treatment = Treatment(name, description, benefits, price, salePrice, onSale, duration)
        images = request.files.getlist("images")
        bPath = "static/uploads/products/" + str(treatment.getId())
        os.makedirs(bPath)

        for image in images:
            sPath = secure_filename(image.filename)
            if not allowedFile(sPath):
                flash("Unable to create treatment, image file(s) is invalid", category="error")
                return render_template("admin/shop/addTreatment.html", form=form)

            path = os.path.join(bPath, sPath)
            image.save(path)
            treatment.appendImage(path)

        with shelve.open("treatments") as treatments:
            treatments[str(treatment.getId())] = treatment

        flash("Successfully created treatment", category="success")
        return redirect(url_for("adminTreatments.viewAllTreatments"))
    else:
        flashFormErrors("Unable to create the treatment", form.errors)

    return render_template("admin/shop/addTreatment.html", form=form)


@adminTreatments.route("/admin/treatments/edit/<id>", methods=['GET', 'POST'])
@adminAccess
def editTreatment(id):
    form = editTreatmentForm(request.form)
    try:
        with shelve.open("treatments", writeback=True) as treatments:
            treatment = treatments[id]

            if request.method == "POST" and form.validate():
                print("Edit treatment here")
                treatment.setName(form.name.data)
                treatment.setDescription(form.description.data)
                treatment.setBenefits(form.benefits.data)
                treatment.setPrice(form.price.data)
                treatment.setSalePrice(form.salePrice.data)
                treatment.setOnSale(form.onSale.data)
                treatment.setDuration(form.duration.data)

                flash("Successfully edited treatment.", category="success")
                return redirect(url_for("adminTreatments.viewAllTreatments"))
            else:
                flashFormErrors("Unable to edit the treatment", form.errors)

            form.description.data = treatment.getDescription()
            form.benefits.data = treatment.getBenefits()
            form.onSale.data = treatment.getOnSale()

            return render_template("admin/shop/editTreatment.html", treatment=treatment, form=form)
    except KeyError:
        flash("Unable to edit treatment details: treatment does not exist", category="error")
        return redirect(url_for("adminTreatments.viewAllTreatments"))


@adminTreatments.route("/admin/treatments/delete/<id>")
@adminAccess
def deleteTreatment(id):
    try:
        with shelve.open("treatments", writeback=True) as treatments:
            del treatments[id]
            # I used to delete the image files, but that was causing order history images to be missing
            flash("Successfully deleted treatment", category="success")
    except KeyError:
        flash("Unable to delete treatment: treatment does not exist", category="error")

    return redirect(url_for("adminTreatments.viewAllTreatments"))


@adminTreatments.route("/admin/treatments/edit/<id>/images", methods=['GET', 'POST'])
@adminAccess
def editTreatmentImages(id):
    form = uploadImageForm(request.form)
    try:
        with shelve.open("treatments", writeback=True) as treatments:
            treatment = treatments[id]
            if request.method == "POST" and form.validate():
                images = request.files.getlist("images")
                bPath = "static/uploads/products/" + str(treatment.getId())
                print(images)

                for image in images:
                    if image.filename != "":
                        sPath = secure_filename(image.filename)
                        if not allowedFile(sPath):
                            flash("Unable to add images, image file(s) is invalid", category="error")
                            return render_template("admin/shop/editTreatmentImages.html", treatment=treatment, form=form)

                        path = os.path.join(bPath, sPath)
                        image.save(path)
                        treatment.appendImage(path)
                    else:
                        flash("There are no images to upload.", category="warning")
                        return render_template("admin/shop/editTreatmentImages.html", treatment=treatment, form=form)

                flash("Successfully uploaded treatment images.", category="success")
            else:
                flashFormErrors("Unable to edit the treatment images", form.errors)

            return render_template("admin/shop/editTreatmentImages.html", treatment=treatment, form=form)
    except KeyError:
        flash("Unable to edit treatment images: treatment does not exist", category="error")
        return redirect(url_for("adminTreatments.viewAllTreatments"))


@adminTreatments.route("/admin/treatments/edit/<id>/images/delete/<imageId>")
@adminAccess
def deleteTreatmentImage(id, imageId):
    try:
        with shelve.open("treatments", writeback=True) as treatments:
            treatment = treatments[id]
            if len(treatment.getImages()) > 1:
                imgPath = treatment.getImages()[int(imageId)]
                treatment.deleteImage(imageId)
                # I used to delete the image files, but that was causing order history images to be missing
                flash("Image successfully deleted", category="success")
            else:
                flash("Unable to delete the last image. Product should has at least one image", category="error")

            return redirect(url_for("adminTreatments.editTreatmentImages", id=treatment.getId()))

    except KeyError:
        flash("Unable to delete treatment image: treatment does not exist", category="error")
        return redirect(url_for("adminTreatments.viewAllTreatments"))


@adminTreatments.route("/admin/treatments/edit/<id>/images/right/<imageId>")
@adminAccess
def moveTreatmentImageRight(id: int, imageId: int):
    try:
        with shelve.open("treatments", writeback=True) as treatments:
            treatment = treatments[id]
            treatmentImgs = treatment.getImages()
            imageId = int(imageId)
            if len(treatmentImgs) != imageId + 1:
                treatmentImgs[imageId], treatmentImgs[imageId + 1] = treatmentImgs[imageId + 1], treatmentImgs[imageId]

            return redirect(url_for("adminTreatments.editTreatmentImages", id=treatment.getId()))

    except KeyError:
        flash("Unable to edit treatment image: treatment does not exist", category="error")
        return redirect(url_for("adminTreatments.viewAllTreatments"))


@adminTreatments.route("/admin/treatments/edit/<id>/images/left/<imageId>")
@adminAccess
def moveTreatmentImageLeft(id: int, imageId: int):
    try:
        with shelve.open("treatments", writeback=True) as treatments:
            treatment = treatments[id]
            treatmentImgs = treatment.getImages()
            imageId = int(imageId)
            if imageId != 0:
                treatmentImgs[imageId - 1], treatmentImgs[imageId] = treatmentImgs[imageId], treatmentImgs[imageId - 1]

            return redirect(url_for("adminTreatments.editTreatmentImages", id=treatment.getId()))

    except KeyError:
        flash("Unable to edit treatment image: treatment does not exist", category="error")
        return redirect(url_for("adminTreatments.viewAllTreatments"))
