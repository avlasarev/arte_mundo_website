from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt
from app.models import User, Image, Property
from app.forms import RegistrationForm, LoginForm, PropertyForm
import os
from werkzeug.utils import secure_filename
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Property, Image
from app.forms import PropertyForm
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


@app.route('/')
def index():
    properties = Property.query.all()
    return render_template('index.html', properties=properties)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_property():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

    form = PropertyForm()
    if form.validate_on_submit():
        try:
            new_property = Property(
                title=form.title.data,
                description=form.description.data,
                price=float(form.price.data),
                location=form.location.data,
                image_url='uploads/' + secure_filename(form.image.data.filename)
            )
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], new_property.image_url.split('/')[-1]))
            db.session.add(new_property)
            db.session.commit()

            # Add multiple images
            for img in form.images.data:
                image_file = secure_filename(img.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
                img.save(image_path)
                image_url = 'uploads/' + image_file
                new_image = Image(image_url=image_url, property=new_property)
                db.session.add(new_image)

            db.session.commit()
            flash('Property added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding property: {str(e)}', 'danger')
        finally:
            db.session.close()

        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:property_id>', methods=['POST'])
@login_required
def delete_property(property_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))

    property_to_delete = Property.query.get_or_404(property_id)
    db.session.delete(property_to_delete)
    db.session.commit()
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query')
    properties = Property.query.filter(
        Property.title.contains(query) | Property.description.contains(query) | Property.location.contains(query)).all()
    return render_template('index.html', properties=properties)

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property_detail.html', property=property)