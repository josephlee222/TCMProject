import shelve

from flask import flash, Blueprint, render_template, redirect, url_for, request
from functions import normalAccess
from forms import addProductCartForm

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

        return render_template("products/viewProduct.html", product=product, form=form)
    except KeyError:
        flash("Sorry! The product you are trying to find has been deleted or moved.", category="error")
        return redirect(url_for("home"), code=404)


@products.route('/products')
@normalAccess
def viewProducts():
    with shelve.open("products") as products:
        return render_template("products/viewProducts.html", products=list(products.values()))