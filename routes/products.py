import shelve

from flask import flash, Blueprint, render_template, redirect, url_for, request
from wtforms import validators

from forms import addProductCartForm
from functions import normalAccess

products = Blueprint("products", __name__)


@products.route('/products/<id>', methods=['GET', 'POST'])
@normalAccess
def viewProduct(id):
    form = addProductCartForm(request.form)
    try:
        with shelve.open("products") as products:
            product = products[id]

        if request.method == "POST" and form.validate():
            qty = form.qty.data
            return redirect(url_for("cart.addCart", id=product.getId(), quantity=qty, type="products"))

        if product.getQuantity() < 1:
            form.qty.data = 0
            form.qty.render_kw = {"disabled": True}
            form.submit.render_kw = {"disabled": True}

        form.qty.validators.append(
            validators.NumberRange(1, product.getQuantity(), message="Quantity is above stock amount"))

        return render_template("products/viewProduct.html", product=product, form=form)
    except KeyError:
        flash("Sorry! The product you are trying to find has been deleted or moved.", category="error")
        return redirect(url_for("home"))


@products.route('/products')
@normalAccess
def viewProducts():
    with shelve.open("products") as products:
        saleProducts = []
        for product in products.values():
            if product.getOnSale():
                saleProducts.append(product)
        return render_template("products/viewProducts.html", products=list(products.values()),
                               saleProducts=saleProducts)
