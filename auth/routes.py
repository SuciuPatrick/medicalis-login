from flask import render_template, redirect, url_for, request, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from project.models import User
from project import db
from . import auth
from project.email import send_email
from .forms import LoginForm, SignUpForm, ChangePasswordForm
# from ..email import send_email


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html', form=LoginForm())


def __flashErrors(errorItems):
    for error in errorItems:
        flash(error[1][0]) 


@auth.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.profile'))
        
        flash('User not found!')
    __flashErrors(form.errors.items())
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html', form=SignUpForm())


@auth.route('/signup', methods=['POST'])
def signup_post():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            name=form.name.data.strip(),
            password=form.password.data,
            doctor=form.doctor.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.', 'succes')
        login_user(user)
        return redirect(url_for('main.profile'))
    __flashErrors(form.errors.items())
    return redirect(url_for('auth.signup'))


@auth.route('/confirm/<token>')
def confirm(token):
    email = User.confirm_email(token)
    if email is False:
        flash('Token expired. Resend a new confirmation email from your profile page.')
        return redirect(url_for(('main.profile')))
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Something went terribly wrong.')
        return redirect(url_for(('main.index')))
    user.confirm_user()
    flash('Confirmation successful!', 'succes')
    if current_user.is_authenticated and current_user.email == user.email:
        return redirect(url_for(('main.profile')))
    return redirect(url_for(('auth.login')))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'info')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))