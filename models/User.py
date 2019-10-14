from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db

### Example
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)