import datetime
import shelve

from wtforms import Form, StringField, PasswordField, RadioField, validators, EmailField, DateField, ValidationError, \
    SubmitField, TextAreaField, IntegerField, DecimalField, BooleanField, MultipleFileField
from functions import allowedFile


# Put all forms here with a comment describing the form

# ADMIN USERS FORMS

# Sample form for testpage
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

    submit = SubmitField("Register an account")

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
        validators.regexp("^[689]\d{7}$", message="Phone number must a number that starts with the number 6, 8 or 9 and 8 digits long")
    ])
    submit = SubmitField("Edit User")

    def validate_birthday(form, birthday):
        if form.birthday.data > datetime.date.today():
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
        validators.regexp("^[689]\d{7}$", message="Phone number must a number that starts with the number 6, 8 or 9 and 8 digits long")
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
        if form.birthday.data > datetime.date.today():
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
        validators.DataRequired(message="Treatment price is required")
    ])
    salePrice = DecimalField("Sale Price ($)", [
        validators.DataRequired(message="Sale price is required")
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
    duration = DecimalField("Treatment Duration", [
        validators.DataRequired(message="Treatment duration is required"),
        validators.NumberRange(0.5, 6, message="Treatment duration must be between 0.5 hours and 6 hours")
    ])
    images = MultipleFileField("Treatment Images", [
        #validators.regexp(".(jpe?g|png|webp)$/i", message="Invalid file extension, only PNG, JPG or WEBP files allowed.")
        #validators.DataRequired(message="Treatment Images are required")
    ])

    submit = SubmitField("Add Treatment")

    def validate_images(form, images):
        print(form.images.data)


class editTreatmentForm(Form):
    name = StringField("Treatment Name", [
        validators.Length(3, 128, message="Treatment name must be between 3 to 128 characters"),
        validators.DataRequired(message="Treatment name is required to search")
    ])
    price = DecimalField("Treatment Price ($)", [
        validators.DataRequired(message="Treatment price is required")
    ])
    salePrice = DecimalField("Sale Price ($)", [
        validators.DataRequired(message="Sale price is required")
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
    duration = DecimalField("Treatment Duration", [
        validators.DataRequired(message="Treatment duration is required"),
        validators.NumberRange(0.5, 6, message="Treatment duration must be between 0.5 hours and 6 hours")
    ])

    submit = SubmitField("Edit Treatment")

class uploadImageForm(Form):
    images = MultipleFileField("Treatment Images", [
        # validators.regexp(".(jpe?g|png|webp)$/i", message="Invalid file extension, only PNG, JPG or WEBP files allowed.")
        # validators.DataRequired(message="Treatment Images are required")
    ])

    submit = SubmitField("Upload Images")

class CheckoutForm(Form):
    Fname: StringField("First Name:", [

    ])
    Lname: StringField("Last Name:", [

    ])
    Cnumber: StringField("Card Number:", [
        validators.Length(16, message="Card number must be 16 digits"),
        validators.DataRequired(message="Card number is required for purchase")
    ])
    CVV: StringField("CVV:", [
        validators.Length(3, message="CVV must be 3 digits"),
        validators.DataRequired(message="CVV is required for purchase")
    ])
    Expiry: StringField("Expiry Date:", [
        validators.Length(2,3, message="Expiry date must in numerals"),
        validators.DataRequired(message="Card Expiry Date is required for purchase")
    ])
    Shipping: StringField("", [

    ])
    Voucher: StringField("", [

    ])