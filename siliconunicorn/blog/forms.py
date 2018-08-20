from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.forms import PasswordInput, DateInput, NumberInput, HiddenInput, TextInput

from .models import UnicornUser, Post, Comment


class UnicornUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UnicornUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UnicornUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-input',
                                                     'autocomplete': 'off'})
        self.fields['email'].widget.attrs.update({'class' : 'form-input'})
        self.fields['password1'].widget.attrs.update({'class' : 'form-input',
                                                      'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-input',
                                                      'autocomplete': 'new-password'})


class UnicornUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = UnicornUser
        fields = ('username', 'email')


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['display_author', 'content', ]

        widgets = {
        'content' : forms.Textarea(attrs = {'id' : 'new-comment',
                                            'placeholder': 'Enter comment here...'}),
        'display_author' : forms.TextInput(attrs = {'id' : 'new-comment-author',
                                                    'value' : 'LonelyUnicorn'}),
        }
