import shelve
from datetime import time, datetime

from flask import Flask, render_template, session, url_for
from flask_mail import Mail

from classes.User import User
from functions import normalAccess

from routes.adminAppointments import adminAppointments
from routes.adminCoupons import adminCoupons
from routes.adminMedications import adminTrackers
from routes.medications import medications
from routes.adminProducts import adminProducts
from routes.adminTreatments import adminTreatments
from routes.adminUsers import adminUsers
from routes.adminBlog import adminBlog
from routes.adminEnquiry import adminEnquiry
from routes.adminOrders import adminOrders
from routes.auth import auth
from routes.cart import cart
from routes.checkout import checkout
from routes.profile import profile
from routes.test import test
from routes.treatments import treatments
from routes.blog import blogs
from routes.enquiry import enquiry

app = Flask(__name__)
app.secret_key = "Secret Key"

# Configuration (The gmail password is correct, its a app password specifically generated)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'TCMShifu@gmail.com'
app.config['MAIL_PASSWORD'] = 'tklwzooqrebhqdmz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Register blueprints
app.register_blueprint(test)
app.register_blueprint(auth)
app.register_blueprint(adminUsers)
app.register_blueprint(adminTreatments)
app.register_blueprint(adminAppointments)
app.register_blueprint(adminCoupons)
app.register_blueprint(adminTrackers)
app.register_blueprint(adminEnquiry)
app.register_blueprint(adminOrders)
app.register_blueprint(medications)
app.register_blueprint(adminBlog)
app.register_blueprint(adminProducts)
app.register_blueprint(profile)
app.register_blueprint(treatments)
app.register_blueprint(cart)
app.register_blueprint(checkout)
app.register_blueprint(blogs)
app.register_blueprint(enquiry)


# ONLY HOMEPAGE HERE (Other pages please use separate files and link via blueprint)
@app.route('/')
@normalAccess
def home():
    session["previous_url"] = url_for("home")
    return render_template("home.html")

# Give website context
@app.context_processor
def websiteContextInit():

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

    with shelve.open("users", writeback=True) as users:
        if "admin@admin.com" not in users:
            print("Default admin user not detected. Creating one...")
            user = User("Admin", "Adminpassword", "admin@admin.com", "admin")
            users["admin@admin.com"] = user
            print("Default Admin E-mail: admin@admin.com")
            print("Default Admin Password: Adminpassword")

initialization()


if __name__ == '__main__':
    app.run(debug=True)
