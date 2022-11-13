from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(150))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Tenant(db.Model):
    __tablename__ = "pay_tenant"
    __table_args__ = {"schema": "pgs_ccv"}
    
    ten_id =db.Column(db.Integer, primary_key=True)
    ten_external_id = db.Column(db.String)
    ten_pp_id = db.Column(db.Integer)
