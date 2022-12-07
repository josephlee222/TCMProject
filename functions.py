from flask import flash, Markup, session, redirect, url_for

def flashFormErrors(title ,errors):
    if errors:
        errortext = f"<b>{title}:</b>"
        print(errors)
        for errorlist in errors:
            print(errorlist)
            for error in errors[errorlist]:
                errortext += f"<br>{error}"

        flash(Markup(errortext), category="error")

def goBack():
    if "previous_url" in session:
        return redirect(session["previous_url"])
    else:
        return redirect(url_for("home"))