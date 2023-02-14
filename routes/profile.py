import shelve
from datetime import datetime, timedelta, time

from flask import flash, Blueprint, render_template, request, session, redirect, url_for, Response
from icalendar import Calendar, Event, vCalAddress, vText

from classes.Address import Address
from classes.Appointment import Appointment
from forms import editProfileForm, addAddressForm, editAddressForm, bookAppointmentForm
from functions import flashFormErrors, loginAccess, convertHoursToTime

profile = Blueprint("profile", __name__)


@profile.route('/profile')
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


@profile.route('/profile/appointments/')
@loginAccess
def viewAppointments():
    with shelve.open("appointments") as appointments:
        appointmentArray = []
        for id, appointment in appointments.items():
            if appointment.getUserEmail() == session["user"]["email"] and appointment.getDate() > datetime.now().date():
                appointmentArray.append(appointment)

    return render_template("profile/viewAppointments.html", appointments=appointmentArray)


@profile.route('/profile/appointments/delete/<id>')
@loginAccess
def cancelAppointment(id):
    try:
        with shelve.open("appointments", writeback=True) as appointments:
            if appointments[id].getUser().getEmail() == session["user"]["email"]:
                del appointments[id]

                flash("The appointment has been cancelled", category="success")
                return redirect(url_for("profile.viewProfile"))
            else:
                flash("Unable to cancel the appointment.", category="error")
                return redirect(url_for("profile.viewProfile"), code=401)
    except KeyError:
        flash("Unable to cancel your appointment, appointment does not exist.", category="error")
        return redirect(url_for("profile.viewProfile"), code=404)


@profile.route('/profile/appointments/export/')
@loginAccess
def exportAllCalendar():
    with shelve.open("appointments") as appointments:
        appointmentArray = []
        for id, appointment in appointments.items():
            if appointment.getUserEmail() == session["user"]["email"] and appointment.getDate() > datetime.now().date():
                appointmentArray.append(appointment)

        if len(appointmentArray) != 0:
            cal = Calendar()
            cal.add('prodid', '-//My calendar product//example.com//')
            cal.add('version', '2.0')
            for appointment in appointmentArray:
                event = Event()

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

            return Response(cal.to_ical(), mimetype="text/calendar",
                            headers={"Content-disposition": "attachment; filename=appointment.ics"})
        else:
            flash("Unable to export calendar, No appointments available to export with this account.", category="error")
            return redirect(url_for("profile.viewProfile"), code=404)


@profile.route('/profile/appointments/export/<id>')
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

                return Response(cal.to_ical(), mimetype="text/calendar",
                                headers={"Content-disposition": "attachment; filename=appointment.ics"})
            else:
                flash("Unable to export event, appointment is not assigned to your account", category="error")
                return redirect(url_for("profile.viewProfile"), code=401)
    except KeyError:
        flash("Unable to export calendar, appointment does not exist.", category="error")
        return redirect(url_for("profile.viewProfile"), code=404)


@profile.route('/profile/orders')
@loginAccess
def viewOrderHistory():
    with shelve.open("orders") as orders:
        order = []

        for item in orders.values():
            if item.getUserId() == session["user"]["email"]:
                order.append(item)

    order.reverse()

    return render_template("profile/viewOrderHistory.html", orders=order)


@profile.route('/profile/orders/<id>')
@loginAccess
def viewOrderHistoryDetails(id):
    try:
        with shelve.open("orders") as orders:
            order = orders[id]

        if order.getUserId() != session["user"]["email"]:
            flash("Unable to view your order, the order is not associated with your account", category="error")
            return redirect(url_for("profile.viewOrderHistory"))

        if order.getStatus() == 1:
            statusDescription = "Your order has been received by the clinic and its being prepared."
        elif order.getStatus() == 2:
            statusDescription = "Your order has been prepared and its awaiting delivery."
        elif order.getStatus() == 3:
            statusDescription = "Your order has been collected by our delivery partner and its being delivered."
        elif order.getStatus() == 4:
            statusDescription = "Your order has been delivered to the specified address. For enquires, contact the clinic directly."
        elif order.getStatus() == 5:
            statusDescription = "Your order has been cancelled and will not be delivered. Contact the clinic for refunds."
        elif order.getStatus() == 6:
            statusDescription = "Your order has been refunded by TCM Shifu. Contact us for more details."
        else:
            statusDescription = "Unknown delivery status. Please contact the clinic for details."

        return render_template("profile/viewOrderHistoryDetails.html", order=order, statusDescription=statusDescription)
    except KeyError:
        flash("Unable to view your order, order does not exist", category="error")
        return redirect(url_for("profile.viewOrderHistory"))


