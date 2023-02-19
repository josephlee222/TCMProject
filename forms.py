import shelve
from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Form, StringField, PasswordField, RadioField, validators, EmailField, DateField, ValidationError, \
    SubmitField, TextAreaField, IntegerField, DecimalField, BooleanField, MultipleFileField, SelectField, TimeField

from functions import checkCoupon


# Put all forms here with a comment describing the form

# ADMIN USERS FORMS

# Sample form for test page
class testForm(Form):
    test = StringField("Testing Field", [
        # Validators in here, write error messages in the "message" parameter and use flashFormErrors() when
        # validating on post
        validators.Length(3, 64, message="The input must be between 3 to 64 characters"),
        validators.DataRequired(message="The input is required")
    ])


# User login form
class loginUserForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail is required to login")
    ])
    password = PasswordField("Password", [
        validators.Length(8, 64, message="Password must be at least 8 characters"),
        validators.DataRequired(message="Password is required to login")
    ])

    submit = SubmitField("Login")

class resetPasswordForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail is required to login")
    ])

    submit = SubmitField("Send Reset E-mail")


# User registration form
class registerUserForm(Form):
    name = StringField("Your name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Username is required for registration")
    ])
    password = PasswordField("Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.Regexp("(?=.*[A-Z])", message="New password should contain at least 1 uppercase letter"),
        validators.DataRequired(message="Password is required for registration")
    ])
    confirmPassword = PasswordField("Confirm Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.equal_to("password", message="New password and confirm password fields do not match."),
        validators.data_required(message="You need to confirm your new password.")
    ])
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail address is required for registration")
    ])

    submit = SubmitField("Register")

    def validate_email(form, field):
        with shelve.open("users") as users:
            if form.email.data in users:
                raise ValidationError("This e-mail has an existing account, please try again")


class searchUsersForm(Form):
    name = StringField("Search by name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required to search")
    ])


class editUserForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True)
    ], render_kw={'readonly': True})
    name = StringField("Account Name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required")
    ])
    birthday = DateField("Birthday", [
        validators.Optional()
    ])
    phone = StringField("Phone Number", [
        validators.Optional(),
        validators.regexp("^[689]\d{7}$",
                          message="Phone number must a number that starts with the number 6, 8 or 9 and 8 digits long")
    ])
    submit = SubmitField("Edit User")

    def validate_birthday(form, birthday):
        if form.birthday.data > datetime.now().date():
            raise ValidationError("Invalid birthday, date cannot be in the future")


class editProfileForm(Form):
    name = StringField("Account Name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required")
    ])
    birthday = DateField("Birthday", [
        validators.Optional()
    ])
    phone = StringField("Phone Number", [
        validators.Optional(),
        validators.regexp("^[689]\d{7}$",
                          message="Phone number must a number that starts with the number 6, 8 or 9 and 8 digits long")
    ])

    submit = SubmitField("Update Profile")

    def validate_birthday(form, birthday):
        if form.birthday.data > datetime.now().date():
            raise ValidationError("Invalid birthday, date cannot be in the future")


class changeUserPasswordForm(Form):
    password = PasswordField("Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.Regexp("(?=.*[A-Z])", message="New password should contain at least 1 uppercase letter"),
        validators.DataRequired(message="Password is required for registration")
    ])
    confirmPassword = PasswordField("Confirm Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.equal_to("password", message="New password and confirm password fields do not match."),
        validators.data_required(message="You need to confirm your new password.")
    ])

    submit = SubmitField("Change Password")


class addUserForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail Address is required")
    ])
    name = StringField("Account Name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required")
    ])
    password = PasswordField("New Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.Regexp("(?=.*[A-Z])", message="New password should contain at least 1 uppercase letter"),
        validators.DataRequired(message="Password is required for registration")
    ])
    confirmPassword = PasswordField("Confirm Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.equal_to("password", message="New password and confirm password fields do not match."),
        validators.data_required(message="You need to confirm your new password.")
    ])
    birthday = DateField("Birthday", [
        validators.Optional(),

    ])
    phone = StringField("Phone Number", [
        validators.Optional(),
        validators.regexp("^[689]\d{7}$",
                          message="Phone number must a number that starts with the number 6, 8 or 9 and 8 digits long")
    ])
    accountType = RadioField("Account Type", choices=[
        ("customer", "Customer Account"),
        ("admin", "Doctor/Staff Account"),
        ("delivery", "Delivery Partner Account")
    ], validators=[
        validators.DataRequired("Account type is required")
    ])
    submit = SubmitField("Create User")

    def validate_email(form, field):
        with shelve.open("users") as users:
            if form.email.data in users:
                raise ValidationError("This e-mail has an existing account, please try again")

    def validate_birthday(form, birthday):
        if form.birthday.data > datetime.now().date():
            raise ValidationError("Invalid birthday, date cannot be in the future")


