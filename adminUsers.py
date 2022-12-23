import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from classes.User import User
from classes.Address import Address
from forms import editUserForm, searchUsersForm, changeUserPasswordForm, addUserForm, addressForm

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

@adminUsers.route("/admin/users/edit/password/<email>", methods=['GET', 'POST'])
@adminAccess
def editPassword(email):
    form = changeUserPasswordForm(request.form)

    if request.method == "POST" and form.validate():
        # Do user edit here
        with shelve.open("users", writeback=True) as users:
            users[email].setPassword(form.password.data)

        flash("Successfully changed password.", category="success")
    else:
        flashFormErrors("Unable to change the password", form.errors)

    with shelve.open("users") as users:
        return render_template("admin/editPassword.html", user=users[email], form=form)

@adminUsers.route("/admin/users/edit/address/<email>", methods=['GET', 'POST'])
@adminAccess
def viewAddresses(email):

    with shelve.open("users") as users:
        try:
            with shelve.open("addresses") as allAddresses:
                addresses = allAddresses[email]
        except KeyError:
            addresses = []
            flash("No addresses added yet for this account.", category="warning")
        finally:
            return render_template("admin/editAddress.html", user=users[email], addresses=addresses)

@adminUsers.route("/admin/users/add/address/<email>", methods=['GET', 'POST'])
@adminAccess
def addAddress(email):
    form = addressForm(request.form)

    if request.method == "POST" and form.validate():
        print("Add address")
        address = Address(form.name.data, form.location.data)

        with shelve.open("addresses", writeback=True) as addresses:
            if email not in addresses.keys():
                addresses[email] = [address]
            else:
                addresses[email].append(address)

            flash("Address has been successfully added")
            return redirect(url_for("adminUsers.viewAddresses", email=email))
    else:
        flashFormErrors("Unable to add address", form.errors)

    with shelve.open("users") as users:
        return render_template("admin/addAddress.html", user=users[email], form=form)

@adminUsers.route("/admin/users/add", methods=['GET', 'POST'])
@adminAccess
def addUser():
    form = addUserForm(request.form)
    email_taken = False

    if request.method == "POST":
        with shelve.open("users") as users:
            if form.email.data in users:
                email_taken = True
                flash("Unable to register: This e-mail has an existing account, please try again", category="error")

    if request.method == "POST" and form.validate() and not email_taken:
        # Do user edit here
        name = form.name.data
        password = form.password.data
        email = form.email.data
        accountType = form.accountType.data

        user = User(name, password, email, accountType)
        with shelve.open("users") as users:
            users[email] = user
            flash("User successfully created", category="success")
    else:
        flashFormErrors("Unable to create the user", form.errors)

    return render_template("admin/addUser.html", form=form)