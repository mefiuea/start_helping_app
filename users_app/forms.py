from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=_('first name'), help_text='Imię jest wymagane')
    last_name = forms.CharField(label=_('last name'), help_text='Nazwisko jest wymagane')
    email = forms.EmailField(label=_('email'), help_text='Email jest wymagany i musi być unikalny')

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
