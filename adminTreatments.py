import os
import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from functions import flashFormErrors, goBack, adminAccess, allowedFile
from forms import searchTreatmentsForm, createTreatmentForm
from classes.Treatment import Treatment


adminTreatments = Blueprint("adminTreatments", __name__)

@adminTreatments.route("/admin/treatments")
@adminAccess
def viewAllTreatments():
    form = searchTreatmentsForm(request.form)

    with shelve.open("treatments") as treatments:
        return render_template("admin/shop/viewTreatments.html", form=form, treatments=treatments)


@adminTreatments.route("/admin/treatments/add", methods=['GET', 'POST'])
@adminAccess
def addTreatment():
    form = createTreatmentForm(request.form)

    if request.method == "POST" and form.validate():
        print("Add treatment here")
        name = form.name.data
        description = form.description.data
        benefits = form.benefits.data
        price = form.price.data
        salePrice = form.salePrice.data
        onSale = form.onSale.data
        duration = form.duration.data
        treatment = Treatment(name, description, benefits, price, salePrice, onSale, [], duration)
        images = request.files.getlist("images")
        bPath = "static/uploads/products/" + str(treatment.getId())
        os.makedirs(bPath)

        for image in images:
            sPath = secure_filename(image.filename)
            path = os.path.join(bPath, sPath)
            image.save(path)
            treatment.appendImage(path)

        with shelve.open("treatments") as treatments:
            treatments[str(treatment.getId())] = treatment

        flash("Successfully created treatment.", category="success")
        return redirect(url_for("adminTreatments.viewAllTreatments"))
    else:
        flashFormErrors("Unable to create the treatment", form.errors)

    return render_template("admin/shop/addTreatment.html", form=form)

@adminTreatments.route("/admin/treatments/edit/<id>", methods=['GET', 'POST'])
@adminAccess
def editTreatment(id):
    form = createTreatmentForm(request.form)
    try:
        with shelve.open("treatments") as treatments:
            treatment = treatments[id]

            form.description.data = treatment.getDescription()
            form.benefits.data = treatment.getBenefits()
            form.onSale.data = treatment.getOnSale()

            if request.method == "POST" and form.validate():
                print("Edit treatment here")

            print(treatment.getImages())
            return render_template("admin/shop/editTreatment.html", treatment=treatment, form=form)
    except KeyError:
        flash("Unable to edit treatment details: treatment does not exist", category="error")
        return redirect(url_for("adminTreatments.viewAllTreatments"))