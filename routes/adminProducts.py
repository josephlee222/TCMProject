import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for

from classes.Product import Product
from forms import addProductForm, editProductForm, searchProductForm
from functions import flashFormErrors, adminAccess

adminProducts = Blueprint("adminProducts", __name__)

# Admin side products

@adminProducts.route("/admin/products/add", methods=['GET', 'POST'])
@adminAccess
def addProduct():
    form = addProductForm(request.form)
    #Check whether user is submitting data and whether form is valid
    if request.method == "POST" and form.validate():
        name = form.name.data
        description = form.description.data
        benefits = form.benefits.data
        price = form.price.data
        details = form.details.data
        #Take data from form and combine into a single object representing the product
        product = Product(name, description, benefits, price, details)

        with shelve.open("products", writeback=True) as products:
            products[str(product.getId())] = product

        flash("Product successfully created")
        return redirect(url_for("adminProducts.viewAllProducts"))
    return render_template("admin/products/addProduct.html", form=form)


@adminProducts.route("/admin/products", methods=['GET', 'POST'])
@adminAccess
def viewAllProducts():
    # Bring up form functions for webpage
    form = searchProductForm(request.form)
    # Load products onto webpage
    with shelve.open("products") as products:
        if len(products.keys()) == 0:
            flash("No products found.")
        #Display page, (ie for treatments=treatments, it signals jinja to load the list into the webpage. {jinjanam=currentFileName)
        return render_template("admin/products/viewProducts.html", form=form, products=products)


@adminProducts.route("/admin/products/edit/<id>", methods=['GET', 'POST'])
@adminAccess
def editProduct(id):
    form = editProductForm(request.form)
    try:
        with shelve.open("products", writeback=True) as products:
            product = products[id]

            if request.method == "POST" and form.validate():
                print("Edit product here")
                product.setName(form.name.data)
                product.setDescription(form.description.data)
                product.setBenefits(form.benefits.data)
                product.setDetails(form.details.data)
                product.setPrice(form.price.data)
                #product.setSalePrice(form.salePrice.data)
                #product.setOnSale(form.onSale.data)

                flash("Successfully edited product.", category="success")
                return redirect(url_for("adminProducts.viewAllProducts"))

            else:
                flashFormErrors("Unable to edit the product", form.errors)

        form.name.data = product.getName()
        form.price.data = product.getPrice()
        form.description.data = product.getDescription()
        form.benefits.data = product.getBenefits()
        form.details.data = product.getDetails()

        return render_template("admin/products/editProduct.html", product=product, form=form)
    except KeyError:
        flash("Unable to edit product details: product does not exist", category="error")
    return redirect(url_for("adminProducts.viewAllProducts"))
@adminProducts.route("/admin/products/delete/<id>", methods=['GET', 'POST'])
@adminAccess
def deleteProduct(id):
    try:
        with shelve.open("products", writeback=True) as products:
            del products[id]

            flash("Successfully deleted product", category="success")
    except KeyError:
        flash("Product either does not exist on database or has a key mismatch.")
    return redirect(url_for("adminProducts.viewAllProducts"))


