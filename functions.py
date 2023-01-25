import functools
import shelve
from flask import flash, Markup, session, redirect, url_for
from functools import wraps
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

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

# Check for valid file ext
def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Decorator func to ensure that the page is only visited by NOT login users (login, register pages)
def unloginAccess(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if "user" in session:
            return goBack()
        else:
            return func(*args, **kwargs)

    return wrapper_func

# Decorator to ensure that only login users can access the page (ex. cart, checkout, profile)
def loginAccess(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if "user" not in session:
            flash("You need to login to access the page.")
            return redirect(url_for("auth.login"))
        else:
            return func(*args, **kwargs)

    return wrapper_func

def deliveryAccess(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if "user" not in session:
            flash("You need to login to access the page.")
            return redirect(url_for("auth.login"))
        elif not session["user"]["accountType"] == "admin" or not session["user"]["accountType"] == "delivery":
            flash("Not allowed! Authorised users only.", category="error")
            return goBack()
        else:
            return func(*args, **kwargs)

    return wrapper_func


# Decorator func to ensure that the page is only visited by users with admin accountType access
def adminAccess(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if "user" not in session:
            flash("You need to login to access the page.")
            return redirect(url_for("auth.login"))
        elif not session["user"]["accountType"] == "admin":
            flash("Not allowed! Admin users only.", category="error")
            return goBack()
        else:
            return func(*args, **kwargs)

    return wrapper_func

def checkCoupon(couponCode):
    with shelve.open("coupons") as coupons:
        for coupon in coupons.values():
            if coupon.getCode() == couponCode and coupon.isValid():
                return True

        return False
