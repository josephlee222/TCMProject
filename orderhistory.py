import shelve

from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from forms import loginUserForm, registerUserForm,
from functions import flashFormErrors, goBack, unloginAccess, loginAccess
from classes.User import User

history = Blueprint("history", __name__)

@history.route('/history', methods=['GET', 'POST'])
@loginAccess
def order_history(request, username):
    order_qs = Order.objects.filter(user__username=username)

    context = {
        'order_qs': order_qs,
    }
    return render_template(request ,"orderhistory/orderhistory.html.html", form=form)