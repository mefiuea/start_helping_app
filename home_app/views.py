from django.http import HttpResponse
from django.shortcuts import render


def landing_page_view(request):
    if request.method == 'GET':
        return render(request, 'home_app/landing_page.html')
