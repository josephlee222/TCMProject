import os
import shutil
import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from functions import flashFormErrors, goBack, adminAccess, allowedFile
from forms import searchTreatmentsForm, createTreatmentForm, editTreatmentForm, uploadImageForm
from classes.Form import Form

adminBlog = Blueprint("adminBlog", __name__)

@adminBlog.route("/admin/blog", methods=['GET', 'POST'])
@adminAccess
def addBlog():
    form = createBlogForm(request.form)

    if request.method == "POST" and form.validate():
        print("add blog")
        name = form.name.data
        description = form.description.data
        code = form.code.data
        discount = form.discount.data
        startDate = form.startDate.data
        endDate = form.endDate.data

        coupon = Coupon(name, code, discount, startDate, endDate, description)

        with shelve.open("coupons", writeback=True) as coupons:
            coupons[str(coupon.getId())] = coupon

        flash("Successfully created coupon.", category="success")
        return redirect(url_for("adminCoupons.viewAllCoupons"))
    else:
        flashFormErrors("Unable to create the coupon", form.errors)

    return render_template("admin/shop/addCoupon.html", form=form)
