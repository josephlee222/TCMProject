import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for

from classes.Medications import Medication
from forms import createMedicationForm, editMedicationForm, searchTracker
from functions import flashFormErrors, adminAccess

adminTrackers = Blueprint("adminTrackers", __name__)


# Admin side medications
@adminTrackers.route("/admin/trackers/<email>")
@adminAccess
def viewAllTrackers(email):
    form = searchTracker(request.form)

    with shelve.open("users") as users:
        trackers = users[email].getMedications()
        if len(trackers) == 0:
            flash("No medications added yet. Add one by clicking 'Create Medication'")

        return render_template("admin/medications/viewMedication.html", form=form, trackers=trackers, email=email)


@adminTrackers.route("/admin/trackers/add/<email>", methods=['GET', 'POST'])
@adminAccess
def addTracker(email):
    form = createMedicationForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        description = form.description.data
        duration = form.duration.data
        pills = form.pills.data
        frequency_of_pills = form.frequency_of_pills.data
        additional_notes = form.additional_notes.data
        tracker = Medication(name, description, duration, pills, frequency_of_pills, additional_notes)

        with shelve.open("users", writeback=True) as users:
            users[email].setMedication(tracker)

        flash("Successfully created the medication.", category="success")
        return redirect(url_for("adminTrackers.viewAllTrackers", email=email))
    else:
        flashFormErrors("Unable to create the medication", form.errors)

    return render_template("admin/medications/addMedication.html", form=form, email=email)


@adminTrackers.route("/admin/trackers/edit/<email>/<id>", methods=['GET', 'POST'])
@adminAccess
def editTracker(email, id):
    form = editMedicationForm(request.form)
    try:
        with shelve.open("users", writeback=True) as users:
            medication = users[email].getMedications()[int(id)]

            if request.method == "POST" and form.validate():
                print("Edit treatment here")
                medication.setName(form.name.data)
                medication.setDescription(form.description.data)
                medication.setDuration_of_medication(form.duration.data)
                medication.setFrequency_of_pills(form.frequency_of_pills.data)
                medication.setNo_of_pills(form.pills.data)
                medication.setNotes(form.additional_notes.data)

                flash("Successfully edited medication.", category="success")
                return redirect(url_for("adminTrackers.viewAllTrackers", email=email))
            else:
                flashFormErrors("Unable to edit the treatment", form.errors)

            form.name.data = medication.getName()
            form.description.data = medication.getDescription()
            form.duration.data = medication.getDuration_of_medication()
            form.pills.data = medication.getNo_of_pills()
            form.frequency_of_pills.data = medication.getFrequency_of_pills()
            form.additional_notes.data = medication.getNotes()

            return render_template("admin/medications/editMedication.html", medication=medication, form=form,
                                   email=email)
    except KeyError:
        flash("Unable to edit treatment details: treatment does not exist", category="error")
        return redirect(url_for("adminTrackers.viewAllTrackers", email=email))


@adminTrackers.route("/admin/trackers/view/<email>/<id>", methods=['GET'])
@adminAccess
def viewTracker(email, id):
    form = searchTracker(request.form)

    with shelve.open("users") as users:
        trackers = users[email].getMedications()[int(id)]

        return render_template("admin/medications/viewspecificMedication.html", form=form, trackers=trackers,
                               email=email, id=id)


@adminTrackers.route("/admin/trackers/delete/<email>/<id>")
@adminAccess
def deleteTracker(email, id):
    try:
        with shelve.open("users", writeback=True) as users:

            users[email].deleteMedication(id)

            flash("Successfully deleted medication", category="success")
    except KeyError:
        flash("Unable to delete medication: medication does not exist", category="error")

    return redirect(url_for("adminTrackers.viewAllTrackers", email=email))
