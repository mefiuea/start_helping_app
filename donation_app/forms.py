from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from .models import DonationModel

# Validators
phone_regex = RegexValidator(regex=r'(?<!\w)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)')
zip_code_regex = RegexValidator(regex=r'\d{2}-\d{3}')


class DonationForm(forms.Form):
    categories = forms.IntegerField()
    bags = forms.IntegerField(label=_('test'), help_text='Wprowadź ilość worków')
    organization = forms.CharField(max_length=200, label=_('organization'), help_text='Wybierz organizacje')
    address = forms.CharField(max_length=200, label=_('address'), help_text='Wprowadź adres')
    city = forms.CharField(max_length=200, label=_('city'), help_text='Wprowadź miasto')
    postcode = forms.CharField(max_length=200, label=_('postcode'), help_text='Dopuszczalny format: XX-YYY',
                               validators=[zip_code_regex])
    phone = forms.CharField(max_length=200, label=_('phone'), help_text='9 numerowy numer - dopuszczalne +48 i spacje',
                            validators=[phone_regex])
    data = forms.DateField(label=_('data'), help_text='Wprowadź datę')
    time = forms.TimeField(label=_('time'), help_text='Wprowadź godzinę')
    more_info = forms.CharField(max_length=300, label=_('more_info'), help_text='Wprowadź uwagi', required=False)

    class Meta:
        fields = ('bags', 'organization', 'address', 'city', 'postcode', 'phone', 'data', 'time', 'more_info')
