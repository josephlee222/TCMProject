import os
import shelve

from flask import flash, Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from classes.Product import Product
from forms import addProductForm, editProductForm, searchProductForm, uploadImageForm
from functions import flashFormErrors, adminAccess, allowedFile

adminProducts = Blueprint("adminProducts", __name__)


# Admin side products

@adminProducts.route("/admin/products/add", methods=['GET', 'POST'])
@adminAccess
def addProduct():
    form = addProductForm(request.form)
    # Check whether user is submitting data and whether form is valid
    if request.method == "POST" and form.validate():
        name = form.name.data
        description = form.description.data
        benefits = form.benefits.data
        price = form.price.data
        salePrice = form.salePrice.data
        onSale = form.onSale.data
        qty = form.qty.data

        # Take data from form and combine into a single object representing the product
        product = Product(name, description, benefits, price, salePrice, onSale, qty)

        # Get images and upload
        images = request.files.getlist("images")
        bPath = "static/uploads/products/" + str(product.getId())
        os.makedirs(bPath)

        for image in images:
            sPath = secure_filename(image.filename)
            if not allowedFile(sPath):
                flash("Unable to add product, image file(s) is invalid", category="error")
                return render_template("admin/products/addProduct.html", form=form)

            path = os.path.join(bPath, sPath)
            image.save(path)
            product.appendImage(path)

        with shelve.open("products", writeback=True) as products:
            products[str(product.getId())] = product

        flash("Successfully created product", category="success")
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
            flash("No products found. Create one by clicking 'Create New Product'.")
        # Display page, (ie for treatments=treatments, it signals jinja to load the list into the webpage. {jinjanam=currentFileName)
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
                product.setPrice(form.price.data)
                product.setSalePrice(form.salePrice.data)
                product.setOnSale(form.onSale.data)
                product.setQuantity(form.qty.data)

                flash("Successfully edited product.", category="success")
                return redirect(url_for("adminProducts.viewAllProducts"))

            else:
                flashFormErrors("Unable to edit the product", form.errors)

        form.name.data = product.getName()
        form.price.data = product.getPrice()
        form.description.data = product.getDescription()
        form.benefits.data = product.getBenefits()
        form.salePrice.data = product.getSalePrice()
        form.onSale.data = product.getOnSale()
        form.qty.data = product.getQuantity()

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
            # I used to delete the image files, but that was causing order history images to be missing
            flash("Successfully deleted product", category="success")
    except KeyError:
        flash("Product either does not exist on database or has a key mismatch.")
    return redirect(url_for("adminProducts.viewAllProducts"))


@adminProducts.route("/admin/products/edit/<id>/images", methods=['GET', 'POST'])
@adminAccess
def editProductImages(id):
    form = uploadImageForm(request.form)
    try:
        with shelve.open("products", writeback=True) as products:
            product = products[id]
            if request.method == "POST" and form.validate():
                images = request.files.getlist("images")
                bPath = "static/uploads/products/" + str(product.getId())
                print(images)

                for image in images:
                    if image.filename != "":
                        sPath = secure_filename(image.filename)
                        if not allowedFile(sPath):
                            flash("Unable to add images, image file(s) is invalid", category="error")
                            return render_template("admin/products/editProductImages.html", product=product, form=form)

                        path = os.path.join(bPath, sPath)
                        image.save(path)
                        product.appendImage(path)
                    else:
                        flash("There are no images to upload.", category="warning")
                        return render_template("admin/products/editProductImages.html", product=product, form=form)

                flash("Successfully uploaded product images.", category="success")
            else:
                flashFormErrors("Unable to edit the treatment images", form.errors)

            return render_template("admin/products/editProductImages.html", product=product, form=form)
    except KeyError:
        flash("Unable to edit product images: product does not exist", category="error")
        return redirect(url_for("adminProducts.viewAllProducts"))


@adminProducts.route("/admin/products/edit/<id>/images/delete/<imageId>")
@adminAccess
def deleteProductImage(id, imageId):
    try:
        with shelve.open("products", writeback=True) as products:
            product = products[id]
            if len(product.getImages()) > 1:
                imgPath = product.getImages()[int(imageId)]
                product.deleteImage(imageId)
                # I used to delete the image files, but that was causing order history images to be missing
                flash("Image successfully deleted", category="success")
            else:
                flash("Unable to delete the last image. Product should has at least one image", category="error")

            return redirect(url_for("adminProducts.editProductImages", id=product.getId()))

    except KeyError:
        flash("Unable to delete product image: product does not exist", category="error")
        return redirect(url_for("adminProducts.viewAllProducts"))


@adminProducts.route("/admin/products/edit/<id>/images/right/<imageId>")
@adminAccess
def moveProductImageRight(id: int, imageId: int):
    try:
        with shelve.open("products", writeback=True) as products:
            product = products[id]
            productImgs = product.getImages()
            imageId = int(imageId)
            if len(productImgs) != imageId + 1:
                productImgs[imageId], productImgs[imageId + 1] = productImgs[imageId + 1], productImgs[imageId]

            return redirect(url_for("adminProducts.editProductImages", id=product.getId()))

    except KeyError:
        flash("Unable to edit product image: product does not exist", category="error")
        return redirect(url_for("adminProducts.viewAllProducts"))


@adminProducts.route("/admin/products/edit/<id>/images/left/<imageId>")
@adminAccess
def moveProductImageLeft(id: int, imageId: int):
    try:
        with shelve.open("products", writeback=True) as products:
            product = products[id]
            productImgs = product.getImages()
            imageId = int(imageId)
            if imageId != 0:
                productImgs[imageId - 1], productImgs[imageId] = productImgs[imageId], productImgs[imageId - 1]

            return redirect(url_for("adminProducts.editProductImages", id=product.getId()))

    except KeyError:
        flash("Unable to edit product image: product does not exist", category="error")
        return redirect(url_for("adminProducts.viewAllProducts"))
