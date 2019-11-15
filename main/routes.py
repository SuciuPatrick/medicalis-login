from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def  profile():
    name = current_user.name
    if current_user.confirmed is False:
        flash('Email not confirmed yet.')
    return render_template('profile.html', name=name)