@profile.route('/profile/orders/<id>/book/<itemId>', methods=['GET', 'POST'])
@loginAccess
def bookAppointment(id, itemId):
    form = bookAppointmentForm(request.form)
    try:
        with shelve.open("orders") as orders:
            order = orders[id]
            item = order.getCart()[int(itemId)]

        if order.getUserId() != session["user"]["email"]:
            flash("Unable to book appointment, the order is not associated with your account", category="error")
            return redirect(url_for("profile.viewOrderHistory"))

        if order.getStatus() == 5 or order.getStatus() == 6:
            flash("Unable to book appointment, the order is cancelled or refunded", category="error")
            return redirect(url_for("profile.viewOrderHistory"))

        if item.getType() != "treatments":
            flash("Unable to make a appointment with this item as it is not a treatment.")
            return redirect(url_for("profile.viewOrderHistoryDetails", id=id))
        elif item.isConsumed():
            flash("Unable to make a appointment as this treatment has already been used.")
            return redirect(url_for("profile.viewOrderHistoryDetails", id=id))

        with shelve.open("users") as users:
            # Get a list of doctors via for loop, I know this is not the best method and will have a performance impact if the userbase gets larger
            # It's a solution I can think of at the moment with the current method of storing users
            doctorList = []
            for user in users.values():
                if user.getAccountType() == "admin":
                    doctorList.append((user.getEmail(), user.getName()))

            form.doctor.choices = doctorList

        if request.method == "POST" and form.validate():
            print("Under construction")
            name = item.getStoredItem().getName()
            userEmail = session["user"]["email"]
            doctorEmail = form.doctor.data
            date = form.date.data
            startTime = form.startTime.data
            endTime = datetime.combine(date.today(), startTime) + convertHoursToTime(item.getStoredItem().getDuration())

            appointment = Appointment(name, userEmail, doctorEmail, date, startTime, endTime.time(),
                                      "Booked automatically via website")
            with shelve.open("appointments") as appointments:
                appointments[str(appointment.getId())] = appointment

            with shelve.open("orders", writeback=True) as orders:
                order = orders[id]
                item = order.getCart()[int(itemId)]
                item.consumeCart()

            flash("Appointment has been successfully booked, see you there!", category="success")
            return redirect(url_for("profile.viewOrderHistoryDetails", id=id))
        else:
            flashFormErrors("Unable to book an appointment", form.errors)

        return render_template("profile/bookAppointment.html", order=order, item=item, form=form)
    except KeyError:
        flash("Unable to view your order, order does not exist", category="error")
        return redirect(url_for("profile.viewOrderHistory"))


@profile.route('/profile/address')
@loginAccess
def viewAddresses():
    try:
        with shelve.open("users") as users:
            addresses = users[session["user"]["email"]].getAddress()

        return render_template("profile/viewAddresses.html", addresses=addresses)
    except KeyError:
        flash("Unable to get your delivery addresses", category="error")
        return redirect(url_for("profile.viewProfile"))


@profile.route('/profile/address/add', methods=['GET', 'POST'])
@loginAccess
def addAddress():
    form = addAddressForm(request.form)

    if request.method == "POST" and form.validate():
        print("Add Address Here")
        try:
            with shelve.open("users", writeback=True) as users:
                user = users[session["user"]["email"]]

                address = Address(form.name.data, form.location.data)
                if address.getLatitude() is not None and address.getLongitude() is not None:
                    user.setAddress(address)
                    flash("Your new address has been added to your account", category="success")
                    return redirect(url_for("profile.viewAddresses"))
                else:
                    flash("Unable to add address because our location provider could not find your address.",
                          category="error")
        except Exception as e:
            flash("Unable to add delivery address", category="error")

    return render_template("profile/addAddress.html", form=form)


@profile.route('/profile/address/delete/<id>', methods=['GET', 'POST'])
@loginAccess
def deleteAddress(id):
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[session["user"]["email"]]
            if user.deleteAddress(id):
                flash("Your saved address has been deleted", category="success")
            else:
                flash("Unable to delete delivery address: Delivery address does not exist", category="error")
    except KeyError:
        flash("Unable to delete delivery address: Account or delivery address does not exist", category="error")

    return redirect(url_for("profile.viewAddresses"))


@profile.route('/profile/address/edit/<id>', methods=['GET', 'POST'])
@loginAccess
def editAddress(id):
    form = editAddressForm(request.form)
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[session["user"]["email"]]

            if request.method == "POST" and form.validate():
                address = Address(form.name.data, form.location.data)
                if address.getLatitude() is not None and address.getLongitude() is not None:
                    user.editAddress(int(id), address)
                    flash("Address has been successfully edited", category="success")
                    return redirect(url_for("profile.viewAddresses"))
                else:
                    flash("Unable to edit your address because our location provider could not find your address.",
                          category="error")
            else:
                flashFormErrors("Unable to edit address", form.errors)

            if user.getAddress() is not None:
                try:
                    address = user.getAddress()[int(id)]
                    form.name.data = address.getName()
                    form.location.data = address.getLocation()
                    return render_template("profile/editAddress.html", form=form)
                except IndexError:
                    flash("Cannot edit address. Specified address ID does not exist.", category="error")
                    return redirect(url_for("profile.viewAddresses"))
            else:
                flash("Cannot edit address. No address has been added yet", category="error")
                return redirect(url_for("profile.viewAddresses"))

    except KeyError:
        flash("Unable to delete delivery address: Account or delivery address does not exist", category="error")
        return redirect(url_for("profile.viewAddresses"))


