from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from .forms import RegistrationForm, LoginForm
from donation_app.models import DonationModel


def register_view(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            print('PRINT: Użytkownik utworzony!!!!', user, flush=True)
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
            user = authenticate(request, email=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('home_app:landing_page_view')
            else:
                return redirect('users_app:register_view')
        else:
            print('Walidacja formularza nie przeszła', flush=True)
            context = {'form': form, }
            # check if user email is in database
            email_field = request.POST.get('username')
            current_user_model = get_user_model()
            # emails_from_db = current_user_model.objects.get(email=email_field)
            # print('USERS: ', emails_from_db, flush=True)
            try:
                current_user_model.objects.get(email=email_field)
                print('Taki mail jest w bazie danych', flush=True)
                return render(request, 'users_app/login.html', context=context)
            except ObjectDoesNotExist:
                print('Takiego maila nie ma w bazie danych', flush=True)
                return redirect('users_app:register_view')

    return render(request, 'users_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('home_app:landing_page_view')


def profile_view(request):
    if request.method == 'POST':
        taken_donations_id_list = request.POST.getlist('is_taken')
        print('ISTAKEN: ', taken_donations_id_list, flush=True)
        for id_element in taken_donations_id_list:
            donation = DonationModel.objects.get(pk=int(id_element))
            donation.is_taken = True
            donation.save()

        return redirect('users_app:profile_view')

    if request.method == 'GET':
        user = request.user
        # find donation for specific user
        donations_not_taken = DonationModel.objects.filter(user_donator=user, is_taken=False)
        donations_taken = DonationModel.objects.filter(user_donator=user, is_taken=True)
        context = {
            'donations_not_taken': donations_not_taken,
            'donations_taken': donations_taken,
        }

        return render(request, 'users_app/profile.html', context=context)


def profile_settings_view(request):
    if request.method == 'POST':
        pass

    if request.method == 'GET':

        return render(request, 'users_app/profile_settings.html')
