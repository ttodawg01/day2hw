from datetime import datetime
from flask_login import UserMixin
from app import db, login

#creating a user class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    posts = db.relationship('Address', backref='author', lazy= 'dynamic')

    # def __init__(self, **kwargs):
    #     super(),__init__()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.first_name

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#create a address model --One To Many.. One user to many addresses

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()


    #update method for the address object
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'address'}:
                setattr(self, key, value)
        db.session.commit()

     # Delete post from database
    def delete(self):
        db.session.delete(self)
        db.session.commit()