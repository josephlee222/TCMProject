from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import loginAccess

tracker = Blueprint("tracker", __name__)

# User side tracker

@tracker.route("/tracker")
@loginAccess
def tracker():
    print("Under construction")
