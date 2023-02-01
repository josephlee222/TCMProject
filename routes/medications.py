from flask import Blueprint

medications = Blueprint("medications", __name__)

# User side medications

import shelve
from datetime import timedelta, date
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
            flash("You are currently not on any medication")

        for tracker in trackers:
            today = date.today()
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
            else:
                flash("There is no medication for today", category="error")
                return redirect(url_for("medications.viewMedications"))

        return render_template("profile/viewMedication.html", morning=morning, afternoon=afternoon, night=night, trackers=trackers)

@medications.route('/profile/yesterdaymedications')
@loginAccess
def yesterdayMedications():

    with shelve.open("users") as users:
        morning = []
        afternoon = []
        night = []
        trackers = users[session["user"]["email"]].getMedications()
        print(trackers)
        if len(trackers) == 0:
            flash("No medication has been prescribed to you currently")

        for tracker in trackers:
            today = date.today() - timedelta(days=int(1))
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
            else:
                flash("There is no medication for today", category="error")
                return redirect(url_for("medications.viewMedications"))

        return render_template("profile/viewyesterdayMedication.html", morning=morning, afternoon=afternoon, night=night, trackers=trackers)
@medications.route('/profile/tomorrowmedications')
@loginAccess
def tommorrowMedications():

    with shelve.open("users") as users:
        morning = []
        afternoon = []
        night = []
        trackers = users[session["user"]["email"]].getMedications()
        print(trackers)
        if len(trackers) == 0:
            flash("No medication currently")

        for tracker in trackers:
            today = date.today() + timedelta(days=int(1))
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
            else:
                flash("There is no medication for today", category="error")
                return redirect(url_for("medications.viewMedications"))

        return render_template("profile/viewtomorrowMedication.html", morning=morning, afternoon=afternoon, night=night, trackers=trackers)
