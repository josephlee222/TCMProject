import shelve
from datetime import time, datetime

from flask import Flask, render_template, session, url_for

from routes.adminAppointments import adminAppointments
from routes.adminCoupons import adminCoupons
from routes.adminMedications import adminTrackers
from routes.adminProducts import adminProducts
from routes.adminTreatments import adminTreatments
from routes.adminUsers import adminUsers
from routes.auth import auth
from routes.cart import cart
from routes.checkout import checkout
from routes.profile import profile
from routes.test import test
from routes.tracker import tracker
from routes.treatments import treatments

app = Flask(__name__)
app.secret_key = "Secret Key"

# Register blueprints
app.register_blueprint(test)
app.register_blueprint(auth)
app.register_blueprint(adminUsers)
app.register_blueprint(adminTreatments)
app.register_blueprint(adminAppointments)
app.register_blueprint(adminCoupons)
app.register_blueprint(adminTrackers)
app.register_blueprint(tracker)
app.register_blueprint(adminProducts)
app.register_blueprint(profile)
app.register_blueprint(treatments)
app.register_blueprint(cart)
app.register_blueprint(checkout)

# ONLY HOMEPAGE HERE (Other pages please use separate files and link via blueprint)
@app.route('/')
def home():
    session["previous_url"] = url_for("home")
    return render_template("home.html")

# Give website context
@app.context_processor
def websiteContextInit():
    cart = 0
    if "user" in session:
        with shelve.open("users", flag="r") as users:
            user = users[session["user"]["email"]]
            cart = len(user.getCart())
            users.close()

    return {
        "cartAmount": cart,
        "websiteName": "TCM Shifu",
        "now": datetime.now().date(),
    }

def initialization():
    print("Init code start")
    with shelve.open("data", writeback=True) as data:
        if "opening" not in data or "closing" not in data:
            print("No opening hours detected. Setting default 9am - 9pm opening hours.")
            data["opening"] = time(9, 0, 0)
            data["closing"] = time(21, 0, 0)

initialization()


if __name__ == '__main__':
    app.run()
