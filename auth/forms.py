from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from project.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,50), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,50), Email()], render_kw={"placeholder": "Email"})
    name = StringField(u'Full Name', validators=[DataRequired(), Regexp('^[A-Za-z ]*$', 0, 
    'Name must have only letters and spaces.'), Length(1,100)], render_kw={"placeholder": "Full Name"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message="Passwords must match.")], render_kw={"placeholder": "Password"})
    password_confirm = PasswordField('Confirm password', validators=[DataRequired()], render_kw={"placeholder": "Confirm password"})
    doctor = BooleanField('I am a doctor.')
    submit = SubmitField('Sign up')

    def validate_email(self, input_email):
        if User.query.filter_by(email=input_email.data).first():
            raise ValidationError('Email already in use.')
        
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()], render_kw={"placeholder": "Current password"})
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Password must match.')], render_kw={"placeholder": "New password"})
    password2 = PasswordField('Confirm new password', validators=[DataRequired()], render_kw={"placeholder": "Verify new password"})
    submit = SubmitField('Update password')
