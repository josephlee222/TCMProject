import shelve
from datetime import time, datetime
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from forms import openingHoursForm, createAppointmentForm, searchAppointmentsForm
from classes.Appointment import Appointment

adminAppointments = Blueprint("adminAppointments", __name__)

@adminAppointments.route("/admin/appointments/", methods=['GET', 'POST'])
@adminAccess
def viewAllAppointments():
    form = searchAppointmentsForm(request.form)

    # This code is shit but it works
    with shelve.open("appointments") as appointments:
        userAppointments = {}
        userAppointmentsDict = []
        for appointment in appointments:
            if appointments[appointment].getDoctorEmail() == session["user"]["email"]:
                dict = appointments[appointment].__dict__
                dict["datetime"] = datetime.combine(dict["date"], dict["time"]).isoformat()
                del dict["date"]
                del dict["time"]
                userAppointmentsDict.append(dict)


        if len(appointments.keys()) == 0:
            flash("You do not have any appointments at the moment. Add one by clicking 'Create New Appointment'")

        return render_template("admin/appointments/viewAppointments.html", appointments=appointments, form=form, appointmentsDict=userAppointmentsDict)


@adminAppointments.route("/admin/appointments/details/<id>", methods=['GET', 'POST'])
@adminAccess
def viewAppointment(id):
    try:
        with shelve.open("appointments") as appointments:
            appointment = appointments[id]

            return render_template("admin/appointments/viewAppointment.html", appointment=appointment)

    except KeyError:
        flash("Unable to view appointment details: appointment does not exist", category="error")
        return redirect(url_for("adminAppointments.viewAllAppointments"))


@adminAppointments.route("/admin/appointments/add", methods=['GET', 'POST'])
@adminAccess
def addAppointment():
    form = createAppointmentForm(request.form)
    if request.method == "POST" and form.validate():
        print("Create appointment")
        name = form.name.data
        userEmail = form.userEmail.data
        doctorEmail = session["user"]["email"]
        date = form.date.data
        time = form.time.data
        notes = form.notes.data
        appointment = Appointment(name, userEmail, doctorEmail, date, time, notes)

        with shelve.open("appointments") as appointments:
            appointments[str(appointment.getId())] = appointment

        flash("Successfully created appointment.", category="success")
        return redirect(url_for("adminAppointments.viewAllAppointments"))
    else:
        flashFormErrors("Unable to create the appointment", form.errors)

    with shelve.open("users") as users:
        return render_template("admin/appointments/addAppointment.html", form=form, users=list(users.keys()))



# Admin side medications

@adminAppointments.route("/admin/appointments/openinghours", methods=['GET', 'POST'])
@adminAccess
def editOpeningHours():
    form = openingHoursForm(request.form)

    with shelve.open("data", writeback=True) as data:
        if "opening" not in data or "closing" not in data:
            data["opening"] = time(9, 0, 0)
            data["closing"] = time(21, 0, 0)

        if request.method == "POST" and form.validate():
            data["opening"] = form.opening.data
            data["closing"] = form.closing.data
            flash("Opening hours successfully edited.", category="success")
        else:
            flashFormErrors("Unable to edit opening hours", form.errors)

        form.opening.data = data["opening"]
        form.closing.data = data["closing"]

    return render_template("admin/appointments/editOpeningHours.html", form=form)
