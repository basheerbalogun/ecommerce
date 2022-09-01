from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django.contrib.auth.models import User
from .models import Account


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

        labels = {
            'password1': 'password',
            'password2': 'confirm password'
        }


class UserUpdateForm(forms.Form):

    class Meta:
        model = User
        fields = ('username', 'email',)


class AccountUpdateForm(forms.Form):

    class Meta:
        model = Account
        fields = ('image',)