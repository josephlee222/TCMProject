import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for, session

from classes.Refund import Refund
from forms import addRefundForm
from functions import loginAccess

refunds = Blueprint("refunds", __name__)


@refunds.route("/profile/orders/<id>/refund", methods=['GET', 'POST'])
@loginAccess
def addRefund(id):
    form = addRefundForm(request.form)
    # Check whether user is submitting data and whether form is valid
    try:
        with shelve.open("orders") as orders:
            order = orders[id]
            if order.getStatus() == 5 or order.getStatus() == 6:
                flash("Unable to create a refund request and the order is already cancelled or refunded",
                      category="success")
                return redirect(url_for("profile.viewOrderHistoryDetails", id=id))
    except KeyError:
        flash("Unable to create a refund request and the order is already cancelled or refunded", category="success")
        return redirect(url_for("profile.viewOrderHistory"))

    if request.method == "POST" and form.validate():
        name = session["user"]["name"]
        email = session["user"]["email"]
        order = id
        reason = form.reason.data
        # Take data from form and combine into a single object representing the product
        refund = Refund(name, email, order, reason)

        with shelve.open("refunds", writeback=True) as refunds:
            refunds[str(refund.getId())] = refund

        flash("Refund request successfully created", category="success")
        return redirect(url_for("profile.viewOrderHistoryDetails", id=id))

    return render_template("refunds/addRefunds.html", form=form, id=id)


@refunds.route("/profile/orders/refunds", methods=['GET', 'POST'])
@loginAccess
def viewAllRefund():
    with shelve.open("refunds") as refunds:
        refund = []
        for item in refunds.values():
            if item.getEmail() == session["user"]["email"]:
                print(item.getResolved())
                refund.append(item)
        # Display page, (ie for treatments=treatments, it signals jinja to load the list into the webpage. {jinjanam=currentFileName)
        return render_template("refunds/viewRefunds.html", refunds=refund)


@refunds.route("/profile/orders/refunds/<id>/delete", methods=['GET', 'POST'])
@loginAccess
def deleteRefund(id):
    try:
        with shelve.open("refunds", writeback=True) as refunds:
            del refunds[id]
            flash("Successfully deleted refund request", category="success")
    except KeyError:
        flash("Request either does not exist on database or has a key mismatch.")

    return redirect(url_for("refunds.viewAllRefund"))
