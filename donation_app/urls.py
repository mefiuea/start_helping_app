from django.urls import path

from . import views

app_name = 'donation_app'

urlpatterns = [
    path('add-donation/', views.add_donation_view, name='donation_view'),
]
