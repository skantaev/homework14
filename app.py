from flask import Flask, request, flash, render_template
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/posts', methods=['GET', 'POST'])
def index():
    from models import Post
    from forms import PostForm

    if request.method == 'POST':
        form = PostForm(request.form)

        if form.validate():
            post = Post(**form.data)
            db.session.add(post)
            db.session.commit()

            flash('Пост опубликован.')

        else:
            flash('Форма не валидна! Пост не был опубликован.')
            flash(str(form.errors))

    posts = Post.query.all()

    return render_template('posts.txt', posts=posts)


@app.route('/posts/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    from models import Comment, Post
    from forms import CommentForm

    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        return 'Not Found', 404

    if request.method == 'POST':
        form = CommentForm(request.form)

        if form.validate():
            comment = Comment(post=post, content=request.form['content'])
            db.session.add(comment)

            post.number_of_comments += 1

            db.session.commit()

            flash('Комментарий опубликован.')

        else:
            flash('Форма не валидна! Комментарий не был опубликован.')
            flash(str(form.errors))

    comments = Comment.query.filter_by(post_id=post.id).all()

    return render_template('item.txt', post=post, comments=comments)


if __name__ == '__main__':
    from models import *

    db.create_all()
    app.run()
