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

    with shelve.open("users", writeback=True) as users:
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
                with shelve.open("products") as products:
                    product = products[item.getItemId()]
                    if not (item.getQuantity() + 1) > product.getQuantity():
                        item.setQuantity(item.getQuantity() + 1)
                    else:
                        flash("Cannot increase quantity for product as there is not enough stock", category="warning")
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
                    flash(
                        "Cannot decrease quantity below 1. To delete the item from the cart, use the delete button instead.")
                else:
                    item.setQuantity(item.getQuantity() - 1)
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
                if type == "products":
                    if int(quantity) > item.getQuantity():
                        flash("Cannot item to cart. Quantity cannot exceed stock available.", category="error")
                        return redirect(url_for("products.viewProduct", id=id))

                # Create cart class to add to user cart. Too many if statements, but it works for now :>
                cart = Cart(id, int(quantity), type, item)
                with shelve.open("users", writeback=True) as users:
                    user = users[session["user"]["email"]]
                    if type == "products":
                        alreadyAdded = False
                        for cartItem in user.getCart(fixed=True):
                            # Check whether selected product already exist in cart by going through every item in
                            # cart. If it exists, check whether new quantity overshoots available quantity. If it
                            # does not, set cart item quantity to reflect new quantity
                            if cartItem.getItemId() == id:
                                alreadyAdded = True
                                if cartItem.getQuantity() + int(quantity) <= item.getQuantity():
                                    cartItem.setQuantity(cartItem.getQuantity() + int(quantity))
                                    flash(
                                        "Item has been added to cart. <a class='alert-link ms-1' href='/cart'>View Cart</a>",
                                        category="success")
                                else:
                                    flash(
                                        "Unable to add anymore of this item, maximum possible quantity has been already been added.",
                                        category="error")
                                    break

                        if not alreadyAdded:
                            user.addCartItem(cart)
                            flash("Item has been added to cart. <a class='alert-link ms-1' href='/cart'>View Cart</a>",
                                  category="success")
                    else:
                        user.addCartItem(cart)
                        flash("Item has been added to cart. <a class='alert-link ms-1' href='/cart'>View Cart</a>",
                              category="success")

            if type == "treatments":
                return redirect(url_for("treatments.viewTreatment", id=id))
            else:
                return redirect(url_for("products.viewProduct", id=id))
        else:
            flash("Cannot item to cart. Invalid product type.", category="error")
            if type == "treatments":
                return redirect(url_for("treatments.viewTreatment", id=id))
            else:
                return redirect(url_for("products.viewProduct", id=id))
    except KeyError:
        flash("Unable to add to cart. Item does not exist.", category="error")
