import qrcode
import base64
import logging
from io import BytesIO
from flask import render_template, url_for, flash, redirect, request
from CarParkingApp import app, db, bcrypt
from CarParkingApp.forms import RegistrationForm, LoginForm, AvailabilityForm
from CarParkingApp.models import User, ParkingLot
from flask_login import login_user,current_user,logout_user,login_required
#from pyqrcode import QRCode 

@app.route("/")
@app.route("/home")
def home():
    #db.create_all()
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/slots")
def slots():
    return render_template('slots.html', title='Slots')    

@app.route("/availability")
@login_required
def availability():
    form = AvailabilityForm()
    if form.validate_on_submit():
        return redirect(url_for('slots'))
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
        #app.logger.info(f"{url_for('login')}")
        return render_template('home.html')
        #return render_template('login.html',form=form)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        #return redirect(url_for('home'))
        return render_template('home.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            app.logger.info(f"{url_for('home')}")
            #return redirect(next_page) if next_page else redirect(url_for('home'))
            return redirect(next_page) if next_page else render_template('home.html')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
        
    return render_template('login.html', title='Login', form=form)    

@app.route("/logout")
@login_required
def logout():   
    logout_user()
    #app.logger.info(f"{url_for('home')}")
    #return redirect(url_for('home'))
    return render_template('home.html')
    
    

@app.route("/account")
@login_required
def account(): 
     return render_template('account.html', title='Account')

@app.route("/myTicket")
@login_required
def myTicket(): 
    #url = pyqrcode.create(current_user.car_number) 
    #image=url.png('CarParkingApp\Image\myqr.png', scale = 6)
    img = qrcode.make(current_user.car_number)
    #data=base64.b64encode(img.getvalue())
    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)


    return render_template('myTicket.html', data=im_b64)     

        
