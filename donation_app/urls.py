from django.urls import path

from . import views

app_name = 'donation_app'

urlpatterns = [
    path('add-donation/', views.add_donation_view, name='donation_view'),
    path('get_institutions_by_id/', views.get_institutions_by_id, name='get_institutions_by_id_view'),
]
