import shelve
import smtplib

from flask import flash, Blueprint, render_template, request, redirect, url_for
from flask_mail import Message
from markupsafe import Markup

import app
from forms import searchOrdersForm, editOrdersStatusForm
from functions import deliveryAccess, statusChangeTemplate

adminOrders = Blueprint("adminOrders", __name__)


@adminOrders.route('/admin/orders')
@deliveryAccess
def viewAllOrders():
    form = searchOrdersForm(request.form)

    with shelve.open("orders") as orders:
        ordersList = list(orders.values())
        ordersList.reverse()
        return render_template("admin/orders/viewOrders.html", orders=ordersList, form=form)


@adminOrders.route('/admin/orders/<id>')
@deliveryAccess
def viewOrder(id):
    try:
        with shelve.open("orders") as orders:
            order = orders[id]

        if order.getStatus() == 1:
            statusDescription = "The order is being prepared by the clinic."
        elif order.getStatus() == 2:
            statusDescription = "The order has been prepared by the clinic and its awaiting delivery."
        elif order.getStatus() == 3:
            statusDescription = "The order is being delivered to the customer via a delivery partner."
        elif order.getStatus() == 4:
            statusDescription = "The order has been delivered to the customer."
        elif order.getStatus() == 5:
            statusDescription = "This order has been cancelled by the user or the clinic."
        elif order.getStatus() == 6:
            statusDescription = "This order has been has been refunded by the clinic."
        else:
            statusDescription = "Unknown delivery status."

        return render_template("admin/orders/viewOrder.html", order=order, statusDescription=statusDescription)
    except KeyError:
        flash("Unable to view order details, order does not exist", category="error")
        return redirect(url_for("adminOrders.viewAllOrders"))


@adminOrders.route('/admin/orders/<id>/edit', methods=['GET', 'POST'])
@deliveryAccess
def editOrderStatus(id):
    form = editOrdersStatusForm(request.form)
    try:
        with shelve.open("orders", writeback=True) as orders:
            order = orders[id]
            choices = [(1, "Preparing"), (2, "Pending delivery"), (3, "On Delivery"), (4, "Delivered")]
            form.status.choices = choices

            if order.getStatus() == 4 or order.getStatus() == 5 or order.getStatus() == 6:
                flash("Unable to update order status, order has already been completed, cancelled or refunded",
                      category="error")
                return redirect(url_for("adminOrders.viewAllOrders"))

            if request.method == "POST" and form.validate():
                order.setStatus(int(form.status.data))
                msg = Message("[TCM Shifu] Your delivery status for order #" + str(order.getId()) + " has changed",
                              sender="TCMShifu@gmail.com", recipients=[order.getUserId()])
                msg.html = Markup(statusChangeTemplate(str(order.getId()), order.getStatusText()))
                try:
                    app.mail.send(msg)
                except TimeoutError:
                    flash("Order status successfully changed however the e-mail is not sent due to a timeout error",
                          category="warning")
                except smtplib.SMTPDataError:
                    flash("Order status successfully changed however the e-mail is not sent due to a server error",
                          category="error")
                else:
                    flash("Order status successfully changed. User will be notified with an email about the change",
                          category="success")

                return redirect(url_for("adminOrders.viewAllOrders"))

            form.status.data = str(order.getStatus())
            print(order.getStatus())

        return render_template("admin/orders/editOrderStatus.html", form=form, order=order)

    except KeyError:
        flash("Unable to update order status, order does not exist", category="error")
        return redirect(url_for("adminOrders.viewAllOrders"))


@adminOrders.route('/admin/orders/<id>/cancel')
@deliveryAccess
def cancelOrder(id):
    try:
        with shelve.open("orders", writeback=True) as orders:
            order = orders[id]

            if order.getStatus() != 6 and order.getStatus() != 5 and order.getStatus() != 4:
                order.setStatus(5)
                flash("Order successfully cancelled", category="success")
            else:
                flash("Unable to cancel order, order has already been completed, cancelled or refunded",
                      category="error")

            return redirect(url_for("adminOrders.viewAllOrders"))

    except KeyError:
        flash("Unable to cancel order, order does not exist", category="error")
        return redirect(url_for("adminOrders.viewAllOrders"))
