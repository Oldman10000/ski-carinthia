from django import forms
from .models import Post, PostComment


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholder, remove auto-generated label
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'content': 'Add Comment',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'content', 'tag')
