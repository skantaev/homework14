from wtforms_alchemy import ModelForm
from models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        only = ['title', 'content']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        only = ['content']
