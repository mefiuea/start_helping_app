from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

from .models import MyUser
from .forms import RegistrationForm


# admin.site.register(MyUser)

# @admin.register(MyUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name')

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser


# class CustomUserAdmin(UserAdmin):
#     # form = MyUserChangeForm
#     # add_form = MyUserChangeForm
#     model = MyUser
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()
#     fields = ()
#
#     list_display = ('email', 'first_name', 'last_name', 'is_admin')
#
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('email',)}),
#     )
#
#     ordering = ('email', )

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = MyUserChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MyUser, CustomUserAdmin)