class addAddressForm(Form):
    name = StringField("Address Name", [
        validators.Length(1, 64, message="Address name must be between 1 to 64 characters"),
        validators.DataRequired(message="Address name is required")
    ])
    location = StringField("Location", [
        validators.Length(16, 256, message="Location must be between 16 to 256 characters"),
        validators.DataRequired(message="Location is required")
    ])

    submit = SubmitField("Add Address")


class editAddressForm(Form):
    name = StringField("Address Name", [
        validators.Length(1, 64, message="Address name must be between 1 to 64 characters"),
        validators.DataRequired(message="Address name is required")
    ])
    location = StringField("Location", [
        validators.Length(16, 256, message="Location must be between 16 to 256 characters"),
        validators.DataRequired(message="Location is required")
    ])

    submit = SubmitField("Edit Address")


class deleteUserForm(Form):
    name = StringField("Account Name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required")
    ])

    submit = SubmitField("Confirm Delete")


# ADMIN TREATMENT FORMS

class searchTreatmentsForm(Form):
    name = StringField("Search by treatment name", [
        validators.Length(3, 128, message="Treatment name must be between 3 to 128 characters"),
        validators.DataRequired(message="Treatment name is required to search")
    ])


class createTreatmentForm(Form):
    name = StringField("Treatment Name", [
        validators.Length(3, 128, message="Treatment name must be between 3 to 128 characters"),
        validators.DataRequired(message="Treatment name is required to search")
    ])
    price = DecimalField("Treatment Price ($)", [
        validators.DataRequired(message="Treatment price is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    salePrice = DecimalField("Sale Price ($)", [
        validators.DataRequired(message="Sale price is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    onSale = BooleanField("On Sale?", [
        validators.optional()
    ])
    description = TextAreaField("Treatment Description", [
        validators.DataRequired(message="Treatment description is required")
    ])
    benefits = TextAreaField("Treatment Benefits", [
        validators.DataRequired(message="Treatment benefits is required")
    ])
    duration = DecimalField("Duration in Hours", [
        validators.DataRequired(message="Treatment duration is required"),
        validators.NumberRange(0.5, 6, message="Treatment duration must be between 0.5 hours and 6 hours")
    ], render_kw={"step": "0.5"})
    images = MultipleFileField("Treatment Images", [
        # validators.regexp(".(jpe?g|png|webp)$/i", message="Invalid file extension, only PNG, JPG or WEBP files allowed.")
        # validators.DataRequired(message="Treatment Images are required")
    ], render_kw={
        "required": "true",
        "accept": "image/jpg, image/jpeg, image/webp, image/png"
    })

    submit = SubmitField("Add Treatment")

    def validate_images(form, images):
        print(form.images.data)

    def validate_salePrice(form, salePrice):
        if form.salePrice.data >= form.price.data:
            raise ValidationError("Sale price cannot exceed normal price")


class editTreatmentForm(Form):
    name = StringField("Treatment Name", [
        validators.Length(3, 128, message="Treatment name must be between 3 to 128 characters"),
        validators.DataRequired(message="Treatment name is required to search")
    ])
    price = DecimalField("Treatment Price ($)", [
        validators.DataRequired(message="Treatment price is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    salePrice = DecimalField("Sale Price ($)", [
        validators.DataRequired(message="Sale price is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    onSale = BooleanField("On Sale?", [
        validators.optional()
    ])
    description = TextAreaField("Treatment Description", [
        validators.DataRequired(message="Treatment description is required")
    ])
    benefits = TextAreaField("Treatment Benefits", [
        validators.DataRequired(message="Treatment benefits is required")
    ])
    duration = DecimalField("Duration in Hours", [
        validators.DataRequired(message="Treatment duration is required"),
        validators.NumberRange(0.5, 6, message="Treatment duration must be between 0.5 hours and 6 hours"),
    ], render_kw={"step": "0.5"})

    submit = SubmitField("Edit Treatment")

    def validate_salePrice(form, salePrice):
        if form.salePrice.data >= form.price.data:
            raise ValidationError("Sale price cannot exceed normal price")


class uploadImageForm(Form):
    images = MultipleFileField("Product Images", [
        # validators.regexp(".(jpe?g|png|webp)$/i", message="Invalid file extension, only PNG, JPG or WEBP files allowed.")
        # validators.DataRequired(message="Treatment Images are required")
    ], render_kw={
        "required": "true",
        "accept": "image/jpg, image/jpeg, image/webp, image/png"
    })

    submit = SubmitField("Upload Images")


class searchTracker(Form):
    name = StringField("Search by patient's name", [
        validators.Length(3, 128, message="Patients name must be between 3 to 128 characters"),
        validators.DataRequired(message="Patients name is required to search")
    ])


class createMedicationForm(Form):
    name = StringField("Medicine Name", [
        validators.Length(3, 128, message="Medicine name must be between 3 to 128 characters"),
        validators.DataRequired(message="Medicine name is required to search")
    ])
    description = StringField('Description', [
        validators.Length(3, 128, message="Description of medication must be between 3 to 128 characters"),
        validators.DataRequired(message="Description of medication is required")
    ])
    duration = SelectField("Duration",
                           [validators.DataRequired(message="Duration of the medication is required")],
                           choices=[(1, '1 days'), (2, '2 days'), (3, '3 days'), (4, '4 days'),
                                    (5, '5 days'), (6, '6 days'), (7, 'One week'),
                                    (14, 'Two weeks')])
    pills = SelectField('Dosage',
                        [validators.DataRequired(message="Pills per dosage of the medication is required")],
                        choices=[(1, '1 Tablet(s)'), (2, '2 Tablet(s)'),
                                 (3, '3 Tablet(s)'),
                                 (4, '4 Tablet(s)'), (5, '5 Tablet(s)'),
                                 (6, '6 Tablet(s)')])
    frequency_of_pills = SelectField('No. of times',
                                     [validators.DataRequired(message="Dosage of the medication is required")],
                                     choices=[(1, '1 times a day'),
                                              (2, '2 times a day'),
                                              (3, '3 times a day')])
    additional_notes = TextAreaField("Additional Notes", [
        validators.optional()
    ])
    submit = SubmitField("Add Medicine")


class editMedicationForm(Form):
    name = StringField("Medicine Name", [
        validators.Length(3, 128, message="Medicine name must be between 3 to 128 characters"),
        validators.DataRequired(message="Medicine name is required to search")
    ])
    description = StringField('Description', [
        validators.Length(3, 128, message="Description of medication must be between 3 to 128 characters"),
        validators.DataRequired(message="Description of medication is required")
    ])
    duration = SelectField("Duration",
                           [validators.DataRequired(message="Duration of the medication is required")],
                           choices=[(1, '1 days'), (2, '2 days'), (3, '3 days'), (4, '4 days'),
                                    (5, '5 days'), (6, '6 days'), (7, 'One week'),
                                    (14, 'Two weeks')])
    pills = SelectField('Dosage',
                        [validators.DataRequired(message="Pills per dosage of the medication is required")],
                        choices=[(1, '1 Tablet(s)'), (2, '2 Tablet(s)'),
                                 (3, '3 Tablet(s)'),
                                 (4, '4 Tablet(s)'), (5, '5 Tablet(s)'),
                                 (6, '6 Tablet(s)')])
    frequency_of_pills = SelectField('No. of times',
                                     [validators.DataRequired(message="Dosage of the medication is required")],
                                     choices=[(1, '1 times a day'),
                                              (2, '2 times a day'),
                                              (3, '3 times a day')])
    additional_notes = TextAreaField("Additional Notes", [
        validators.optional()
    ])
    submit = SubmitField("Save Medicine")

class openingHoursForm(Form):
    opening = TimeField("Opening Hour", [
        validators.DataRequired(message="Opening Hours are required")
    ])
    closing = TimeField("Closing Hour", [
        validators.DataRequired(message="Closing Hours are required")
    ])

    def validate_opening(form, opening):
        if form.opening.data > form.closing.data:
            raise ValidationError("Opening time cannot exceed closing time")

    def validate_closing(form, closing):
        if form.closing.data < form.opening.data:
            raise ValidationError("Closing time cannot be earlier than opening time")

    submit = SubmitField("Edit Hours")


# Coupon forms
class searchCouponsForm(Form):
    name = StringField("Search by coupon name", [
        validators.Length(3, 128, message="Coupon name must be between 3 to 128 characters"),
        validators.DataRequired(message="Coupon name is required to search")
    ])


class createCouponForm(Form):
    name = StringField("Coupon Name", [
        validators.Length(3, 128, message="Coupon name must be between 3 to 128 characters"),
        validators.DataRequired(message="Coupon name is required")
    ])
    description = TextAreaField("Coupon Description", [
        validators.Optional()
    ])
    code = StringField("Coupon Code", [
        validators.Length(3, 64, message="Coupon code must be between 3 to 64 characters"),
        validators.DataRequired(message="Coupon code is required")
    ])
    discount = IntegerField("Discount Amount (%)", [
        validators.NumberRange(1, 100, "Discount amount must range between 1% to 100%"),
        validators.DataRequired(message="Discount amount is required"),
    ])
    startDate = DateField("Start Date", [
        validators.DataRequired(message="Discount start date is required")
    ])
    endDate = DateField("End Date", [
        validators.DataRequired(message="Discount end date is required")
    ])

    submit = SubmitField("Add Coupon")

    def validate_startDate(form, startDate):
        if form.startDate.data < datetime.now().date():
            raise ValidationError("Coupon start date cannot be earlier than current date")
        elif form.startDate.data > form.endDate.data:
            raise ValidationError("Coupon start date cannot exceed end date")

    def validate_endDate(form, endDate):
        if form.endDate.data < datetime.now().date():
            raise ValidationError("Coupon end date cannot be earlier than current time")


class editCouponForm(Form):
    name = StringField("Coupon Name", [
        validators.Length(3, 128, message="Coupon name must be between 3 to 128 characters"),
        validators.DataRequired(message="Coupon name is required")
    ])
    description = TextAreaField("Coupon Description", [
        validators.Optional()
    ])
    code = StringField("Coupon Code", [
        validators.Length(3, 64, message="Coupon code must be between 3 to 64 characters"),
        validators.DataRequired(message="Coupon code is required")
    ])
    discount = IntegerField("Discount Amount (%)", [
        validators.NumberRange(1, 100, "Discount amount must range between 1% to 100%"),
        validators.DataRequired(message="Discount amount is required")
    ])
    startDate = DateField("Start Date", [
        validators.DataRequired(message="Discount start date is required")
    ])
    endDate = DateField("End Date", [
        validators.DataRequired(message="Discount end date is required")
    ])

    submit = SubmitField("Edit Coupon")

    def validate_startDate(form, startDate):
        if form.startDate.data > form.endDate.data:
            raise ValidationError("Coupon start date cannot exceed end date")

    def validate_endDate(form, endDate):
        if form.endDate.data < datetime.now().date():
            raise ValidationError("Coupon end date cannot be earlier than current time")


class searchAppointmentsForm(Form):
    name = StringField("Search by appointment name", [
        validators.Length(3, 128, message="Appointment name must be between 3 to 128 characters"),
        validators.DataRequired(message="Appointment name is required to search")
    ])


class createAppointmentForm(Form):
    name = StringField("Appointment Name", [
        validators.Length(3, 128, message="Appointment name must be between 3 to 128 characters"),
        validators.DataRequired(message="Appointment name is required")
    ])
    userEmail = EmailField("User E-mail Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail Address is required")
    ], render_kw={
        "autocomplete": "off"
    })
    date = DateField("Appointment Date", [
        validators.DataRequired("Appointment date is required")
    ])
    time = TimeField("Start Time", [
        validators.DataRequired("Appointment start time is required")
    ])
    endTime = TimeField("End Time", [
        validators.DataRequired("Appointment end time is required")
    ])
    notes = TextAreaField("Additional Notes", [
        validators.Optional()
    ])

    submit = SubmitField("Add Appointment")

    def validate_userEmail(form, userEmail):
        with shelve.open("users") as users:
            if form.userEmail.data not in users.keys():
                raise ValidationError("User with associated e-mail does not exist")

    def validate_date(form, date):
        if form.date.data < datetime.now().date():
            raise ValidationError("Appointment date cannot be in the past")

    def validate_time(form, time):
        with shelve.open("data", writeback=True) as data:
            if form.time.data < data["opening"] or form.time.data > data["closing"]:
                raise ValidationError("Appointment start time cannot be set outside of operating hours.")

            if form.time.data >= form.endTime.data:
                raise ValidationError("Appointment start time cannot exceed end time.")

    def validate_endTime(form, endTime):
        with shelve.open("data", writeback=True) as data:
            if form.time.data < data["opening"] or form.time.data > data["closing"]:
                raise ValidationError("Appointment end time cannot be set outside of operating hours.")


# PRODUCT FORMS

class searchProductForm(Form):
    name = StringField("Search by name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required to search")
    ])


