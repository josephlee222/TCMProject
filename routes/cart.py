import shelve

from flask import flash, Blueprint, session, redirect, url_for, render_template, request

from classes.Cart import Cart
from forms import CartCouponForm
from functions import loginAccess, flashFormErrors

cart = Blueprint("cart", __name__)


@cart.route("/cart", methods=['GET', 'POST'])
@loginAccess
def viewCart():
    form = CartCouponForm(request.form)

    if request.method == "POST" and form.validate():
        # valid coupon code, proceed to checkout
        if form.coupon.data != "":
            return redirect(url_for("checkout.viewCheckout", coupon=form.coupon.data))
        else:
            return redirect(url_for("checkout.viewCheckout"))
    else:
        flashFormErrors("The coupon code entered is not valid", form.errors)


    with shelve.open("users") as users:
        user = users[session["user"]["email"]]
        cart = users[session["user"]["email"]].getCart()

    return render_template("cart/viewCart.html", cart=cart, user=user, form=form)


@cart.route("/cart/delete/<id>")
@loginAccess
def deleteCartItem(id):
    try:
        with shelve.open("users", writeback=True) as users:
            cart = users[session["user"]["email"]].getCart()
            del cart[int(id)]

            flash("Cart item has been successfully deleted", category="success")
            return redirect(url_for("cart.viewCart"))
    except ValueError:
        flash("Unable to change quantity, invalid cart ID", category="error")
        return redirect(url_for("cart.viewCart"))


@cart.route("/cart/increase/<id>")
@loginAccess
def increaseCartItem(id):
    try:
        with shelve.open("users", writeback=True) as users:
            cart = users[session["user"]["email"]].getCart()
            item = cart[int(id)]
            if item.getType() != "treatments":
                item.setQuantity(item.getQuantity() + 1)
            else:
                flash("Cannot change quantity for treatments", category="warning")

            return redirect(url_for("cart.viewCart"))
    except ValueError:
        flash("Unable to change quantity, invalid cart ID", category="error")
        return redirect(url_for("cart.viewCart"))


@cart.route("/cart/decrease/<id>")
@loginAccess
def decreaseCartItem(id):
    try:
        with shelve.open("users", writeback=True) as users:
            cart = users[session["user"]["email"]].getCart()
            item = cart[int(id)]
            if item.getType() != "treatments":
                if item.getQuantity() == 1:
                    flash("Cannot decrease quantity below 1. To delete the item from the cart, use the delete button instead.")
                else:
                    item.setQuantity(item.getQuantity() + 1)
            else:
                flash("Cannot change quantity for treatments", category="warning")

        return redirect(url_for("cart.viewCart"))
    except ValueError:
        flash("Unable to change quantity, invalid cart ID", category="error")
        return redirect(url_for("cart.viewCart"))


@cart.route("/cart/add/<type>/<id>/<quantity>")
@loginAccess
def addCart(type, id, quantity):
    try:
        if type == "treatments" or type == "products":
            with shelve.open(type) as items:
                # CHECK PRODUCT IS VALID
                item = items[id]

            # Create cart class to add to user cart
            cart = Cart(id, quantity, type)
            with shelve.open("users", writeback=True) as users:
                user = users[session["user"]["email"]]
                user.addCartItem(cart)

            flash("Item has been added to cart. <a class='alert-link ms-1' href='/cart'>View Cart</a>", category="success")
            if type == "treatments":
                return redirect(url_for("treatments.viewTreatment", id=id))
            else:
                # To be replace with product page
                return redirect(url_for("treatments.viewTreatment", id=id))
        else:
            flash("Cannot item to cart. Invalid product type.", category="error")
    except KeyError:
        flash("Unable to add to cart. Item does not exist.", category="error")