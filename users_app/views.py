from django.shortcuts import render


def login_view(request):
    if request.method == 'GET':
        return render(request, 'users_app/login.html')


def register_view(request):
    if request.method == 'GET':
        return render(request, 'users_app/register.html')
