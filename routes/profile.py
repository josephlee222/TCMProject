import shelve
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from flask import flash, Blueprint, render_template, request, session, redirect, url_for, Response
from forms import editProfileForm
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
            if appointment.getUserEmail() == session["user"]["email"] and appointment.getDate() > datetime.now().date():
                appointmentArray.append(appointment)

    return render_template("profile/viewProfile.html", user=user, appointments=appointmentArray)

@profile.route('/profile/edit', methods=['GET', 'POST'])
@loginAccess
def editProfile():
    form = editProfileForm(request.form)

    with shelve.open("users", writeback=True) as users:
        user = users[session["user"]["email"]]

        if request.method == "POST" and form.validate():
            print("Update profile")
            user.setName(form.name.data)
            user.setBirthday(form.birthday.data)
            user.setPhone(form.phone.data)

            flash("Your profile has been updated successfully!", category="success")
            return redirect(url_for("profile.viewProfile"))
        else:
            flashFormErrors("Unable to update your profile", form.errors)

        form.name.data = user.getName()
        form.birthday.data = user.getBirthday()
        form.phone.data = user.getPhone()
        return render_template("profile/editProfile.html", form=form, user=user)




@profile.route('/profile/appointments/export/<id>', methods=['GET', 'POST'])
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
        flash("Unable to export calendar, appointment does not exist.")
        return redirect(url_for("profile.viewProfile"), code=404)