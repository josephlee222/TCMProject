import shelve
from datetime import datetime
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from forms import loginUserForm, registerUserForm
from functions import flashFormErrors, goBack, loginAccess
from classes.User import User

profile = Blueprint("profile", __name__)

@profile.route('/profile', methods=['GET', 'POST'])
@loginAccess
def viewProfile():
    session["previous_url"] = url_for("profile.viewProfile")
    with shelve.open("users") as users, shelve.open("appointments") as appointments:
        user = users[session["user"]["email"]]
        appointmentArray = []
        for id, appointment in appointments.items():
            if appointment.getUserEmail() == session["user"]["email"]:
                appointmentArray.append(appointment)

        return render_template("profile/viewProfile.html", user=user, appointments=appointmentArray)