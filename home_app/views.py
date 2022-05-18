from django.http import HttpResponse
from django.shortcuts import render


def simple_view(request):
    if request.method == 'GET':
        return render(request, )
