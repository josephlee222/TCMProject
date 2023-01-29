import os
import shelve
import shutil

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from functions import flashFormErrors, adminAccess
from forms import createArticleForm
from classes.Blog import Blog

adminBlog = Blueprint("adminBlog", __name__)

@adminBlog.route("/admin/blog/add", methods=['GET', 'POST'])
@adminAccess
def addBlog():
    form = createArticleForm(request.form)

    if request.method == "POST" and form.validate():
        print("add blog")
        title = form.title.data
        content = form.content.data
        images = request.files.getlist("articleImage")
        blog = Blog(session["user"]["name"], title, content)
        bPath = "static/uploads/blogs/" + str(blog.getId())
        os.makedirs(bPath)

        for image in images:
            sPath = secure_filename(image.filename)
            path = os.path.join(bPath, sPath)
            image.save(path)
            blog.setCoverImage(path)

        with shelve.open("blogs", writeback=True) as blogs:
            blogs[str(blog.getId())] = blog

        flash("Successfully created blog article.", category="success")
        return redirect(url_for("adminBlog.viewAllBlogs"))
    else:
        flashFormErrors("Unable to create the blog article", form.errors)

    return render_template("admin/blogs/addBlog.html", form=form)


@adminBlog.route("/admin/blog")
@adminAccess
def viewAllBlogs():
    with shelve.open("blogs") as blogs:
        if len(blogs.keys()) == 0:
            flash("No blog articles added yet. Create a new blog article by clicking the 'Create Article' button.")
        return render_template("admin/blogs/viewBlogs.html", blogs=blogs)


@adminBlog.route("/admin/blog/delete/<id>")
@adminAccess
def deleteBlog(id):
    try:
        with shelve.open("blogs", writeback=True) as blogs:
            del blogs[id]
            try:
                shutil.rmtree("static/uploads/blogs/" + id)
            except FileNotFoundError:
                flash("Blog article has been deleted, however, there is an error when deleting the image files", category="warning")
            else:
                flash("Successfully deleted blog article", category="success")
    except KeyError:
        flash("Unable to delete blog article: article does not exist", category="error")

    return redirect(url_for("adminBlog.viewAllBlogs"))

# TODO: add new forms.py funct to view blogs
# TODO: create new html file to view the blogs
