import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from classes.User import User
from forms import editUserForm

adminUsers = Blueprint("adminUsers", __name__)

@adminUsers.route("/admin/users/")
@adminAccess
def viewAllUsers():
    with shelve.open("users") as users:
        return render_template("users.html", users=users)

@adminUsers.route("/admin/users/edit/<email>")
@adminAccess
def editUser(email):

    form = editUserForm(request.form)