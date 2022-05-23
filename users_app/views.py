from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from .forms import RegistrationForm


def login_view(request):
    if request.method == 'GET':
        return render(request, 'users_app/login.html')


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
            errors_list = []
            for field in form:
                errors_list.append((field.errors, field.help_text))
            context = {'form': form,
                       'errors_list': errors_list}
            return render(request, 'users_app/register.html', context=context)

    return render(request, 'users_app/register.html')
