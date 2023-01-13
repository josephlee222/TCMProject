import shelve
from datetime import time

from flask import Flask, render_template, flash, Blueprint, session, url_for, send_from_directory
from test import test
from auth import auth
from adminUsers import adminUsers
from adminTreatments import adminTreatments
from adminAppointments import adminAppointments
from adminCoupons import adminCoupons
from adminBlog import adminBlog
from tracker import tracker


app = Flask(__name__)
app.secret_key = "Secret Key"

# Register blueprints
app.register_blueprint(test)
app.register_blueprint(auth)
app.register_blueprint(adminUsers)
app.register_blueprint(adminTreatments)
app.register_blueprint(adminAppointments)
app.register_blueprint(adminCoupons)
app.register_blueprint(tracker)
app.register_blueprint(adminBlog)

# ONLY HOMEPAGE HERE (Other pages please use separate files and link via blueprint)
@app.route('/')
def home():
    session["previous_url"] = url_for("home")
    return render_template("home.html")

# Give website context
@app.context_processor
def websiteContextInit():
    return {
        "websiteName": "TCM Shifu",
    }

def initialization():
    print("Init code start")
    with shelve.open("data", writeback=True) as data:
        if "opening" not in data or "closing" not in data:
            data["opening"] = time(9, 0, 0)
            data["closing"] = time(21, 0, 0)

initialization()


if __name__ == '__main__':
    app.run()
