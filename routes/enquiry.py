from flask import Blueprint

from classes.Enquiry import Enquiry
from forms import createEnquiryForm

enquiry = Blueprint("enquiry", __name__)

import shelve
from datetime import timedelta, date
from flask import flash, render_template, session, redirect, url_for, request
from functions import loginAccess, normalAccess, flashFormErrors

@enquiry.route("/ContactUs", methods=['GET', 'POST'])
@normalAccess
def addEnquiry():
    form = createEnquiryForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        purpose = form.purpose.data
        subject = form.subject.data
        query = form.enquiry.data
        this_enquiry = Enquiry(name, email, purpose, subject, query)

        with shelve.open("enquiry", writeback='True') as enquiries:
            enquiries[str(this_enquiry.getId())] = this_enquiry


        flash("Thanks for contacting TCM Shifu. We will get back to you shortly.", category="success")
        return redirect(url_for("enquiry.addEnquiry"))
    else:
        flashFormErrors("Unable to create the enquiry", form.errors)

    return render_template("enquiry/viewEnquiry.html", form=form)
