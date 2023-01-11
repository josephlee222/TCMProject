import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from forms import loginUserForm, registerUserForm
from functions import flashFormErrors, goBack, unloginAccess, loginAccess
from classes.User import User
import stripe

checkout = Blueprint("checkout", __name__)
stripe.api_key = 'sk_test_Ou1w6LVt3zmVipDVJsvMeQsc'

def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

@checkout.route('/checkout', methods=['GET', 'POST'])
@loginAccess
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403
