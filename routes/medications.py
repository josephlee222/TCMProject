from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import loginAccess

medications = Blueprint("medications", __name__)

# User side medications

import shelve
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta, date
from flask import flash, Blueprint, render_template, request, session, redirect, url_for, Response
from forms import editProfileForm
from functions import flashFormErrors, goBack, loginAccess
from classes.User import User


@medications.route('/medication')
@loginAccess
def viewProfile(email):
    session["previous_url"] = url_for("profile.viewProfile")

    with shelve.open("users") as users:
        morning = []
        afternoon = []
        night = []
        trackers = users[email].getMedications()
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

        return render_template("medication/viewMedication.html", trackers=trackers, email=email)

@medications.route('/profile/appointments/export/<id>')
@loginAccess
def exportCalendar(id):
    try:
        with shelve.open("appointments") as appointments:
            appointment = appointments[id]

            if appointment.getUserEmail() == session["user"]["email"]:
                print("Export calendar")
                cal = Calendar()
                event = Event()

                cal.add('prodid', '-//My calendar product//example.com//')
                cal.add('version', '2.0')

                event.add("summary", appointment.getName() + " with " + appointment.getDoctor().getName())
                event.add("description", appointment.getNotes())
                event.add("dtstart", datetime.combine(appointment.getDate(), appointment.getTime()))
                event.add("dtend", datetime.combine(appointment.getDate(), appointment.getEndTime()))

                organizer = vCalAddress("MAILTO:" + appointment.getDoctor().getEmail())
                organizer.params['name'] = vText(appointment.getDoctor().getName())
                organizer.params['role'] = vText('TCM Doctor')
                event["organizer"] = organizer

                attendee = vCalAddress('MAILTO:' + appointment.getUser().getEmail())
                attendee.params['name'] = vText(appointment.getUser().getName())
                attendee.params['role'] = vText('Patient')
                event.add('attendee', attendee, encode=0)

                cal.add_component(event)

                return Response(cal.to_ical(),mimetype="text/calendar", headers={"Content-disposition":"attachment; filename=appointment.ics"})
            else:
                flash("Unable to export event, appointment is not assigned to your account", category="error")
                return redirect(url_for("profile.viewProfile"), code=401)
    except KeyError:
        flash("Unable to export calendar, appointment does not exist.", category="error")
        return redirect(url_for("profile.viewProfile"), code=404)
