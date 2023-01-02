import shelve
from datetime import time
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from forms import openingHoursForm

adminAppointments = Blueprint("adminAppointments", __name__)

# Admin side tracker

@adminAppointments.route("/admin/appointments/openinghours", methods=['GET', 'POST'])
@adminAccess
def editOpeningHours():
    form = openingHoursForm(request.form)

    with shelve.open("data", writeback=True) as data:
        if "opening" not in data or "closing" not in data:
            data["opening"] = time(9, 0, 0)
            data["closing"] = time(21, 0, 0)

        if request.method == "POST" and form.validate():
            print("Update time")
            data["opening"] = form.opening.data
            data["closing"] = form.closing.data
            flash("Opening hours successfully edited.", category="success")
        else:
            flashFormErrors("Unable to edit opening hours", form.errors)

        form.opening.data = data["opening"]
        form.closing.data = data["closing"]

    return render_template("admin/appointments/editOpeningHours.html", form=form)