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