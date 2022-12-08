import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack
from classes.User import User

adminUsers = Blueprint("adminUsers", __name__)

@adminUsers.route("/admin/users/")
def viewAllUsers():
    if "user" in session and session["user"]["admin"]:
        print("yes")
    else:
        flash("Not allowed! Admin users only.", category="error")
        return goBack()

    with shelve.open("users") as users:
        return render_template("users.html", users=users)