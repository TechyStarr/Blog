from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required, current_user
from .models import Article, User
from . import db


aven = Blueprint("", __name__)

@aven.route("/")
@aven.route("/home")
def index():
	articles = Article.query.all()
	return render_template("index.html", user = current_user, articles = articles)


@aven.route("/publish", methods = ['GET', 'POST'])
@login_required
def publish():
	if request.method == "POST":
		title = request.form.get('title')
		bodytext = request.form.get('bodytext')

		if not bodytext and not title:
			flash('Please fill in the Title and Bodytext fields to proceed')
		else:
			article = Article(title = title, bodytext = bodytext, author = current_user.id)
			db.session.add(article)
			db.session.commit()
			flash("Your article has been successfully published", category = 'success')
			return redirect(url_for('index'))
	return render_template('publish.html')


@aven.route("/edit/<article_id>", methods = ['GET', 'POST'])
@login_required
def edit(article_id):
	article = Article.query.filter_by(id = article_id).first()
	if request.method == 'POST':
		title = request.form.get('title')
		bodytext = request.form.get('bodytext')

		if not article:
			flash("We can't find your article, Try creating and publising one.", category = 'error' )
		elif current_user.id != article.author:
			flash("You are not allowed to make changes to this article.", category = 'error')
		else:
			article.title = title
			article.bodytext = bodytext
			db.session.commit()
			flash('You successfully edited this article', category ='success')
		return redirect(url_for('index'))
	return render_template('edit.html', article = article)


@aven.route('/delete/<article_id>')
@login_required
def delete(article_id):
	article = Article.query.filter_by(id = article_id).first()
	
	if not article:
		flash("This article does not exist.", category ='error')
	elif current_user.id != article.author:
		flash('You are not allowed to delete thus article', category ='error')
	else:
		db.session.delete(article)
		db.session.commit()
		flash('You have deleted this article', category = 'success')
	return redirect(url_for('index'))

#about route displays info about the page
@aven.route('/about.html')
def about():
	return render_template('about.html')


@aven.route("/article/<email>")
@login_required
def aricles(email):
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('No user with that email exists.', category='error')
        return redirect(url_for('index'))

    aricles = user.aricles
    return render_template("aricles.html", user=current_user, aricles=aricles, email=email)