import smtplib

from flask import Blueprint

from forms import searchEnquiry

adminEnquiry = Blueprint("adminEnquiry", __name__)

from classes.Enquiry import Enquiry
import shelve
from datetime import timedelta, date
from flask import flash, render_template, session, redirect, url_for, request
from functions import loginAccess, normalAccess, flashFormErrors, adminAccess
from flask_mail import Mail, Message

@adminEnquiry.route('/admin/enquiries')
@adminAccess
def viewAllEnquiries():
    form = searchEnquiry(request.form)

    with shelve.open("enquiry") as enquiry:
        if len(enquiry.keys()) == 0:
            flash("No enquiries have been made.")

        return render_template("admin/enquiry/viewAllEnquiry.html", form=form, enquiries=enquiry)


@adminEnquiry.route('/admin/enquiries/view/<id>')
@adminAccess
def viewEnquiry(id):
    with shelve.open("enquiry") as enquiry:
        enquiries = ''
        if len(enquiry.keys()) == 0:
            flash("No enquiries have been made.")
        for en in enquiry.values():
            for i in range(len(enquiry.keys())):
                if str(i) == id:
                    enquiries = en
        print(enquiries)

        return render_template("admin/enquiry/viewEnquiry.html", id=id, enquiry=enquiries)


@adminEnquiry.route("/send_email", methods=["GET", "POST"])
def send_email():
    email_data = Enquiry("", "", "", "", "")
    if request.method == "POST":
        email_data.to = request.form['to']
        email_data.subject = request.form['subject']
        email_data.message = request.form['query']
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('pethesnotes@gmail.com', '7DSeliza')
            message = 'Subject: {}\n\n{}'.format(email_data.subject, email_data.message)
            server.sendmail('your_email@gmail.com', email_data.to, message)
            server.quit()
            flash("Email sent successfully")
        except:
            flash("Email failed to send")
            return render_template("admin/enquiry/viewEnquiry.html", id=id)

def send_email():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        msg = request.form['message']

        message = Message(subject, sender='TCMShifu@gmail.com', recipients=[email])

        message.body = msg

        mail.send(message)

        flash('Email was successfully sent')
        return render_template("admin/enquiry/viewAllEnquiry.html", id=id)

