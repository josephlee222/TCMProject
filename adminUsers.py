import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from classes.User import User
from forms import editUserForm, searchUsersForm, changeUserPasswordForm, addUserForm

adminUsers = Blueprint("adminUsers", __name__)

@adminUsers.route("/admin/users/", methods=['GET', 'POST'])
@adminAccess
def viewAllUsers():
    form = searchUsersForm(request.form)

    # Todo: Add user search functionality

    with shelve.open("users") as users:
        return render_template("admin/viewUsers.html", users=users, form=form)

@adminUsers.route("/admin/users/edit/<email>", methods=['GET', 'POST'])
@adminAccess
def editUser(email):
    form = editUserForm(request.form)

    if request.method == "POST" and form.validate():
        # Do user edit here
        print("Update user")
    else:
        flashFormErrors("Unable to update the user", form.errors)

    with shelve.open("users") as users:
        return render_template("admin/editUser.html", user=users[email], form=form)

@adminUsers.route("/admin/users/add", methods=['GET', 'POST'])
@adminAccess
def addUser():
    form = addUserForm(request.form)

    if request.method == "POST" and form.validate():
        # Do user edit here
        print("Add user")
    else:
        flashFormErrors("Unable to create the user", form.errors)

    with shelve.open("users") as users:
        return render_template("admin/addUser.html", form=form)