from datetime import datetime
from imageboard.app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    updated_at = date_created
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.id,
            'creation date': self.date_created,
            'updated at': self.updated_at,
            'deleted': self.is_visible
        }


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
    updated_at = date_created
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'content': self.id,
            'creation date': self.date_created,
            'updated at': self.updated_at,
            'deleted': self.is_visible
        }
