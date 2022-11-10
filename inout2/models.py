from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)

class Tenant(db.Model):
    __tablename__ = "pay_tenant"
    __table_args__ = {"schema": "pgs_ccv"}
    
    ten_id =db.Column(db.Integer, primary_key=True)
    ten_external_id = db.Column(db.String)
    ten_pp_id = db.Column(db.Integer)
