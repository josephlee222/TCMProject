import shelve

from flask import flash, Blueprint, render_template, redirect, url_for

treatments = Blueprint("treatments", __name__)

@treatments.route('/treatments/<id>')
def viewTreatment(id):
    try:
        with shelve.open("treatments") as treatments:
            treatment = treatments[id]
            return render_template("treatment/viewTreatment.html", treatment=treatment)
    except KeyError:
        flash("Sorry! The treatment you are trying to find has been deleted or moved.", category="error")
        return redirect(url_for("home"), code=404)