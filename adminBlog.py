import os
import shutil
import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from functions import flashFormErrors, goBack, adminAccess, allowedFile
from forms import createArticleForm, uploadImageForm
from classes.Form import Form

adminBlog = Blueprint("adminBlog", __name__)

@adminBlog.route("/admin/blog", methods=['GET', 'POST'])
@adminAccess
def addBlog():
    form = createBlogForm(request.form)

    if request.method == "POST" and form.validate():
        print("add blog")
        title = form.title.data
        content = form.content.data

        blog = blog(title, content)

        with shelve.open("blog", writeback=True) as blog:
            blog[str(blog.getId())] = blog

        flash("Successfully created blog article.", category="success")
        return redirect(url_for("adminBlog.viewAllBlogs"))
    else:
        flashFormErrors("Unable to create the blog article", form.errors)

    return render_template("admin/blog/blogcreation.html", form=form, user=user)



