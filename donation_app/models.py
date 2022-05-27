import enum

from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator
from django.contrib.auth import get_user_model

# Validators
phone_regex = RegexValidator(regex=r'(?<!\w)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)')
zip_code_regex = RegexValidator(regex=r'\d{2}-\d{3}')


# Enums choices
@enum.unique
class Type(str, enum.Enum):
    F = 'Fundacja'
    OP = 'Organizacja Pozarządowa'
    ZL = 'Zbiórka Lokalna'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class CategoryModel(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, verbose_name='Nazwa')


class InstitutionModel(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, verbose_name='Nazwa')
    description = models.TextField(blank=False, validators=[MaxLengthValidator(2000)], verbose_name='Opis')
    # TYPE_CHOICES = [
    #     ('F', 'Fundacja'),
    #     ('OP', 'Organizacja Pozarządowa'),
    #     ('ZL', 'Zbiórka Lokalna'),
    # ]
    type = models.CharField(max_length=23, choices=Type.choices(), blank=False, default=Type.F, verbose_name='Typ')
    categories = models.ManyToManyField('CategoryModel', blank=False, related_name='institution_category')


class DonationModel(models.Model):
    quantity = models.PositiveIntegerField(blank=False, verbose_name='ilość')
    categories = models.ManyToManyField('CategoryModel', blank=False, related_name='donation_category')
    institution = models.ForeignKey('InstitutionModel', on_delete=models.PROTECT, related_name='institution')
    address = models.CharField(max_length=200, blank=False, verbose_name='Adres')
    phone_number = models.CharField(max_length=17, blank=False, validators=[phone_regex], verbose_name='Numer telefonu')
    city = models.CharField(max_length=50, blank=False, verbose_name='Miasto')
    zip_code = models.CharField(max_length=6, blank=False, validators=[zip_code_regex], verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(verbose_name='Data')
    pick_up_time = models.TimeField(verbose_name='Godzina')
    pick_up_comment = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(300)], verbose_name='Opis')
    user_donator = models.ForeignKey(get_user_model(), blank=True, null=True, default=None, on_delete=models.PROTECT,
                                     related_name='donator')
