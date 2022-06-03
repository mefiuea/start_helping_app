from django.contrib import admin

from .models import InstitutionModel, CategoryModel, DonationModel


@admin.register(InstitutionModel)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(DonationModel)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user_donator', 'address')
