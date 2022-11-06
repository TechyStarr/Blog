from time import timezone

from sqlalchemy import true
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#user model
class User(db.Model, UserMixin):
	id =  db.Column(db.Integer(), primary_key = True) 
	firstname = db.Column(db.String(255), nullable = False, unique = False)
	lastname = db.Column(db.String(255), nullable = False, unique = False)
	username = db.Column(db.String(255), nullable = False, unique = False)
	email = db.Column(db.String(255), nullable = False, unique = True)
	password_hash = db.Column(db.String())
	date_created = db.Column(db.DateTime(timezone = True), default = func.now())
	article = db.relationship('Article', backref = 'user', passive_deletes = True)



	# is_writer = db.Column(db.Boolean(False))

# Article model
class Article(db.Model):
	id =  db.Column(db.Integer(), primary_key = True) 
	title = db.Column(db.String(550))
	bodytext = db.Column(db.String(3000), nullable = False, unique = False)
	author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
	date_created = db.Column(db.DateTime(timezone = True), default = func.now())


