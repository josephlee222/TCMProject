import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from classes.User import User
from classes.Address import Address
from forms import editUserForm, searchUsersForm, changeUserPasswordForm, addUserForm, addAddressForm, editAddressForm, deleteUserForm

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

@adminUsers.route("/admin/users/delete/<email>", methods=['GET', 'POST'])
@adminAccess
def deleteUser(email):
    form = deleteUserForm(request.form)

    if request.method == "POST" and form.validate():
        # Do user edit here
        print("Delete user")
        with shelve.open("users") as users:
            if form.name.data != users[email].getName():
                flash("Unable to delete the account: The account name does not match the registered email account name.", category="error")
            else:
                try:
                    del users[email]
                    flash("Successfully deleted the account.", category="success")

                    if session["user"]["email"] == email:
                        flash("Logging out because your account has been deleted.", category="warning")
                        return redirect(url_for("auth.logout"))

                    return redirect(url_for("adminUsers.viewAllUsers"))
                except KeyError:
                    flash("Unable to delete the account: The account does not exist.", category="error")
    else:
        flashFormErrors("Unable to delete the account", form.errors)

    with shelve.open("users") as users:
        return render_template("admin/deleteUser.html", user=users[email], form=form)

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
        if users[email].getAddress() is not None:
            addresses = users[email].getAddress()
        else:
            addresses = []
            flash("No addresses added yet for this account.", category="warning")
        return render_template("admin/editAddress.html", user=users[email], addresses=addresses)


@adminUsers.route("/admin/users/edit/address/<email>/<id>", methods=['GET', 'POST'])
@adminAccess
def editAddress(email, id):
    form = editAddressForm(request.form)

    if request.method == "POST" and form.validate():
        print("Edit Address")
        address = Address(form.name.data, form.location.data)

        with shelve.open("users", writeback=True) as users:
            users[email].editAddress(int(id), address)

            flash("Address has been successfully edited", category="success")
            return redirect(url_for("adminUsers.viewAddresses", email=email))
    else:
        flashFormErrors("Unable to edit address", form.errors)
        with shelve.open("users") as users:
            if users[email].getAddress() is not None:
                try:
                    address = users[email].getAddress()[int(id)]
                except IndexError:
                    flash("Cannot edit address. Specified address ID does not exist.", category="error")
                    return redirect(url_for("adminUsers.viewAddresses", email=email))
            else:
                flash("Cannot edit address. No address has been added yet", category="error")
                return redirect("adminUsers.viewAddresses")

    with shelve.open("users") as users:
        return render_template("admin/editAddress.html", user=users[email], address=address, id=id, form=form)


@adminUsers.route("/admin/users/add/address/<email>", methods=['GET', 'POST'])
@adminAccess
def addAddress(email):
    form = addAddressForm(request.form)

    if request.method == "POST" and form.validate():
        print("Add address")
        address = Address(form.name.data, form.location.data)

        with shelve.open("users", writeback=True) as users:
            users[email].setAddress(address)

            flash("Address has been successfully added", category="success")
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
