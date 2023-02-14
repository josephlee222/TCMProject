import shelve
from datetime import time, datetime

from flask import flash, Blueprint, render_template, request, session, redirect, url_for

from classes.Appointment import Appointment
from forms import openingHoursForm, createAppointmentForm, searchAppointmentsForm
from functions import flashFormErrors, adminAccess

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
                dict["startTime"] = datetime.combine(dict["date"], dict["time"]).isoformat()
                dict["endTime"] = datetime.combine(dict["date"], dict["endTime"]).isoformat()
                del dict["date"]
                del dict["time"]
                userAppointmentsDict.append(dict)

        if len(appointments.keys()) == 0:
            flash("You do not have any appointments at the moment. Add one by clicking 'Create New Appointment'")

        return render_template("admin/appointments/viewAppointments.html", appointments=appointments, form=form,
                               appointmentsDict=userAppointmentsDict)


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
        endTime = form.endTime.data
        notes = form.notes.data
        appointment = Appointment(name, userEmail, doctorEmail, date, time, endTime, notes)

        with shelve.open("appointments") as appointments:
            appointments[str(appointment.getId())] = appointment

        flash("Successfully created appointment.", category="success")
        return redirect(url_for("adminAppointments.viewAllAppointments"))
    else:
        flashFormErrors("Unable to create the appointment", form.errors)

    with shelve.open("users") as users:
        return render_template("admin/appointments/addAppointment.html", form=form, users=list(users.keys()))


@adminAppointments.route("/admin/appointments/edit/<id>", methods=['GET', 'POST'])
@adminAccess
def editAppointment(id):
    form = createAppointmentForm(request.form)

    try:
        with shelve.open("appointments", writeback=True) as appointments:
            appointment = appointments[id]

            if request.method == "POST" and form.validate():
                print("edit appointment")
                appointment.setName(form.name.data)
                appointment.setDate(form.date.data)
                appointment.setUserEmail(form.userEmail.data)
                appointment.setTime(form.time.data)
                appointment.setEndTime(form.endTime.data)
                appointment.setNotes(form.notes.data)

                flash("Successfully edited appointment.", category="success")
                return redirect(url_for("adminAppointments.viewAppointment", id=id))
            else:
                flashFormErrors("Unable to edit the appointment", form.errors)

            # set form fields
            form.name.data = appointment.getName()
            form.date.data = appointment.getDate()
            form.userEmail.data = appointment.getUserEmail()
            form.time.data = appointment.getTime()
            form.endTime.data = appointment.getEndTime()
            form.notes.data = appointment.getNotes()

            with shelve.open("users") as users:
                return render_template("admin/appointments/editAppointment.html", appointment=appointment, form=form,
                                       users=list(users.keys()))



    except KeyError:
        flash("Unable to edit appointment: appointment does not exist", category="error")
        return redirect(url_for("adminAppointments.viewAllAppointments"))


@adminAppointments.route("/admin/appointments/delete/<id>")
@adminAccess
def deleteAppointment(id):
    try:
        with shelve.open("appointments", writeback=True) as appointments:
            del appointments[id]

        flash("Successfully deleted appointment", category="success")
    except KeyError:
        flash("Unable to delete appointment: appointment does not exist", category="error")

    return redirect(url_for("adminAppointments.viewAllAppointments"))


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
