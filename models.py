from datetime import datetime
from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    number_of_comments = db.Column(db.Integer, default=0)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
        nullable=False,
        index=True
    )
    post = db.relationship(Post, foreign_keys=[post_id])
    content = db.Column(db.String(3000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
