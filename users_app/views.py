from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout

from .forms import RegistrationForm, LoginForm


def register_view(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            print('PRINT: Uzytkownik utworzony!!!!', user, flush=True)
            return redirect('users_app:login_view')
        else:
            context = {'form': form, }
            return render(request, 'users_app/register.html', context=context)

    return render(request, 'users_app/register.html')


def login_view(request):
    form = LoginForm(request, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home_app:landing_page_view')
            else:
                return redirect('users_app:register_view')
        else:
            print('Walidacja formularza nie przeszła', flush=True)
            print('ERRORS:', form.errors, flush=True)
            context = {'form': form, }

            return render(request, 'users_app/login.html', context=context)

    return render(request, 'users_app/login.html')
