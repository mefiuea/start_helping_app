from django.urls import path
from django.contrib.auth import views as v

from . import views
from users_app.forms import LoginForm

app_name = 'users_app'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile-settings/', views.profile_settings_view, name='profile_settings_view'),
    path('password-reset/', views.password_reset_view, name='password_reset_view'),
    path('activate-user/<uidb64>/<token>/', views.activate_user_view, name='activate_user_view'),
    path('password-reset-by-email/', views.password_reset_by_email, name='password_reset_by_email_view'),
    path('password-reset-by-email-changing-form/<uidb64>/<token>/', views.password_reset_by_email_changing_form_view,
         name='password_reset_by_email_changing_form_view'),
]
