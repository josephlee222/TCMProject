import logging
import shelve
import smtplib
from datetime import datetime, timedelta

import jwt
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from flask_mail import Message

import app
from classes.User import User
from forms import loginUserForm, registerUserForm, resetPasswordForm, changeUserPasswordForm
from functions import flashFormErrors, goBack, unloginAccess

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
@unloginAccess
def login():  # put application's code here
    form = loginUserForm(request.form)

    if request.method == "POST" and form.validate():
        try:
            with shelve.open("users") as users:
                user = users[form.email.data]
                if user.getPassword() == form.password.data:
                    userDict = {
                        "name": user.getName(),
                        "email": user.getEmail(),
                        "accountType": user.getAccountType(),
                        "birthday": user.getBirthday(),
                        "phone": user.getPhone(),
                    }
                    session["user"] = userDict
                    print(session["user"])
                    flash("Successfully logged in. Welcome back!", category="success")
                    return goBack()
                else:
                    flash("Wrong username or password. Please try again", category="error")
        except KeyError:
            flash("Wrong username or password. Please try again", category="error")
    else:
        flashFormErrors("Unable to login", form.errors)

    return render_template("auth/login.html", form=form)


@auth.route('/register', methods=['GET', 'POST'])
@unloginAccess
def register():
    form = registerUserForm(request.form)

    if request.method == "POST" and form.validate():
        print("Register")
        name = form.name.data
        password = form.password.data
        email = form.email.data

        user = User(name, password, email, "customer")
        with shelve.open("users") as users:
            users[email] = user
            flash("User successfully created, you can login now", category="success")
            return redirect(url_for("auth.login"))
    else:
        flashFormErrors("Unable to register an account", form.errors)

    return render_template("auth/register.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
@unloginAccess
def resetPassword():
    form = resetPasswordForm(request.form)

    if request.method == "POST" and form.validate():
        email = form.email.data
        with shelve.open("users") as users:
            if email in users:
                token = jwt.encode({'reset_password': email, 'exp': datetime.utcnow() + timedelta(minutes=15)},
                                   key="reset_password")
                msg = Message("[TCM Shifu] Password reset requested", sender="TCMShifu@gmail.com", recipients=[email])
                msg.html = render_template("email/resetPassword.html", token=token)

                try:
                    app.mail.send(msg)
                except TimeoutError:
                    flash("Unable to send a password reset email due to a timeout error", category="error")
                except smtplib.SMTPDataError:
                    flash("Unable to send a password reset email due to a server error", category="error")
                    logging.exception("Unable to sent email")
                else:
                    flash("Password reset request successfully sent", category="success")
            else:
                flash("The email used is not associated with a TCM Shifu account", category="error")

    return render_template("auth/reset.html", form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
@unloginAccess
def confirmResetPassword(token):
    print("Do something")
    form = changeUserPasswordForm(request.form)
    try:
        email = jwt.decode(token, "reset_password", algorithms=["HS256"])
        with shelve.open("users", writeback=True) as users:
            user = users[email["reset_password"]]
            if request.method == "POST" and form.validate():
                password = form.password.data
                user.setPassword(password)
                flash("The password has successfully been reset", category="success")
                return redirect(url_for("auth.login"))

            return render_template("auth/confirmReset.html", form=form)

    except jwt.ExpiredSignatureError:
        flash("The password reset request has been expired, please try again", category="error")
        return redirect(url_for("home"))
    except KeyError:
        flash("The user that requested for the password reset does not exist anymore", category="error")
        return redirect(url_for("home"))


# Logout page
@auth.route('/logout')
def logout():
    try:
        session.pop("user")
        flash("Successfully logged out")
        return redirect(url_for("home"))
    except KeyError:
        flash("Error while logging out, you were probably never logged in.", category="error")
        return redirect(url_for("home"))
