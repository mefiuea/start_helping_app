from django.contrib import admin

from .models import InstitutionModel


@admin.register(InstitutionModel)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')

