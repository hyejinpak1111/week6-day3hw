from . import bp as app
from app.blueprints.main.models import User
from app import db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.blueprints.auth.forms import SignupForm, SigninForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SigninForm()

    if request.method == 'GET':
        return render_template('login.html', form = form)
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('A user with this email does not exists.', 'danger')
        elif not user.check_my_password(password):
            flash('The password was incorrect.', 'danger')
        else:
            flash('Logged in successfully', 'success')
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid form data.')
        return redirect(url_for('main.home'))

    return render_template('login.html', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()

    if request.method == 'GET':
        return render_template('register.html', form = form)
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data
            confirm_password = form.confirm_password.data

            # A user with this email already exists
            # A user with this email does not exist, but the passwords do not match
            # A user with this email does not exist, and the passwords match - REGISTER THE USER
            check_user = User.query.filter_by(email=email).first()

            if check_user is not None:
                flash('A user with this email already exists.', 'danger')

            elif password != confirm_password:
                flash('The passwords do not match', 'danger')

            new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, password='')
            new_user.hash_my_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully', 'success')
            return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid form data.')

    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('User logged out', 'success')
    return redirect(url_for('auth.login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("You can't access this page without logging in.", 'danger')
    return redirect(url_for('auth.login'))
