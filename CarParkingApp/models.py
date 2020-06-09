from datetime import datetime
from CarParkingApp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    



class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    Phone_number = db.Column(db.String(10), unique=True, nullable=False)
    car_number = db.Column(db.String(11), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    ParkingLot = db.relationship('ParkingLot', backref='Owner', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.Phone_number}', '{self.email}', '{self.image_file}')"


class ParkingLot(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ParkingLot_id = db.Column(db.Integer)
    ParkingLot_name = db.Column(db.String(100), nullable=False)
    Entry_Time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Exit_Time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.String(11), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.car_number}', '{self.Entry_Time}')"