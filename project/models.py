from sqlalchemy import Column, Integer, String, Date, Boolean
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
from flask_login import UserMixin
from . import db, login_manager
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    doctor = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt=current_app.config['SECRET_SALT'])

    @staticmethod
    def confirm_email(token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=current_app.config['SECRET_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email

    def confirm_user(self):
        self.confirmed = True
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return "<Book(id='{}', email='{}', name={}, password={}, admin={}, doctor={})>"\
                .format(self.id, self.public_id, self.name, self.password_hash, self.admin, self.doctor)


    @property
    def password(self):
        raise AttributeError("Attribute is not readable.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))