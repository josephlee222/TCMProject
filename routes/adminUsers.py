import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for

from classes.Address import Address
from classes.User import User
from forms import editUserForm, searchUsersForm, changeUserPasswordForm, addUserForm, addAddressForm, editAddressForm, \
    deleteUserForm
from functions import flashFormErrors, adminAccess

adminUsers = Blueprint("adminUsers", __name__)


@adminUsers.route("/admin/users/", methods=['GET', 'POST'])
@adminAccess
def viewAllUsers():
    form = searchUsersForm(request.form)

    # Todo: Add user search functionality

    with shelve.open("users") as users:
        return render_template("admin/users/viewUsers.html", users=users, form=form)


@adminUsers.route("/admin/users/edit/<email>", methods=['GET', 'POST'])
@adminAccess
def editUser(email):
    form = editUserForm(request.form)
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[email]
            if request.method == "POST" and form.validate():
                # Do user edit here
                name = form.name.data
                password = user.getPassword()
                email = user.getEmail()
                accountType = user.getAccountType()
                birthday = form.birthday.data
                phone = form.phone.data
                user = User(name, password, email, accountType)

                if birthday != "":
                    user.setBirthday(birthday)

                if phone != "":
                    user.setPhone(phone)

                users[email] = user

                flash("User successfully edited", category="success")
                return redirect(url_for("adminUsers.viewAllUsers"))
            else:
                flashFormErrors("Unable to update the user", form.errors)

            return render_template("admin/users/editUser.html", user=user, form=form)
    except KeyError:
        flash("Unable to edit the user: Account does not exist", category="error")
        return redirect(url_for("adminUsers.viewAllUsers"))


@adminUsers.route("/admin/users/delete/<email>", methods=['GET', 'POST'])
@adminAccess
def deleteUser(email):
    form = deleteUserForm(request.form)
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[email]
            if request.method == "POST" and form.validate():
                # Do user edit here
                print("Delete user")
                if form.name.data != user.getName():
                    flash(
                        "Unable to delete the account: The account name does not match the registered email account name.",
                        category="error")
                else:
                    try:
                        del users[email]

                        # Delete all user data like appointments and orders
                        with shelve.open("appointments", writeback=True) as appointments:
                            for key, appointment in appointments.items():
                                if appointment.getDoctorEmail() == email or appointment.getUserEmail() == email:
                                    del appointments[key]

                        with shelve.open("orders", writeback=True) as orders:
                            for key, order in orders.items():
                                if order.getUserId() == email:
                                    del orders[key]

                        # TODO: Add refunds

                        flash("Successfully deleted the account.", category="success")

                        if session["user"]["email"] == email:
                            flash("Logging out because your account has been deleted.", category="warning")
                            return redirect(url_for("auth.logout"))

                        return redirect(url_for("adminUsers.viewAllUsers"))
                    except KeyError:
                        flash("Unable to delete the account: The account does not exist.", category="error")
            else:
                flashFormErrors("Unable to delete the account", form.errors)

            return render_template("admin/users/deleteUser.html", user=user, form=form)
    except KeyError:
        flash("Unable to delete the account: The account does not exist.", category="error")
        return redirect(url_for("adminUsers.viewAllUsers"))


@adminUsers.route("/admin/users/edit/password/<email>", methods=['GET', 'POST'])
@adminAccess
def editPassword(email):
    form = changeUserPasswordForm(request.form)
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[email]
            if request.method == "POST" and form.validate():
                # Do user edit here
                user.setPassword(form.password.data)
                flash("Successfully changed password.", category="success")
            else:
                flashFormErrors("Unable to change the password", form.errors)

            return render_template("admin/users/editPassword.html", user=user, form=form)
    except KeyError:
        flash("Unable to change the password: Account does not exist", category="error")
        return redirect(url_for("adminUsers.viewAllUsers"))


