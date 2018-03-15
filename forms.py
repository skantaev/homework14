from wtforms_alchemy import ModelForm
from wtforms.fields import StringField
from wtforms.validators import Length
from imageboard.models import Post, Comment

content_validator = StringField(validators=[Length(min=6, max=3000)])


class PostFullForm(ModelForm):
    class Meta:
        model = Post
        only = ['title', 'content']

    title = StringField(validators=[Length(min=3, max=60)])
    content = content_validator


class PostPatchForm(ModelForm):
    class Meta:
        model = Post
        only = ['content']

    content = content_validator


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        only = ['content']

    content = content_validator
