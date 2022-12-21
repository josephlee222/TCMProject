from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import loginAccess

cart = Blueprint("cart", __name__)

@cart.route("/cart")
@loginAccess
def cart():
