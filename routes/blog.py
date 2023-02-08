import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import normalAccess

blogs = Blueprint("blogs", __name__)

@blogs.route("/blog", methods=['GET', 'POST'])
@normalAccess
def viewBlogs():
    with shelve.open("blogs") as blogs:
        return render_template("blog/viewBlogs.html", blogs=list(blogs.values()))