@adminUsers.route("/admin/users/edit/address/<email>", methods=['GET', 'POST'])
@adminAccess
def viewAddresses(email):
    try:
        with shelve.open("users") as users:
            user = users[email]
            if user.getAddress() is not None and user.getAddress() != []:
                addresses = user.getAddress()
            else:
                addresses = []
                flash("No addresses added yet for this account.", category="warning")
            return render_template("admin/users/editAddress.html", user=user, addresses=addresses)
    except KeyError:
        flash("Unable to view delivery addresses: Account does not exist", category="error")
        return redirect(url_for("adminUsers.viewAllUsers"))


@adminUsers.route("/admin/users/edit/address/<email>/<id>", methods=['GET', 'POST'])
@adminAccess
def editAddress(email, id):
    form = editAddressForm(request.form)
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[email]
            if request.method == "POST" and form.validate():
                print("Edit Address")
                address = Address(form.name.data, form.location.data)
                if address.getLatitude() is not None and address.getLongitude() is not None:
                    user.editAddress(int(id), address)
                    flash("Address has been successfully edited", category="success")
                    return redirect(url_for("adminUsers.viewAddresses", email=email))
                else:
                    flash("Unable to edit address because our location provider could not find your address.",
                          category="error")
            else:
                flashFormErrors("Unable to edit address", form.errors)
                if user.getAddress() is not None:
                    try:
                        address = user.getAddress()[int(id)]
                    except IndexError:
                        flash("Cannot edit address. Specified address ID does not exist.", category="error")
                        return redirect(url_for("adminUsers.viewAddresses", email=email))
                else:
                    flash("Cannot edit address. No address has been added yet", category="error")
                    return redirect(url_for("adminUsers.viewAddresses", email=email))

            return render_template("admin/users/editAddress.html", user=user, address=address, id=id, form=form)
    except KeyError:
        flash("Unable to edit delivery address: Account does not exist", category="error")
        return redirect(url_for("adminUsers.viewAllUsers"))


@adminUsers.route("/admin/users/delete/address/<email>/<id>")
@adminAccess
def deleteAddress(email, id):
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[email]
            if user.deleteAddress(id):
                flash("Your saved address has been deleted", category="success")
            else:
                flash("Unable to delete delivery address: Delivery address does not exist", category="error")
    except KeyError:
        flash("Unable to delete delivery address: Account or delivery address does not exist", category="error")

    return redirect(url_for("adminUsers.viewAddresses", email=email))


@adminUsers.route("/admin/users/add/address/<email>", methods=['GET', 'POST'])
@adminAccess
def addAddress(email):
    form = addAddressForm(request.form)
    try:
        with shelve.open("users", writeback=True) as users:
            user = users[email]
            if request.method == "POST" and form.validate():
                address = Address(form.name.data, form.location.data)

                if address.getLatitude() is not None and address.getLongitude() is not None:
                    user.setAddress(address)
                    flash("Your new address has been added to your account", category="success")
                    return redirect(url_for("adminUsers.viewAddresses", email=email))
                else:
                    flash("Unable to add address because our location provider could not find your address.",
                          category="error")
            else:
                flashFormErrors("Unable to add address", form.errors)

            return render_template("admin/users/addAddress.html", user=user, form=form)
    except KeyError:
        flash("Unable to add delivery address: Account does not exist", category="error")
        return redirect(url_for("adminUsers.viewAllUsers"))


@adminUsers.route("/admin/users/add", methods=['GET', 'POST'])
@adminAccess
def addUser():
    form = addUserForm(request.form)

    if request.method == "POST" and form.validate():
        # Do user edit here
        name = form.name.data
        password = form.password.data
        email = form.email.data
        accountType = form.accountType.data
        birthday = form.birthday.data
        phone = form.phone.data

        user = User(name, password, email, accountType)

        if birthday != "":
            user.setBirthday(birthday)

        if phone != "":
            user.setPhone(phone)

        with shelve.open("users") as users:
            users[email] = user
            flash("User successfully created", category="success")
    else:
        flashFormErrors("Unable to create the user", form.errors)

    return render_template("admin/users/addUser.html", form=form)
