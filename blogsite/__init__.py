from flask import Flask
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = 'blog2.db'

#generate current path
base_dir = os.path.dirname(os.path.realpath(__file__)) 


def blog_app():
	app = Flask(__name__)

# app configuration
	app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'blog.db')
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["SECRET_KEY"] = 'iLhqyLO3HtSpsE8cuQaj'
	app.config["SECRET_KEY"] = 'blog'

#initializing database
	db.init_app(app)
	from .aven import aven
	from .auth import auth

	app.register_blueprint(aven, url_prefix = "/")
	app.register_blueprint(auth, url_prefix = "/")
	
	from .models import User, Article

	with app.app_context():
		db.create_all()

	login_manager = LoginManager()
	login_manager.login_view = "auth.login"
	login_manager.init_app(app)

	def __repr__(self):
		return f"User <{self.username}"

	@login_manager.user_loader
	def user_loader(id):
		return User.query.get(int(id))

	return app