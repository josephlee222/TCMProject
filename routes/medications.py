from flask import Blueprint

medications = Blueprint("medications", __name__)

# User side medications

import shelve
from datetime import timedelta
from flask import flash, render_template, session, redirect, url_for
from functions import loginAccess


@medications.route('/profile/medications')
@loginAccess
def viewMedications():

    with shelve.open("users") as users:
        morning = []
        afternoon = []
        night = []
        trackers = users[session["user"]["email"]].getMedications()
        print(trackers)
        if len(trackers) == 0:
            flash("No medication currently'")

        for tracker in trackers:
            date = date.today()
            list = []
            for i in range(tracker.getDuration_of_medication()):
                list.append(tracker.getdate() + timedelta(days=int(i)))
            if date not in list:
                flash("There is no medication for today", category="error")
                return redirect(url_for("profile.viewProfile"), code=401)
            else:
                if tracker.getFrequency_of_pills() == 1:
                    morning.append(tracker)
                elif tracker.getFrequency_of_pills() == 2:
                    morning.append(tracker)
                    night.append(tracker)
                elif tracker.getFrequency_of_pills() == 3:
                    morning.append(tracker)
                    afternoon.append(tracker)
                    night.append(tracker)

        return render_template("profile/viewMedication.html", trackers=trackers, email=email)
