import datetime

from flask import Blueprint
from markupsafe import Markup
from marko import convert
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

        msg = Message("[TCM Shifu]", sender="TCMShifu@gmail.com",
                      recipients=[email])
        msg.html = Markup(enquiryreplyTemplate(str(subject), message))
        app.mail.send(msg)

        with shelve.open("enquiry", writeback=True) as enquiries:
            enquiry = enquiries[id]
            enquiry.setResolved(datetime.datetime.now().date())

        flash("Email has been successfully sent. User will be notified with an email about the change",
              category="success")
        return redirect(url_for("adminEnquiry.viewAllEnquiries"))

    with shelve.open("enquiry") as enquiries:
        enquiry = enquiries[id]

        form.email.data = enquiry.getEmail()
        form.subject.data = enquiry.getSubject()
        form.message.data = 'Hey '+str(enquiry.getName())+', in response to your query/feedback on '+str(enquiry.getQuery())+' '


        return render_template("admin/enquiry/viewEnquiry.html", id=id, enquiry=enquiry, form=form)
