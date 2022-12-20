import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from forms import loginUserForm, registerUserForm
from functions import flashFormErrors, goBack, unloginAccess
from classes.User import User

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
                    userDict = user.__dict__
                    userDict.pop("password")
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
    email_taken = False

    if request.method == "POST":
        with shelve.open("users") as users:
            if form.email.data in users:
                email_taken = True
                flash("Unable to register: This e-mail has an existing account, please try again", category="error")

    if request.method == "POST" and form.validate() and not email_taken:
        print("Register")
        name = form.name.data
        password = form.password.data
        email = form.email.data

        user = User(name, password, email, "admin")
        with shelve.open("users") as users:
            users[email] = user
            flash("User successfully created", category="success")
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