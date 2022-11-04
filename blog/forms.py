from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp
from blog.models import User, Post

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators = [DataRequired(), Regexp('^[a-zA-Z0-9]{1,20}$', message = 'Your first name contain invalid characters.')])
    email = StringField('Email', validators = [DataRequired(), Regexp('^[a-zA-Z0-9]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$', message = 'Invalid email. Please check.')])
    password = PasswordField('Password', validators = [DataRequired(), Regexp('^[a-zA-Z0-9]{1,20}$', message = 'Your password contains invalid characters.')])
    confirm_password = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password', message = 'Passwords do not match. Please try again.')])
    submit = SubmitField('Register')


    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('This email has already been used. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class SortForm(FlaskForm):
    date_order = SelectField('How do you want to sort these posts?', choices = [('date_asc', ' by ascending date'), ('date_desc', ' by descending date')])
    submit = SubmitField('Confirm')

class AddCommentForm(FlaskForm):
    rating = RadioField('Rating stars', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    comment = TextAreaField('Comment')
    submit = SubmitField('Post')    