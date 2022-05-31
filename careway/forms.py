from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Email,Length,EqualTo, ValidationError
from careway.models import User


class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2, max=20)] )
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please choose another name!')

    def validate_email(self,email):
        
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose another name!')



class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class RequestResetForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request password reset')

    def validate_email(self,email):
        
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with than email. Please register first.')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Reset Password')

class UserInterestForm(FlaskForm):
    interest=StringField('Interest')
    edu_interest=StringField('Education Interest')
    submit=SubmitField('Predict')