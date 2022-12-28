from flask import Flask, render_template, flash, Blueprint, session, url_for
from test import test
from auth import auth
from adminUsers import adminUsers
from adminTreatments import adminTreatments


app = Flask(__name__)
app.secret_key = "Secret Key"

# Register blueprints
app.register_blueprint(test)
app.register_blueprint(auth)
app.register_blueprint(adminUsers)
app.register_blueprint(adminTreatments)

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


if __name__ == '__main__':
    app.run()
