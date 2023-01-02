import shelve
from datetime import time
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from functions import flashFormErrors, goBack, adminAccess
from forms import searchCouponsForm, createCouponForm
from classes.Coupon import Coupon

adminCoupons = Blueprint("adminCoupons", __name__)

@adminCoupons.route("/admin/coupons", methods=['GET', 'POST'])
@adminAccess
def viewAllCoupons():
    form = searchCouponsForm(request.form)

    with shelve.open("coupons") as coupons:
        if len(coupons.keys()) == 0:
            flash("No coupons added yet. Add one by clicking 'Create New Coupon'")

        return render_template("admin/shop/viewCoupons.html", form=form, coupons=coupons)

@adminCoupons.route("/admin/coupons/add",  methods=['GET', 'POST'])
@adminAccess
def addCoupon():
    form = createCouponForm(request.form)

    if request.method == "POST" and form.validate():
        print("add coupon")
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

@adminCoupons.route("/admin/coupons/delete/<id>")
@adminAccess
def deleteCoupon(id):
    try:
        with shelve.open("coupons", writeback=True) as coupons:
            del coupons[id]

        flash("Successfully deleted coupon", category="success")
    except KeyError:
        flash("Unable to delete coupon: coupon does not exist", category="error")

    return redirect(url_for("adminCoupons.viewAllCoupons"))