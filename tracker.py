from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import loginAccess

tracker = Blueprint("tracker", __name__)

# User side tracker

@tracker.route("/trackers")
@loginAccess
def trackers():
    print("Under construction")