class addProductForm(Form):
    name = StringField("Product Name", [
        validators.Length(3, 128, message="Treatment name must be between 3 to 128 characters"),
        validators.DataRequired(message="Treatment name is required")
    ])
    price = DecimalField("Product Price ($)", [
        validators.DataRequired(message="Product price is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    salePrice = DecimalField("Sale Price ($)", [
        validators.DataRequired(message="Sale price is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    onSale = BooleanField("On Sale?", [
        validators.optional()
    ])
    qty = DecimalField("Stock", [
        validators.DataRequired(message="Stock quantity is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    description = TextAreaField("Product Description", [
        validators.DataRequired(message="Treatment description is required")
    ])
    benefits = TextAreaField("Product Benefits", [
        validators.DataRequired(message="Treatment benefits is required")
    ])
    images = MultipleFileField("Product Images", [
        # validators.regexp(".(jpe?g|png|webp)$/i", message="Invalid file extension, only PNG, JPG or WEBP files allowed.")
        # validators.DataRequired(message="Treatment Images are required")
    ], render_kw={
        "required": "true",
        "accept": "image/jpg, image/jpeg, image/webp, image/png"
    })

    def validate_salePrice(form, salePrice):
        if form.salePrice.data >= form.price.data:
            raise ValidationError("Sale price cannot exceed or equal to normal price")

    submit = SubmitField("Add Product")


class editProductForm(Form):
    name = StringField("Product Name", [
        validators.Length(3, 100, message="Product name must be between 3 to 100 characters"),
        validators.DataRequired(message="Product name is required")
    ])
    price = DecimalField("Product Price ($)", [
        validators.DataRequired(message="Treatment price is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    description = TextAreaField("Product Description", [
        validators.DataRequired(message="Treatment description is required")
    ])
    benefits = TextAreaField("Product Benefits", [
        validators.DataRequired(message="Treatment benefits is required")
    ])
    salePrice = DecimalField("Sale Price ($)", [
        validators.DataRequired(message="Sale price is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    qty = IntegerField("Stock", [
        validators.InputRequired(message="Stock quantity is required"),
        validators.NumberRange(min=0, message="Number must be positive")
    ])
    onSale = BooleanField("On Sale?", [
        validators.optional()
    ])

    submit = SubmitField("Edit Product")

    def validate_salePrice(form, salePrice):
        if form.salePrice.data >= form.price.data:
            raise ValidationError("Sale price cannot exceed or equal to normal price")



class CartCouponForm(Form):
    coupon = StringField("Coupon Code (Optional)", [
        validators.Optional()
    ])

    submit = SubmitField("Checkout")

    def validate_coupon(form, coupon):
        if form.coupon.data != "":
            if not checkCoupon(form.coupon.data):
                raise ValidationError("Invalid coupon. The coupon has probably been expired")


class CheckoutForm(Form):
    # Form is only there to be filled with data, javascript handles checkout
    delivery = SelectField("Delivery Address", [
        validators.DataRequired()
    ])


# ADMIN BLOG FORMS
class createArticleForm(FlaskForm):
    title = StringField("Title", [
        validators.Length(3, 64, message="Blog title must be between 3 to 64 characters."),
        validators.DataRequired(message="Blog title is required.")
    ])
    brief = StringField("Brief Description", [
        validators.Length(3, 128, message="Brief description must be between 3 to 128 characters."),
        validators.DataRequired(message="Brief description is required.")
    ])
    content = TextAreaField("Article Content", [
        validators.DataRequired(message="Article content is required.")
    ])
    articleImage = FileField("Article Cover Image", validators=[
        FileRequired("Cover image is required"),
        FileAllowed(['jpg', 'png', 'webp'], message='Images files only!'),
    ])

    submit = SubmitField("Create Article")


class editArticleForm(FlaskForm):
    title = StringField("Title", [
        validators.Length(3, 64, message="Blog title must be between 3 to 64 characters."),
        validators.DataRequired(message="Blog title is required.")
    ])
    brief = StringField("Brief Description", [
        validators.Length(3, 128, message="Brief description must be between 3 to 128 characters."),
        validators.DataRequired(message="Brief description is required.")
    ])
    content = TextAreaField("Article Content", [
        validators.DataRequired(message="Article content is required.")
    ])
    articleImage = FileField("Article Cover Image", validators=[
        validators.Optional(),
        FileAllowed(['jpg', 'png', 'webp'], message='Images files only!'),
    ])

    submit = SubmitField("Save")


class searchBlogForm(Form):
    name = StringField("Search by title", [
        validators.Length(3, 64, message="Blog title must be between 3 to 64 characters"),
        validators.DataRequired(message="Blog title is required to search")
    ])


class editBlogForm(Form):
    title = StringField("Title", [
        validators.Length(3, 64, message="Blog title must be between 3 to 64 characters."),
        validators.DataRequired(message="Blog title is required.")
    ])
    content = TextAreaField("Article Content", [
        validators.DataRequired(message="Article content is required.")
    ])
    articleImage = FileField("Article Cover Image", [])

    submit = SubmitField("Edit Article")

class addRefundForm(Form):
    reason = TextAreaField('Reason for refund', [
        validators.DataRequired(message='Reason is required to continue with refund')
    ])
    submit = SubmitField("Request")

class searchRefundForm(Form):
    name = StringField("Search by name", [
        validators.Length(3, 64, message="Name must be between 3 to 64 characters"),
        validators.DataRequired(message="Name is required to search")
    ])

class editRefundForm(Form):
    fname = StringField('First Name', [
        validators.DataRequired(message='Please input your first name.')
    ])
    lname = StringField('Last Name', [
        validators.DataRequired(message='Please input your last name.')
    ])
    email = EmailField('Email Address', [
        validators.Email(granular_message=True),
        validators.DataRequired(message='E-mail is required to continue with refund')
    ])
    order = StringField('Product name', [
        validators.DataRequired(message='Order number is required to continue with refund')
    ])
    reason = TextAreaField('Reason for refund', [
        validators.DataRequired(message='Reason is required to continue with refund'),
        validators.optional()
    ])
    submit = SubmitField("Edit Refund")


# how to update a previously existing blog using this function?


class createEnquiryForm(Form):
    name = StringField("Name", [
        validators.Length(3, 128, message="Medicine name must be between 3 to 128 characters"),
        validators.DataRequired(message="Name is required")
    ])
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="E-mail is required to contact us")
    ])
    purpose = SelectField('Purpose',
                          [validators.DataRequired(message="Purpose is required")],
                          choices=[("", 'Select a Purpose'), ('Products Question', 'Products Question'),
                                   ('Feedback / Feature Request', 'Feedback / Feature Request'),
                                   ('General Questions', 'General Questions')], default="")

    subject = StringField("Subject", [
        validators.Length(3, 128, message="Subject must be between 3 to 128 characters"),
        validators.DataRequired(message="Subject is required")
    ])
    enquiry = TextAreaField("Enquiry", [
        validators.Length(3, message="Your enquiry needs to be more than 3 characters"),
        validators.DataRequired(message="Enquiry is required")
    ])
    submit = SubmitField("Submit")

class searchEnquiry(Form):
    name = StringField("Search by email", [
        validators.Length(3, 128, message="Email must be between 3 to 128 characters"),
        validators.DataRequired(message="Email is required to search")
    ])


class bookAppointmentForm(Form):
    date = DateField("Appointment Date", [
        validators.DataRequired(message="Appointment date is required")
    ])
    startTime = TimeField("Appointment Time", [
        validators.DataRequired(message="Appointment time is required")
    ])
    doctor = SelectField("Consulting Doctor", [
        validators.DataRequired(message="Consultation doctor is required")
    ])

    submit = SubmitField("Book")

    def validate_date(form, date):
        if form.date.data <= datetime.now().date():
            raise ValidationError("Appointment date cannot be in the past and can only be made from tomorrow onwards")

    def validate_startTime(form, startTime):
        with shelve.open("data") as data:
            if data["opening"] > form.startTime.data >= data["closing"]:
                raise ValidationError("Appointment start time cannot exceed operating hours")


class searchOrdersForm(Form):
    id = StringField("Search by order ID", [
        validators.DataRequired(message="Order ID is required to search")
    ])

class editOrdersStatusForm(Form):
    status = SelectField("Order Status", [
        validators.DataRequired(message="Order status required to update")
    ])

    submit = SubmitField("Save")

class addProductCartForm(Form):
    qty = IntegerField("Quantity", default=1)
    submit = SubmitField("Add to Cart")

class sendEmailForm(Form):
    email = EmailField('To', [validators.DataRequired()])
    subject = StringField('Subject', [validators.DataRequired()])
    message = TextAreaField('Message', [validators.DataRequired()])

    submit = SubmitField('Send Email')
