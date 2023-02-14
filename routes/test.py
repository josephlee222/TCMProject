from flask import flash, Blueprint, render_template, request, session, url_for

from forms import testForm
from functions import flashFormErrors

# Create test route as a blueprint
test = Blueprint("test", __name__)


@test.route('/test', methods=['GET', 'POST'])
def testpage():
    # put application's code here
    form = testForm(request.form)

    # put this in every webpage excluding the login and register pages, this is for the login redirect
    session["previous_url"] = url_for("test.testpage")

    # Check whether the incoming request is a post request and validation is successful
    if request.method == "POST" and form.validate():
        flash("Sample form has been completed successfully", category="success")
    else:
        # flashFormErrors function will automatically check whether there are errors and flash as messages
        # USE THIS WHEN VALIDATING FORMS
        flashFormErrors("Unable to complete the sample form", form.errors)

    # If the incoming request is a get request
    if request.method == "GET":
        flash("This is an error alert", category="error")
        flash("This is an info alert")
        flash("This is a success alert", category="success")

    # Render template at last
    return render_template("uitest.html", form=form)
