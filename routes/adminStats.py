import shelve
from datetime import datetime

from flask import Blueprint, render_template

from functions import adminAccess

adminStats = Blueprint("adminStats", __name__)


@adminStats.route("/admin", methods=['GET', 'POST'])
@adminAccess
def dashboard():
    pending = 0
    unresolved = 0
    productsAmt = 0
    usersAmt = 0
    profitThisMonth = 0
    profitLastMonth = 0
    profitLifetime = 0
    margin = 0
    opening = 0
    closing = 0
    with shelve.open("orders") as orders:
        for order in orders.values():
            if order.getStatus() == 1:
                pending += 1

            if order.getDateTime().month == datetime.now().month:
                profitThisMonth += order.getTotalPrice()
            elif order.getDateTime().month == datetime.now().month - 1:
                profitLastMonth += order.getTotalPrice()

            if profitLastMonth != 0 and profitThisMonth != 0:
                margin = ((profitThisMonth - profitLastMonth) / profitLastMonth) * 100
            else:
                if profitLastMonth == 0:
                    margin = profitThisMonth
                else:
                    margin = -profitLastMonth

            profitLifetime += order.getTotalPrice()

    with shelve.open("users") as users:
        usersAmt = len(users)

    with shelve.open("products") as products, shelve.open("treatments") as treatments:
        productsAmt = len(products) + len(treatments)

    with shelve.open("enquiry") as enquiries:
        for enquiries in enquiries.values():
            if enquiries.getResolved() == "Not resolved":
                unresolved += 1

    with shelve.open("data", writeback=True) as data:
        opening = data["opening"]
        closing = data["closing"]

    return render_template("admin/dashboard.html", users=usersAmt, products=productsAmt, pending=pending,
                           unresolved=unresolved, profitThisMonth=profitThisMonth, profitLastMonth=profitLastMonth,
                           margin=round(margin, 2), profitLifetime=profitLifetime, opening=opening, closing=closing)
