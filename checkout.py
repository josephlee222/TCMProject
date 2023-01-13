import data as data
import stripe
from flask import Blueprint, render_template, request, redirect
from pyexpat.errors import messages

from forms import CheckoutForm
from functions import loginAccess

checkout = Blueprint("checkout", __name__)
stripe.api_key = 'sk_test_Ou1w6LVt3zmVipDVJsvMeQsc'


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


@checkout.route('/checkout', methods=['GET', 'POST'])
@loginAccess
def payment():
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                customer = stripe.Charge.create(
                    amount=calculate_order_amount(data['items']),
                    currency='sgd',
                    card=form.cleaned_data['stripe_id'],
                )
            except (stripe.error.CardError):
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.success(request, "You have successfully paid")
                return redirect("")
            else:
                messages.error(request, "Unable to take payment")
        else:
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        form = CheckoutForm()

    return render_template("payment/checkout.html", form=form)
