import logging
import shelve

import stripe
from flask import flash, Blueprint, render_template, request, session, redirect, url_for, jsonify

from classes.Order import Order
from forms import CheckoutForm
from functions import loginAccess, checkCoupon, loginAccessNoCheck

checkout = Blueprint("checkout", __name__)
stripe.api_key = 'sk_test_51MUAERKZ8ITmwoDIYlwF7AOADSdFApOig86RkKjiROILyx7WJ4JyhrsYMlQso3DhMroiwjnnriJ9iq3G914PnVzY009oPpTjGN'


@checkout.route('/checkout')
@checkout.route('/checkout/<coupon>')
@loginAccess
def viewCheckout(coupon=None):
    form = CheckoutForm(request.form)
    discount = 0

    with shelve.open("users", writeback=True) as users:
        user = users[session["user"]["email"]]

        if len(user.getCart()) == 0:
            flash("Unable to checkout as there are no items in the cart", category="error")
            return redirect(url_for("cart.viewCart"))

    if coupon:
        if not checkCoupon(coupon):
            flash("The coupon code entered is not valid", category="error")
            return redirect(url_for("cart.viewCart"))

        with shelve.open("coupons") as coupons:
            for item in coupons.values():
                if item.getCode() == coupon:
                    discount = item.getDiscount()
                    break

    discountAmt = user.getTotalPrice() * (discount / 100)
    price = round(user.getTotalPrice() - discountAmt, 2)
    session["checkoutPrice"] = price
    session["checkoutDiscount"] = discountAmt
    print(price)
    print(round(price * 100))

    choices = []
    for x, address in enumerate(user.getAddress()):
        choices.append(((x, address.getLocation() + " (" + address.getName() + ")")))

    form.delivery.choices = choices

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(round(price * 100)),
            currency='sgd',
            automatic_payment_methods={
                'enabled': True,
            },
        )
    except Exception as e:
        return jsonify(error=str(e)), 403

    return render_template("/payment/checkout.html", form=form, user=user, discount=discountAmt, price=price,
                           clientSecret=intent['client_secret'])


@checkout.route('/checkout/confirm/<deliveryId>')
@loginAccessNoCheck
def confirmCheckout(deliveryId):
    payment = request.args.get("payment_intent")
    if not payment:
        flash("Return to the previous tab to complete payment.")
        return redirect(url_for("home"))

    # Prevent same payment intent from being used
    with shelve.open("paymentIntents") as intents:
        if payment in intents:
            flash("Unable to fulfill payment as this payment has already been settled.", category="error")
            return render_template("/payment/confirmCheckout.html", success=False)

    try:
        intent = stripe.PaymentIntent.retrieve(payment)
        # Verify payment and price
        if intent["status"] == "succeeded" and (intent["amount"] / 100) == session["checkoutPrice"]:
            with shelve.open("users", writeback=True) as users:
                user = users[session["user"]["email"]]
                cart = user.getCart(fixed=False)
                order = Order(user.getEmail(), cart,
                              user.getAddress()[int(deliveryId)] if user.getAddress()[int(deliveryId)] else None,
                              session["checkoutDiscount"])

                # Save order
                with shelve.open("orders") as orders:
                    orders[str(order.getId())] = order

                # subtract quantity
                with shelve.open("products", writeback=True) as products:
                    for item in cart:
                        if item.getType() == "products":
                            product = products[item.getItemId()]
                            product.setQuantity(product.getQuantity() - item.getQuantity())

                # Use payment intent
                with shelve.open("paymentIntents") as intents:
                    intents[payment] = True

                user.clearCart()
                session["cartAmount"] = 0

            return render_template("/payment/confirmCheckout.html", success=True)
        else:
            return render_template("/payment/confirmCheckout.html", success=False)
    except Exception as e:
        print(e)
        flash("Something went wrong while settling the payment with Stripe.", category="error")
        logging.exception("Something went wrong during payment")
        return render_template("/payment/confirmCheckout.html", success=False)
