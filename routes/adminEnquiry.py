import datetime
import smtplib

from flask import Blueprint
from marko import convert
from markupsafe import Markup

import app
from forms import searchEnquiry, sendEmailForm

adminEnquiry = Blueprint("adminEnquiry", __name__)

from functions import enquiryreplyTemplate
import shelve
from flask import flash, render_template, redirect, url_for, request
from functions import adminAccess
from flask_mail import Message


@adminEnquiry.route('/admin/enquiries')
@adminAccess
def viewAllEnquiries():
    form = searchEnquiry(request.form)

    with shelve.open("enquiry") as enquiry:
        if len(enquiry.keys()) == 0:
            flash("No enquiries have been made.")

        return render_template("admin/enquiry/viewAllEnquiry.html", form=form, enquiries=enquiry)


@adminEnquiry.route('/admin/enquiries/view/<id>', methods=['GET', 'POST'])
@adminAccess
def viewEnquiry(id):
    form = sendEmailForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data
        subject = form.subject.data
        message = convert(form.message.data)

        msg = Message("[TCM Shifu] Regarding your enquiry", sender="TCMShifu@gmail.com",
                      recipients=[email])
        msg.html = Markup(enquiryreplyTemplate(str(subject), message))

        try:
            app.mail.send(msg)
        except TimeoutError:
            flash("Unable to sent a enquiry e-mail to the customer due to a timeout error",
                  category="warning")
        except smtplib.SMTPDataError:
            flash("Unable to sent a enquiry e-mail to the customer due to a server error",
                  category="error")
        else:
            with shelve.open("enquiry", writeback=True) as enquiries:
                enquiry = enquiries[id]
                today = str(datetime.datetime.now().date())
                enquiry.setResolved(today)

            flash("Email has been successfully sent. User will be notified with an email on the enquiry",
                  category="success")

        return redirect(url_for("adminEnquiry.viewAllEnquiries"))

    with shelve.open("enquiry") as enquiries:
        enquiry = enquiries[id]

        form.email.data = enquiry.getEmail()
        form.subject.data = enquiry.getSubject()
        form.message.data = 'Hey ' + str(enquiry.getName()) + ', in response to your query/feedback on ' + str(
            enquiry.getQuery()) + ' '

        return render_template("admin/enquiry/viewEnquiry.html", id=id, enquiry=enquiry, form=form)
