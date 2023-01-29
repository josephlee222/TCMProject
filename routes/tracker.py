from flask import Blueprint

from functions import loginAccess

tracker = Blueprint("tracker", __name__)

# User side tracker

@tracker.route("/trackers")
@loginAccess
def trackers():
    print("Under construction")
