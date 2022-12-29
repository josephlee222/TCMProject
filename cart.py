import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess, loginAccess

cartpage = Blueprint("cart", __name__)

@cartpage.route("/cart")
@loginAccess
def cart():
    return render_template("cart/cart.html")
