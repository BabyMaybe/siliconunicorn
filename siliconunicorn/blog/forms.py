from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
# from django.forms import PasswordInput, DateInput, NumberInput, HiddenInput, TextInput

from .models import UnicornUser, Post, Comment, BlogImage


class UnicornUserCreationForm(UserCreationForm):
    """Form for creation of new custom User Models"""
    class Meta(UserCreationForm.Meta):
        model = UnicornUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UnicornUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input',
                                                     'autocomplete': 'off'})
        self.fields['email'].widget.attrs.update({'class': 'form-input'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input',
                                                      'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input',
                                                      'autocomplete': 'new-password'})


class UnicornUserChangeForm(UserChangeForm):
    """Form for changing of new custom User Models"""
    class Meta(UserChangeForm.Meta):
        model = UnicornUser
        fields = ('username', 'email')


class NewPostForm(ModelForm):
    """Form for creation of new Post Models"""
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(ModelForm):
    """Form for creation of new Comment Models"""
    class Meta:
        model = Comment
        fields = ['display_author', 'content', ]

        widgets = {
            'content': forms.Textarea(attrs={'id': 'comment-input',
                                             'placeholder': 'Enter comment here...'}),
            'display_author': forms.TextInput(attrs={'id': 'name-input',
                                                     'value': 'LonelyUnicorn'}),
        }


class BlogImageForm(ModelForm):
    """Form for creation of new files"""
    class Meta:
        model = BlogImage
        fields = ['docfile']
