import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from forms import searchTreatmentsForm


adminTreatments = Blueprint("adminTreatments", __name__)

@adminTreatments.route("/admin/treatments")
def viewAllTreatments():
    form = searchTreatmentsForm(request.form)

    with shelve.open("treatments") as treatments:
        return render_template("admin/shop/viewTreatments.html", form=form)