from flask import Flask, render_template, flash

app = Flask(__name__)
app.secret_key = "Secret Key"

@app.route('/')
def home():
    return render_template("home.html")



@app.route('/test')
def testpage():  # put application's code here
    flash("This is an error alert", category="error")
    flash("This is an info alert")
    flash("This is a success alert", category="success")
    return render_template("uitest.html")

@app.context_processor
def websiteContextInit():
    return {
        "websiteName": "TCMProject"
    }


if __name__ == '__main__':
    app.run()
