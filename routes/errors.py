from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def handle404(err):
    return render_template("errors/errorHandler.html", title="Not Found",
                           message="The content you are trying to find has been moved or deleted.")


@errors.app_errorhandler(500)
def handle500(err):
    return render_template("errors/errorHandler.html", title="Internal Server Error",
                           message="Something went wrong on our side when trying to process your request.")


@errors.app_errorhandler(503)
def handle500(err):
    return render_template("errors/errorHandler.html", title="Server is Busy",
                           message="The server is at capacity at the moment. Try again later.")