@profile.route('/profile/medications/export/')
@loginAccess
def exportMedicationCalendar():
    try:
        cal = Calendar()
        cal.add('prodid', '-//My calendar product//example.com//')
        cal.add('version', '2.0')
        with shelve.open("users") as users:
            medicationArray = []
            medications = users[session["user"]["email"]].getMedications()
            for medication in medications:
                if medication.getEnddate() > datetime.now().date():
                    medicationArray.append(medication)

            for medication in medicationArray:
                day = medication.getEnddate() - datetime.now().date()
                medication_days_left = day.days
                for i in range(int(medication_days_left)):
                    if medication.getFrequency_of_pills() == "1":
                        # MORNING
                        event = Event()
                        event.add("summary", "Take " + medication.getName() + " at 9:00AM")
                        event.add("description", 'Medication Description: ' + medication.getDescription())
                        event.add("dtstart", datetime.combine(datetime.now().date() + timedelta(i), time(9, 0, 0)))
                        event.add("dtend", datetime.combine(datetime.now().date() + timedelta(i), time(10, 0, 0)))
                        event.add('uid', medication.getName() + str(
                            datetime.combine(datetime.now().date() + day + timedelta(i), time(9, 0, 0))) + ' MORNING')
                        cal.add_component(event)
                    elif medication.getFrequency_of_pills() == "2":
                        # MORNING
                        event = Event()
                        event.add("summary", "Take " + medication.getName() + " at 9:00AM")
                        event.add("description", 'Medication Description: ' + medication.getDescription())
                        event.add("dtstart", datetime.combine(datetime.now().date() + timedelta(i), time(9, 0, 0)))
                        event.add("dtend", datetime.combine(datetime.now().date() + timedelta(i), time(10, 0, 0)))
                        event.add('uid', medication.getName() + str(
                            datetime.combine(datetime.now().date() + day + timedelta(i), time(9, 0, 0))) + ' MORNING')
                        cal.add_component(event)
                        # NIGHT
                        event = Event()
                        event.add("summary", "Take " + medication.getName() + " at 6:00PM")
                        event.add("description", 'Medication Description: ' + medication.getDescription())
                        event.add("dtstart",
                                  datetime.combine(datetime.now().date() + timedelta(i), time(18, 0, 0)))
                        event.add("dtend", datetime.combine(datetime.now().date() + timedelta(i), time(19, 0, 0)))
                        event.add('uid', medication.getName() + str(
                            datetime.combine(datetime.now().date() + day + timedelta(i), time(18, 0, 0))) + ' NIGHT')
                        cal.add_component(event)
                    elif medication.getFrequency_of_pills() == "3":
                        # MORNING
                        event = Event()
                        event.add("summary", "Take " + medication.getName() + " at 9:00AM")
                        event.add("description", 'Medication Description: ' + medication.getDescription())
                        event.add("dtstart", datetime.combine(datetime.now().date() + timedelta(i), time(9, 0, 0)))
                        event.add("dtend", datetime.combine(datetime.now().date() + timedelta(i), time(10, 0, 0)))
                        event.add('uid', medication.getName() + str(
                            datetime.combine(datetime.now().date() + day + timedelta(i), time(9, 0, 0))) + ' MORNING')
                        cal.add_component(event)
                        # AFTERNOON
                        event = Event()
                        event.add("summary", "Take " + medication.getName() + " at 12:00PM")
                        event.add("description", 'Medication Description: ' + medication.getDescription())
                        event.add("dtstart",
                                  datetime.combine(medication.getDate() + timedelta(i), time(12, 0, 0)))
                        event.add("dtend", datetime.combine(datetime.now().date() + timedelta(i), time(13, 0, 0)))
                        event.add('uid', medication.getName() + str(
                            datetime.combine(datetime.now().date() + day + timedelta(i),
                                             time(12, 0, 0))) + ' AFTERNOON')
                        cal.add_component(event)
                        # NIGHT
                        event = Event()
                        event.add("summary", "Take " + medication.getName() + " at 6:00PM")
                        event.add("description", 'Medication Description: ' + medication.getDescription())
                        event.add("dtstart",
                                  datetime.combine(datetime.now().date() + timedelta(i), time(18, 0, 0)))
                        event.add("dtend", datetime.combine(datetime.now().date() + timedelta(i), time(19, 0, 0)))
                        event.add('uid', medication.getName() + str(
                            datetime.combine(datetime.now().date() + day + timedelta(i), time(18, 0, 0))) + ' NIGHT')
                        cal.add_component(event)

            return Response(cal.to_ical(), mimetype="text/calendar",
                            headers={"Content-disposition": "attachment; filename=medications.ics"})
    except KeyError:
        flash("Unable to export calendar, No appointments available to export with this account.", category="error")
        return redirect(url_for("profile.viewProfile"), code=404)
