# contain all the routes
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required, current_user
from blogsite.models import ArticleModel, UserModel
from db import db

aven = Blueprint("aven", __name__)


@aven.route("/")
@aven.route("/index")
def index():
    articles = ArticleModel.query.all()
    return render_template("index.html", user=current_user, articles=articles)


@aven.route("/publish", methods=['GET', 'POST'])
@login_required
def publish():
	if request.method == "POST":
		title = request.form.get('title')
		bodytext = request.form.get('bodytext')

		if not bodytext and not title:
			flash('Please fill in the Title and Bodytext fields to proceed')
		else:
			article = ArticleModel(title=title, bodytext=bodytext, author=current_user.id)
			db.session.add(article)
			db.session.commit()
			flash("Your article has been successfully published", category='success')
			return redirect(url_for('aven.index'))
	return render_template('publish.html')



# about route displays info about the page
@aven.route('/about')
def about():
	return render_template('about.html')


@aven.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('We appreciate the feedback, be on the lookout for our response',
              category='success')
    return render_template("contact.html", current_user=current_user)


@aven.route("/article/<email>")
@login_required
def aricles(email):
    user = UserModel.query.filter_by(email=email).first()

    if not user:
        flash('No user with that email exists.', category='error')
        return redirect(url_for('index'))

    aricles = user.aricles
    return render_template("aricles.html", user=current_user, aricles=aricles, email=email)






