import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for

from classes.User import User
from forms import loginUserForm, registerUserForm
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
                    flash("Successfully logged in, welcome back!")
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