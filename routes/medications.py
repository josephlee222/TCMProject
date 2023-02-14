from flask import Blueprint

medications = Blueprint("medications", __name__)

# User side medications

import shelve
from datetime import timedelta, date
from flask import flash, render_template, session
from functions import loginAccess


@medications.route('/profile/medications')
@medications.route('/profile/medications/<day>')
@loginAccess
def viewMedications(day=0):
    day = int(day)
    today = date.today() + timedelta(days=int(day))
    with shelve.open("users") as users:
        morning = []
        afternoon = []
        night = []
        medications = users[session["user"]["email"]].getMedications()
        if len(medications) == 0:
            flash("You are currently not on any medication")

        for tracker in medications:
            list = []
            for i in range(int(tracker.getDuration_of_medication())):
                list.append(tracker.getDate() + timedelta(days=int(i)))

            if today in list:
                if tracker.getFrequency_of_pills() == "1":
                    morning.append(tracker)
                elif tracker.getFrequency_of_pills() == "2":
                    morning.append(tracker)
                    night.append(tracker)
                elif tracker.getFrequency_of_pills() == "3":
                    morning.append(tracker)
                    afternoon.append(tracker)
                    night.append(tracker)

        return render_template("profile/viewMedication.html", morning=morning, afternoon=afternoon, night=night,
                               medications=medications, date=today, day=day)
