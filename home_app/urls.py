from django.urls import path

from . import views

app_name = 'home_app'

urlpatterns = [
    path('', views.landing_page_view, name='landing_page_view'),
    path('contact/', views.contact_form_view, name='contact_form_view'),
]
