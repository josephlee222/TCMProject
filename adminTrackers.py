import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from forms import createTracker, editTracker, searchTracker
from classes.Tracker import Tracker

adminTrackers = Blueprint("adminTrackers", __name__)


# Admin side tracker

@adminTrackers.route("/admin/trackers/", methods=['GET', 'POST'])
@adminAccess
def viewAllTrackers():
    print("Put your render template here")


@adminTrackers.route("/admin/trackers/")
@adminAccess
def viewAllTracker():
    form = searchTracker(request.form)

    with shelve.open("trackers") as trackers:
        if len(trackers.keys()) == 0:
            flash("No medication added yet. Add one by clicking 'Create New Medication'")

        return render_template("admin/shop/viewTreatments.html", form=form, trackers=trackers)


@adminTrackers.route("/admin/trackers/add")
@adminAccess
def addTracker():
    form = createTracker(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        description = form.description.data
        duration = form.duration.data
        pills = form.pills.data
        frequency_of_pills = form.frequency_of_pills.data
        additional_notes = form.additional_notes.data
        tracker = Tracker(name, description, duration, pills, frequency_of_pills, additional_notes)

        with shelve.open("trackers") as trackers:
            trackers[str(tracker.getId())] = tracker

        flash("Successfully created one medication.", category="success")
        return redirect(url_for("adminTracker.addTreatment"))
    else:
        flashFormErrors("Unable to create the medication", form.errors)

    return render_template("admin/shop/addTreatment.html", form=form)


@adminTrackers.route("/admin/trackers/edit/<id>")
@adminAccess
def editTracker(id):
    form = editTracker(request.form)
    try:
        with shelve.open("trackers", writeback=True) as trackers:
            tracker = trackers[id]

            if request.method == "POST" and form.validate():
                print("Edit treatment here")
                Tracker.setName(form.name.data)
                Tracker.setDescription(form.description.data)
                Tracker.setDuration_of_medication(form.duration.data)
                Tracker.setFrequency_of_pills(form.pills.data)
                Tracker.setNotes(form.additional_notes.data)

                flash("Successfully edited medication.", category="success")
                return redirect(url_for("adminTreatments.viewAllTreatments"))
            else:
                flashFormErrors("Unable to edit the treatment", form.errors)

            form.name.date = Tracker.getName()
            form.description.data = Tracker.getDescription()
            form.duration.data = Tracker.getDuration_of_medication()
            form.pills.data = Tracker.getNo_of_pills()
            form.frequency_of_pills.data = Tracker.getFrequency_of_pills()
            form.additional_notes.data = Tracker.getNotes()

            return render_template("admin/shop/editTreatment.html", tracker=tracker, form=form)
    except KeyError:
        flash("Unable to edit treatment details: treatment does not exist", category="error")
        return redirect(url_for("adminTreatments.viewAllTreatments"))


@adminTrackers.route("/admin/trackers/delete/<id>")
@adminAccess
def deleteTracker(id):
    try:
        with shelve.open("treatments", writeback=True) as treatments:
            del treatments[id]
            shutil.rmtree("static/uploads/products/" + id)

            flash("Successfully deleted treatment", category="success")
    except KeyError:
        flash("Unable to delete treatment: treatment does not exist", category="error")

    return redirect(url_for("adminTreatments.viewAllTreatments"))
