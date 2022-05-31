from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.forms import PasswordInput


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label=_('first name'), help_text='Imię jest wymagane')
    last_name = forms.CharField(max_length=30, label=_('last name'), help_text='Nazwisko jest wymagane')
    email = forms.EmailField(max_length=100, label=_('email'),
                             help_text='Email musi być unikalny i w formie X@Y.pl/com...')

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='email', widget=forms.TextInput(
        attrs={
            'type': 'text',
            'name': 'username',
            'placeholder': 'email'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'name': 'password',
            'placeholder': 'password'
        }
    ))

    class Meta:
        fields = ('username', 'password')


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('first name'), help_text='Imię jest wymagane')
    last_name = forms.CharField(max_length=30, label=_('last name'), help_text='Nazwisko jest wymagane')
    email = forms.EmailField(max_length=100, label=_('email'),
                             help_text='Email musi być unikalny i w formie X@Y.pl/com...')
    password = forms.CharField(label=_('password'), help_text='Wprowadź swoje aktualne hasło żeby zmienić dane',
                               widget=PasswordInput())
