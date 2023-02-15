import shelve

from flask import flash, Blueprint, render_template, redirect, url_for

from functions import normalAccess

blogs = Blueprint("blogs", __name__)


@blogs.route("/blog")
@normalAccess
def viewBlogs():
    with shelve.open("blogs") as blogs:
        return render_template("blog/viewBlogs.html", blogs=list(blogs.values()))


@blogs.route("/blog/<id>")
@normalAccess
def viewBlog(id):
    try:
        with shelve.open("blogs") as blogs:
            blog = blogs[id]

        return render_template("blog/viewBlog.html", blog=blog)
    except KeyError:
        flash("Oops! The article you are trying to view is no longer available.", category="error")
        return redirect(url_for("blogs.viewBlogs"))
