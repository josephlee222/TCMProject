import shelve

from flask import flash, Blueprint, render_template, redirect, url_for

from functions import normalAccess

treatments = Blueprint("treatments", __name__)


@treatments.route('/treatments/<id>')
@normalAccess
def viewTreatment(id):
    try:
        with shelve.open("treatments") as treatments:
            treatment = treatments[id]
            return render_template("treatment/viewTreatment.html", treatment=treatment)
    except KeyError:
        flash("Sorry! The treatment you are trying to find has been deleted or moved.", category="error")
        return redirect(url_for("home"))


@treatments.route('/treatments')
@normalAccess
def viewTreatments():
    with shelve.open("treatments") as treatments:
        saleTreatments = []
        for treatment in treatments.values():
            if treatment.getOnSale():
                saleTreatments.append(treatment)

        return render_template("treatment/viewTreatments.html", treatments=list(treatments.values()),
                               saleTreatments=saleTreatments)
