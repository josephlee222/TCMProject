import shelve
import stripe
import json
from flask import flash, Blueprint, render_template, request, session, redirect, url_for, jsonify
from forms import CheckoutForm
from functions import flashFormErrors, goBack, unloginAccess, loginAccess, checkCoupon
from classes.User import User

checkout = Blueprint("checkout", __name__)
stripe.api_key = 'sk_test_51MUAERKZ8ITmwoDIYlwF7AOADSdFApOig86RkKjiROILyx7WJ4JyhrsYMlQso3DhMroiwjnnriJ9iq3G914PnVzY009oPpTjGN'

@checkout.route('/checkout')
@checkout.route('/checkout/<coupon>')
@loginAccess
def viewCheckout(coupon=None):
    form = CheckoutForm(request.form)
    discount = 0

    if coupon:
        if not checkCoupon(coupon):
            flash("The coupon code entered is not valid", category="error")
            return redirect(url_for("cart.viewCart"))

        with shelve.open("coupons") as coupons:
            for item in coupons.values():
                if item.getCode() == coupon:
                    print("here")
                    discount = item.getDiscount()
                    break

    with shelve.open("users") as users:
        user = users[session["user"]["email"]]

    discountAmt = user.getTotalPrice()*(discount/100)
    price = (user.getTotalPrice()-discountAmt)

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(price*100),
            currency='sgd',
            automatic_payment_methods={
                'enabled': True,
            },
        )
    except Exception as e:
        return jsonify(error=str(e)), 403

    return render_template("/payment/checkout.html", form=form, user=user, discount=discountAmt, price=price, clientSecret=intent['client_secret'])


@checkout.route('/checkout/confirm/<deliveryId>')
@loginAccess
def confirmCheckout(deliveryId):
    if not request.args.get("payment_intent"):
        flash("Return to the previous tab to complete payment.")
        return redirect(url_for("home"))

    try:
        intent = stripe.PaymentIntent.retrieve(request.args.get("payment_intent"))
        if intent["status"] == "succeeded":
            return render_template("/payment/confirmCheckout.html", success=True)
        else:
            return render_template("/payment/confirmCheckout.html", success=False)
    except Exception as e:
        flash("Something went wrong while settling the payment with Stripe", category="error")
        return render_template("/payment/confirmCheckout.html", success=False)


