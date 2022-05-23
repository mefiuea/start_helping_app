from django.urls import path
from django.contrib.auth import views as v

from . import views
from users_app.forms import LoginForm

app_name = 'users_app'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    # path('login/', v.LoginView.as_view(template_name='users_app/login.html', authentication_form=LoginForm), name='login_view'),
    path('register/', views.register_view, name='register_view'),
]
