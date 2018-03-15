from flask import Flask, request, flash, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy

import imageboard.config as config

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/posts', methods=['GET', 'POST'])
def index():
    from imageboard.models import Post
    from imageboard.forms import PostFullForm

    if request.method == 'POST':
        form = PostFullForm(request.form)

        if form.validate():
            post = Post(**form.data)
            db.session.add(post)
            db.session.commit()

            flash('Пост опубликован.')

            resp = make_response(jsonify(post.to_dict()), 201)
            resp.headers['Location'] = '/posts/{}'.format(post.id)
            return resp

        else:
            flash('Форма не валидна! Пост не был опубликован.')
            flash(str(form.errors))

    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@app.route('/posts/<int:post_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def show_post(post_id):
    from imageboard.models import Comment, Post
    from imageboard.forms import CommentForm, PostPatchForm
    from datetime import datetime

    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        if request.method != 'DELETE':
            return 'Not Found', 404
        else:
            return 'No Content', 204

    if request.method == 'POST':
        form = CommentForm(request.form)

        if form.validate():
            comment = Comment(post=post, content=request.form['content'])
            db.session.add(comment)
            db.session.commit()

            flash('Комментарий опубликован.')

        else:
            flash('Форма не валидна! Комментарий не был опубликован.')
            flash(str(form.errors))

    if request.method == 'PATCH':
        form = PostPatchForm(request.form)

        if form.validate():
            post.content = request.form['content']
            post.updated_at = datetime.now()

            db.session.commit()
            flash('Пост изменен.')

        else:
            flash('Форма не валидна! Пост не был изменен.')
            flash(str(form.errors))

    if request.method == 'DELETE':
        post.is_visible = False
        db.session.commit()

    # return jsonify()


if __name__ == '__main__':
    from imageboard.models import *

    db.create_all()
    app.run()
