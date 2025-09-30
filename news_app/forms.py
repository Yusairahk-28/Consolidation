"""
Contains custom user signup and authentication forms.
"""

from django import forms
from .models import Article, Roles
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body", "publisher"]


class SignUpForm(UserCreationForm):
    # Custom signup form for new users.
    role = forms.ChoiceField(choices=Roles.choices, required=True, label="Account role")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', "email", 'password1', "password2"]


class LoginForm(forms.Form):
     # Custom login form for new users.
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")




