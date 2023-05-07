from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    """imageboard posts"""
    class Meta:
        model = Posting
        fields = ('title', 'file')


class SignUpForm(forms.ModelForm):
    """user signup"""
    class Meta:
        model = User
        fields = ('username', 'password')


class CommentForm(forms.ModelForm):
    """user comments"""
    class Meta:
        model = Comment
        fields = ('content',)

class TagForm(forms.ModelForm):
    """adding tags"""
    class Meta:
        model = Tag
        fields = ('name',)

    def clean_name(self):
        data = self.cleaned_data['name']
        if ' ' in data:
            raise ValidationError("Tag cannot contain whitespace")

        return data