import functools

from flask import flash, Markup, session, redirect, url_for
from functools import wraps

def flashFormErrors(title ,errors):
    if errors:
        errortext = f"<b>{title}:</b>"
        print(errors)
        for errorlist in errors:
            print(errorlist)
            for error in errors[errorlist]:
                errortext += f"<br>{error}"

        flash(Markup(errortext), category="error")

def goBack():
    if "previous_url" in session:
        return redirect(session["previous_url"])
    else:
        return redirect(url_for("home"))

# Decorator func to ensure that the page is only visited by NOT login users (login, register pages)
def unloginAccess(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if "user" in session:
            return goBack()
        else:
            return func(*args, **kwargs)

    return wrapper_func

# Decorator func to ensure that the page is only visited by users with admin access
def adminAccess(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if "user" not in session and not session["user"]["admin"]:
            flash("Not allowed! Admin users only.", category="error")
            return goBack()
        else:
            return func(*args, **kwargs)

    return wrapper_func