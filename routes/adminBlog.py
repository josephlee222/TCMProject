import os
import shelve
import shutil

from flask import flash, Blueprint, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename

from classes.Blog import Blog
from forms import createArticleForm, editArticleForm
from functions import flashFormErrors, adminAccess

adminBlog = Blueprint("adminBlog", __name__)


@adminBlog.route("/admin/blog/add", methods=['GET', 'POST'])
@adminAccess
def addBlog():
    form = createArticleForm()

    if form.validate_on_submit():
        print("add blog")
        title = form.title.data
        content = form.content.data
        brief = form.brief.data
        image = form.articleImage.data
        blog = Blog(session["user"]["name"], title, content, brief)
        bPath = "static/uploads/blogs/" + str(blog.getId())
        os.makedirs(bPath)

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


@adminBlog.route("/admin/blog/edit/<id>", methods=['GET', 'POST'])
@adminAccess
def editBlog(id):
    form = editArticleForm()
    try:
        with shelve.open("blogs", writeback=True) as blogs:
            blog = blogs[id]

            if form.validate_on_submit():
                title = form.title.data
                brief = form.brief.data
                content = form.content.data
                updatedBy = session["user"]["name"]
                image = form.articleImage.data

                blog.setTitle(title)
                blog.setBrief(brief)
                blog.setContent(content)
                blog.setUpdatedBy(updatedBy)

                if image:
                    bPath = "static/uploads/blogs/" + str(blog.getId())
                    sPath = secure_filename(image.filename)
                    path = os.path.join(bPath, sPath)
                    image.save(path)
                    blog.setCoverImage(path)

                flash("Article has been updated successfully", category="success")
                return redirect(url_for("adminBlog.viewAllBlogs"))
            else:
                flashFormErrors("Unable to edit the blog article", form.errors)

        form.title.data = blog.getTitle()
        form.brief.data = blog.getBrief()
        form.content.data = blog.getContent()

        return render_template("admin/blogs/editBlog.html", image=blog.getCoverImage(), form=form)
    except KeyError:
        flash("Unable to edit blog article: article does not exist", category="error")
        return redirect(url_for("adminBlog.viewAllBlogs"))


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
                flash("Blog article has been deleted, however, there is an error when deleting the image files",
                      category="warning")
            else:
                flash("Successfully deleted blog article", category="success")
    except KeyError:
        flash("Unable to delete blog article: article does not exist", category="error")

    return redirect(url_for("adminBlog.viewAllBlogs"))
