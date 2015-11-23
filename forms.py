from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class SignUpForm(Form):
    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired(),
                                 EqualTo("password2")
                             ])
    password2 = PasswordField("Confirm Password",
                                     validators=[
                                         DataRequired()
                                     ])


class LoginForm(Form):

    email = StringField("Email",
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired()
                             ])


class TacoForm(Form):
    protein = StringField("Protein")
    shell = StringField("Shell")
    cheese = BooleanField("With Cheese")
    extras = TextAreaField("Extras")
