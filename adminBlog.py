import os
import shutil
import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from functions import flashFormErrors, goBack, adminAccess, allowedFile
from forms import createArticleForm, uploadPreviewImage
from classes.Blog import Blog
from classes.User import User

adminBlog = Blueprint("adminBlog", __name__)

@adminBlog.route("/admin/blog", methods=['GET', 'POST'])
@adminAccess
def addBlog():
    form = createArticleForm(request.form)

    if request.method == "POST" and form.validate():
        print("add blog")
        title = form.title.data
        content = form.content.data

        b = Blog(title, content)

        with shelve.open("Blog", writeback=True) as db:

            db[str(b.getId())] = b

        flash("Successfully created blog article.", category="success")
        return redirect(url_for("adminBlog.addBlog"))
    else:
        flashFormErrors("Unable to create the blog article", form.errors)

    # def __init__(self, name, password, email, accountType, birthday=None, phone=None):
    user = User("Test User 01","1111","test@gmail.com","ADMIN")
    return render_template("admin/blog/blogcreation.html", form=form, user=user)

@adminBlog.route("/admin/blog/view")
@adminAccess
def viewAllBlogs()
# TODO: add new forms.py funct to view blogs
# TODO: create new html file to view the blogs
