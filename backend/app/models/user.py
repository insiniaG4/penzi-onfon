from app.extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    education_level = db.Column(db.String(50))
    profession = db.Column(db.String(100))
    marital_status = db.Column(db.String(20))
    religion = db.Column(db.String(50))
    ethnicity = db.Column(db.String(50))
    self_description = db.Column(db.Text)
    registration_status = db.Column(db.String(20), default='incomplete')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<User {self.username}>'