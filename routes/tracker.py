from flask import Blueprint

from functions import loginAccess

tracker = Blueprint("medications", __name__)

# User side medications

@tracker.route("/trackers")
@loginAccess
def trackers():
    print("Under construction")
