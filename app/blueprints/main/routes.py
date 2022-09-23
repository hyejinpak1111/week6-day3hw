from . import bp as app
from flask import render_template, request, redirect, url_for, flash
from app.blueprints.main.models import User, Post, Car
from app import db
from flask_login import current_user, login_required

# Routes that return/display HTML

@app.route('/')
@login_required
def home():
    cars = Car.query.all()

    return render_template('home.html', user=current_user, cars=cars)

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/blog')
@login_required
def blog():
    return render_template('blog.html')

@app.route('/post', methods=['POST'])
@login_required
def create_post():
    post_make = request.form['make']
    post_model = request.form['model']
    post_year = request.form['year']
    post_color = request.form['color']
    post_price = request.form['price']
    
    new_car = Car(make=post_make, model=post_model, year=post_year, color=post_color, price=post_price, user_id=current_user.id)

    db.session.add(new_car)
    db.session.commit()

    flash('Post added successfully', 'success')
    return redirect(url_for('main.home'))

@app.route('/post/<id>')
def car(id):
    single_post = Car.query.get(id)
    return render_template('single-post.html', car=single_post)