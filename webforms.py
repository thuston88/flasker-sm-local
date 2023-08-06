from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, Form, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
# from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

# Create A Search Form
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create Login Form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")


# Create a Form Class
class UserForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField("Submit")


class SelectForm(FlaskForm):
	institution = SelectField("Institution")
	acct_type = SelectField("Account Type")
	acct_no = SelectField("Account Number")
	submit = SubmitField("Submit")

class SimpleForm(FlaskForm):
	institution = SelectField("Institution")
	submit = SubmitField("Submit")


# Create a Posts Form
class PostForm(FlaskForm):
	institution = StringField("Institution")
	acct_type = StringField("Account Type")
	acct_number = StringField("Account Number")
	acct_balance = StringField("Account Balance")
	access_type = StringField("Access Type")
	access_app = StringField("Access App")
	acct_id = StringField("Account User Id")
	acct_pw = StringField("Account Password")
	comment = StringField("Comment")
	extra = StringField("Extra")
	submit = SubmitField("Submit")


"""
# Create a Form Class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")
"""

	# BooleanField
	# DateField
	# DateTimeField
	# DecimalField
	# FileField
	# HiddenField
	# MultipleField
	# FieldList
	# FloatField
	# FormField
	# IntegerField
	# PasswordField
	# RadioField
	# SelectField
	# SelectMultipleField
	# SubmitField
	# StringField
	# TextAreaField

	## Validators
	# DataRequired
	# Email
	# EqualTo
	# InputRequired
	# IPAddress
	# Length
	# MacAddress
	# NumberRange
	# Optional
	# Regexp
	# URL
	# UUID
	# AnyOf
	# NoneOf
