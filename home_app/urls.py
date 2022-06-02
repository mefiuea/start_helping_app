from django.urls import path

from . import views

app_name = 'home_app'

urlpatterns = [
    path('', views.landing_page_view, name='landing_page_view'),
    path('contact/', views.contact_form_view, name='contact_form_view'),
    path('get_foundations_by_page/', views.get_foundations_by_page, name='get_foundations_by_page_view'),
    path('get_organizations_by_page/', views.get_organizations_by_page, name='get_organizations_by_page_view'),
    path('get_local_collections_by_page/', views.get_local_collections_by_page,
         name='get_local_collections_by_page_view'),
]
