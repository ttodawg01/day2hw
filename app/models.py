from datetime import datetime
from app import db

#creating a user class
class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    # def __repr__(self):
    #     return '<User %r>' % self.username

    # def __repr__(self):
    #     return '<User %r>' % self.username