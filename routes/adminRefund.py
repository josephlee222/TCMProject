import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for

from forms import editRefundForm
from functions import adminAccess

adminRefund = Blueprint("adminRefund", __name__)


@adminRefund.route("/admin/refunds", methods=['GET', 'POST'])
@adminAccess
def viewAllRefunds():
    # Load products onto webpage
    with shelve.open("refunds") as refunds:
        if len(refunds.keys()) == 0:
            flash("No refund request found.")
        # Display page, (ie for treatments=treatments, it signals jinja to load the list into the webpage. {jinjanam=currentFileName)
        return render_template("admin/refunds/viewRefunds.html", refunds=refunds)


@adminRefund.route("/admin/refunds/<id>/view", methods=['GET', 'POST'])
@adminAccess
def viewRefund(id):
    form = editRefundForm(request.form)
    try:
        with shelve.open("refunds", writeback=True) as refunds:
            refund = refunds[id]
            return render_template("admin/refunds/viewRefund.html", refund=refund)
    except KeyError:
        flash("Unable to edit refund request: request does not exist", category="error")
        return redirect(url_for("adminRefund.viewAllRefunds"))


@adminRefund.route("/admin/refunds/<id>/view/accept", methods=['GET', 'POST'])
@adminAccess
def acceptRefund(id):
    try:
        with shelve.open("refunds", writeback=True) as refunds:
            refund = refunds[id]
            with shelve.open("orders", writeback=True) as orders:
                order = orders[refund.getOrder()]
                order.setStatus(6)
                refund.setResolved()

        flash("Order has been marked as refunded.", category="success")
    except KeyError:
        flash("Unable to edit refund request: Request does not exist", category="error")

    return redirect(url_for("adminRefund.viewAllRefunds"))


@adminRefund.route("/admin/refund/<id>/delete", methods=['GET', 'POST'])
@adminAccess
def deleteRefund(id):
    try:
        with shelve.open("refunds", writeback=True) as refunds:
            del refunds[id]

            flash("Successfully deleted refund request", category="success")
    except KeyError:
        flash("Request either does not exist on database or has a key mismatch.")
    return redirect(url_for("adminRefund.viewAllRefunds"))
