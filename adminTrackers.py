import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from classes.Tracker import Tracker, Medicine

adminTrackers = Blueprint("adminTrackers", __name__)

# Admin side tracker

@adminTrackers.route("/admin/trackers/")
@adminAccess
def viewAllTrackers():
    print("Put your render template here")