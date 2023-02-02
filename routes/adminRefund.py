import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for

from classes.Refund import Refund
from forms import addRefundForm, searchRefundForm, editRefundForm
from functions import flashFormErrors, adminAccess

adminRefund = Blueprint("adminRefund", __name__)

# Admin side products

@adminRefund.route("/admin/refund/add", methods=['GET', 'POST'])
@adminAccess
def addRefund():
    form = addRefundForm(request.form)
    #Check whether user is submitting data and whether form is valid
    if request.method == "POST" and form.validate():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        product = form.product.data
        reason = form.reason.data
        #Take data from form and combine into a single object representing the product
        refund = Refund(fname, lname, email, product, reason)

        with shelve.open("refunds", writeback=True) as refunds:
            refunds[str(refund.getId())] = refund

        flash("Refund successfully created")
        return redirect(url_for("adminRefund.viewAllRefunds"))
    return render_template("admin/refund/addRefunds.html", form=form)


@adminRefund.route("/admin/refund", methods=['GET', 'POST'])
@adminAccess
def viewAllRefunds():
    # Bring up form functions for webpage
    form = searchRefundForm(request.form)
    # Load products onto webpage
    with shelve.open("refunds") as refunds:
        if len(refunds.keys()) == 0:
            flash("No refund request found.")
        #Display page, (ie for treatments=treatments, it signals jinja to load the list into the webpage. {jinjanam=currentFileName)
        return render_template("admin/refund/viewRefunds.html", form=form, refunds=refunds)


@adminRefund.route("/admin/refund/edit/<id>", methods=['GET', 'POST'])
@adminAccess
def editRefund(id):
    form = editRefundForm(request.form)
    try:
        with shelve.open("refunds", writeback=True) as refunds:
            refund = refunds[id]

            if request.method == "POST" and form.validate():
                print("Edit refund request here")
                refund.setfname(form.fname.data)
                refund.setlname(form.lname.data)
                refund.setemail(form.email.data)
                refund.setproduct(form.product.data)
                refund.setreason(form.reason.data)

                flash("Successfully edited refund request.", category="success")
                return redirect(url_for("adminRefund.viewAllRefunds"))

            else:
                flashFormErrors("Unable to edit the refund request", form.errors)

        form.fname.data = refund.getfname()
        form.lname.data = refund.getlname()
        form.email.data = refund.getemail()
        form.product.data = refund.getproduct()
        form.reason.data = refund.getreason()

        return render_template("admin/refund/editRefunds.html", refunds=refunds, form=form)
    except KeyError:
        flash("Unable to edit refund request: product does not exist", category="error")
    return redirect(url_for("adminRefund.viewAllRefunds"))
@adminRefund.route("/admin/refund/delete/<id>", methods=['GET', 'POST'])
@adminAccess
def deleteRefund(id):
    try:
        with shelve.open("refunds", writeback=True) as refunds:
            del refunds[id]

            flash("Successfully deleted refund request", category="success")
    except KeyError:
        flash("Request either does not exist on database or has a key mismatch.")
    return redirect(url_for("adminRefund.viewAllRefunds"))


