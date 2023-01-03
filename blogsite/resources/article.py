from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required
from flask_login import current_user, login_required, current_user
from blogsite.models import ArticleModel, UserModel, CommentModel
from db import db


article = Blueprint("Article", "article", __name__)


# @article.route('/search')
# def search():
#     query = request.args.get('query')
#     results = search_engine.search(query)
#     return render_template('search.html', results=results)






# @article.route('/search', methods=['GET', 'POST'])
# def search_article( *article_data):
#     if request.method == 'POST':
#         title = request.form.get("title")
#         bodytext = request.form.get("bodytext")

#         article = ArticleModel.query.filter(title=title, bodytext=bodytext)
#         if article:
#                 flash(f"We found this")
#         return render_template("index.html", "searched")


# @article.route('/search', methods=['GET', 'POST'])
# def search_article():
#     search = request.args.get("searched")

#     if search:
#         article = ArticleModel.query.filter(article.title.contains(
#         search) | article.bodytext.contains(search))
    
#     else:
#         flash("Article not found")

#     return render_template('search.html')


@article.route("/edit/<article_id>", methods=['GET', 'POST'])
@login_required
def edit(article_id):
	article = ArticleModel.query.filter_by(id=article_id).first()
	if request.method == 'POST':
		title = request.form.get('title')
		bodytext = request.form.get('bodytext')

		if not article:
			flash("We can't find your article, Try creating and publising one.", category='error')
		elif current_user.id != article.author:
			flash("You are not allowed to make changes to this article.", category='error')
		else:
			article.title = title
			article.bodytext = bodytext
			db.session.commit()
			flash('You successfully edited this article', category='success')
		return redirect(url_for('aven.index'))
	return render_template('edit.html', article=article)


@article.route('/delete/<article_id>')
@login_required
def delete(article_id):
	article = ArticleModel.query.filter_by(id=article_id).first()

	if not article:
		flash("This article does not exist.", category='error')
	elif current_user.id != article.author:
		flash('You are not allowed to delete this article', category='error')
	else:
		db.session.delete(article)
		db.session.commit()
		flash('You have deleted this article', category='success')
	return redirect(url_for('aven.index'))


@article.route("/articles/<username>")
@login_required
def posts(username):
    user = UserModel.query.filter_by(username=username).first()

    if not user:
        flash('This user does not exist.', category='error')
        return redirect(url_for('aven.index'))

    articles = user.articles
    return render_template("article.html", user=current_user, articles=articles, username=username)



@article.route("/create-comment/<article_id>", methods=['GET','POST'])
@login_required
def create_comment(article_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        article = ArticleModel.query.filter_by(id=article_id)
        if article:
            comment = CommentModel(
                text=text, author=current_user.id, article_id=article_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Article does not exist.', category='error')

    return redirect(url_for('aven.index'))


@article.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = CommentModel.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.article.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('aven.index'))
