from wtforms import Form, StringField, PasswordField, RadioField, SelectField, validators

# Put all forms here with a comment describing the form

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
    username = StringField("Username", [
        validators.Length(3, 64, message="Username must be between 3 to 64 characters"),
        validators.DataRequired(message="Username is required")
    ])
    password = PasswordField("Password", [
        validators.Length(8, 64, message="Password must be at least 8 characters"),
        validators.DataRequired(message="Password is required")
    ])

# User registration form
class registerUserForm(Form):
    username = StringField("Username", [
        validators.Length(3, 64, message="New username must be between 3 to 64 characters"),
        validators.DataRequired(message="Username is required for registration")
    ])
    password = PasswordField("Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.Regexp("(?=.*[A-Z])", message="New password should contain at least 1 uppercase letter"),
        validators.DataRequired(message="Password is required for registration")
    ])
    confirmPassword = PasswordField("Confirm Password", [
        validators.Length(8, 64, message="New password must be between 8 to 64 characters"),
        validators.equal_to("password", message="New password and confirm password fields do not match.")
    ])
    email = StringField("Email Address", [
        validators.Email(granular_message=True)
    ], render_kw={
        "type": "email"
    })


