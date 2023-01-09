from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import loginAccess

tracker = Blueprint("medications", __name__)

# User side medications

@tracker.route("/trackers")
@loginAccess
def trackers():
    print("Under construction")
