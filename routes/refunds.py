import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for, session

from classes.Refund import Refund
from forms import addRefundForm, searchRefundForm, editRefundForm
from functions import flashFormErrors, adminAccess

refunds = Blueprint("refunds", __name__)


@refunds.route("/profile/orders/<id>/refund", methods=['GET', 'POST'])
@adminAccess
def addRefund(id):
    form = addRefundForm(request.form)
    # Check whether user is submitting data and whether form is valid
    if request.method == "POST" and form.validate():
        name = session["user"]["name"]
        email = session["user"]["email"]
        order = id
        reason = form.reason.data
        # Take data from form and combine into a single object representing the product
        refund = Refund(name, email, order, reason)

        with shelve.open("refunds", writeback=True) as refunds:
            refunds[str(refund.getId())] = refund

        flash("Refund successfully created")
        return redirect(url_for("profile.viewOrderHistoryDetails", id=id))
    return render_template("refunds/addRefunds.html", form=form, id=id)

@refunds.route("/profile/orders/", methods=['GET', 'POST'])
@adminAccess
def viewAllRefund():
    # Bring up form functions for webpage
    form = searchRefundForm(request.form)
    # Load products onto webpage
    with shelve.open("refunds") as refunds:
        if len(refunds.keys()) == 0:
            flash("No refund request found.")
        # Display page, (ie for treatments=treatments, it signals jinja to load the list into the webpage. {jinjanam=currentFileName)
        return render_template("refunds/viewRefunds.html", form=form, refunds=refunds)

@refunds.route("/profile/orders/<id>/delete", methods=['GET', 'POST'])
@adminAccess
def deleteRefund(id):
    try:
        with shelve.open("refunds", writeback=True) as refunds:
            del refunds[id]

            flash("Successfully deleted refund request", category="success")
    except KeyError:
        flash("Request either does not exist on database or has a key mismatch.")
    return redirect(url_for("profile.viewOrderHistoryDetails"))
