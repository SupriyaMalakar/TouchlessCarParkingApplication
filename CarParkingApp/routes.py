import pyqrcode 
import png 
from flask import render_template, url_for, flash, redirect,request
from CarParkingApp import app, db, bcrypt
from CarParkingApp.forms import RegistrationForm, LoginForm,AvailabilityForm
from CarParkingApp.models import User, ParkingLot
from flask_login import login_user,current_user,logout_user,login_required
from pyqrcode import QRCode 

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/availability")
def availability():
    form = AvailabilityForm()
    
    return render_template('availability.html', title='availability', form=form)    

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(Phone_number=form.Phone_number.data, email=form.email.data, car_number=form.car_number.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can now login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        
    return render_template('login.html', title='Login', form=form)    

@app.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account(): 
     return render_template('account.html', title='Account')

@app.route("/myTicket")
@login_required
def myTicket(): 
    url = pyqrcode.create(current_user.car_number) 
    image=url.png('CarParkingApp\static\myqr.png', scale = 6)
    return render_template('myTicket.html', title='My Ticket')     

        
