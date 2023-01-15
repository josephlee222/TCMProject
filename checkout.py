import shelve

import data as data
import stripe
from flask import Blueprint, render_template, request, redirect, url_for
from pyexpat.errors import messages

import payment
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
        form = CheckoutForm(request.form)
        if request.method == "POST" and form.validate():
            payment_dict = {}
            db = shelve.open('payment.db', 'c')
            try:
                payment_dict = db['Payment']
            except:
                print("Error in retrieving Payment from user.db.")
            try:
                customer = stripe.Charge.create(
                    # amount=calculate_order_amount(data['items']),
                    currency='sgd',
                    # card=form.cleaned_data['stripe_id'],
                )
            except (stripe.error.CardError):
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.success(request, "You have successfully paid")
                return redirect("")
            else:
                messages.error(request, "Unable to take payment")
    else:
        form = CheckoutForm()

    return render_template("payment/checkout.html", form=form)

def create_payment():
    create_payment_form = CheckoutForm(request.form)
    if request.method == 'POST' and create_payment_form.validate():
        payment_dict = {}
        db = shelve.open('payment.db', 'c')
        try:
            payment_dict = db['Payment']
        except:
            print("Error in retrieving Payment from user.db.")

        detail = payment.payment(create_payment_form.fname.data, create_payment_form.sname.data,
                                 create_payment_form.Cardnumber.data, create_payment_form.cvv.data,
                                 create_payment_form.expiry.data,
                                 create_payment_form.shipping.data, create_payment_form.voucher.data)
        payment_dict[detail.get_user_id()] = detail
        db['Users'] = payment_dict

        payment_dict = db['Payment']
        detail = payment_dict[detail.get_user_id()]
        print(detail.get_first_name(), detail.get_last_name(), "was stored in user.db successfully with user_id ==",
              detail.get_user_id())
        db.close()

        return redirect(url_for('home'))
    return render_template('payment/checkout.html', form=create_payment_form)



# @checkout.route('/pay', methods=['GET', 'POST'])
