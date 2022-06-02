from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Текст поста ...'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
