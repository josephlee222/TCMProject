import shelve
from datetime import datetime
from flask import flash, Blueprint, render_template, request, session, redirect, url_for, Response
from forms import editProfileForm
from functions import flashFormErrors, goBack, loginAccess
from classes.User import User

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