from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('first name'), help_text='Maksymalnie 30 znaków.')
    last_name = forms.CharField(max_length=30, label=_('last name'), help_text='Maksymalnie 30 znaków.')
    message = forms.CharField(max_length=400, label=_('message'), help_text='Maksymalnie 400 znaków.')
