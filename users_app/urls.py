from django.urls import path

from . import views

app_name = 'users_app'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
]
