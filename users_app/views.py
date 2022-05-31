import threading
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, ProfileEditForm, PasswordResetForm
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


@login_required
def profile_view(request):
    if request.method == 'POST':
        taken_donations_id_list = request.POST.getlist('is_taken')
        print('ISTAKEN: ', taken_donations_id_list, flush=True)
        for id_element in taken_donations_id_list:
            donation = DonationModel.objects.get(pk=int(id_element))
            donation.is_taken = True
            donation.is_taken_date = datetime.now()
            donation.save()

        return redirect('users_app:profile_view')

    if request.method == 'GET':
        user = request.user
        # find donation for specific user
        donations_not_taken = DonationModel.objects.filter(user_donator=user, is_taken=False).order_by('-date_add')
        donations_taken = DonationModel.objects.filter(user_donator=user, is_taken=True).order_by('-is_taken_date')
        context = {
            'donations_not_taken': donations_not_taken,
            'donations_taken': donations_taken,
        }

        return render(request, 'users_app/profile.html', context=context)


@login_required
def profile_settings_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST or None)
        if form.is_valid():
            user_instance = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data.get('password')
            if not request.user.check_password(password):
                context = {
                    'form': form,
                    'wrong_password': 'Niepoprawne hasło',
                }
                return render(request, 'users_app/profile_settings.html', context=context)
            # password passed
            # checking if the email has changed
            if email == user_instance.email:
                user_instance.first_name = first_name
                user_instance.last_name = last_name
                user_instance.save()
                return redirect('users_app:profile_view')
            else:
                try:
                    get_user_model().objects.get(email=email)
                    print('Taki mail jest w bazie danych', flush=True)
                    context = {
                        'form': form,
                        'email_repeat': 'Taki email istnieje już w bazie danych',
                    }
                    return render(request, 'users_app/profile_settings.html', context=context)
                except ObjectDoesNotExist:
                    print('Takiego maila nie ma w bazie danych', flush=True)
                    user_instance.first_name = first_name
                    user_instance.last_name = last_name
                    user_instance.email = email
                    user_instance.save()
                    return redirect('users_app:profile_view')
        else:
            print('Walidacja formularza nie przeszła', flush=True)
            context = {'form': form, }
            return render(request, 'users_app/profile_settings.html', context=context)

    if request.method == 'GET':
        form = ProfileEditForm()

        context = {
            'form': form,
        }

        return render(request, 'users_app/profile_settings.html', context=context)


@login_required
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST or None)
        if form.is_valid():
            user_instance = request.user
            old_password = form.cleaned_data.get('old_password')
            # check if actual password match with user password
            if not request.user.check_password(old_password):
                context = {
                    'form': form,
                    'password_help_text': password_validators_help_texts(),
                    'wrong_old_password': 'Niepoprawne aktualne hasło',
                }
                return render(request, 'users_app/password_reset.html', context=context)
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1 and new_password2 and new_password1 != new_password2:
                context = {
                    'form': form,
                    'password_help_text': password_validators_help_texts(),
                    'passwords_dont_match': 'Nowe hasła nie pasują do siebie'
                }
                return render(request, 'users_app/password_reset.html', context=context)
            # django validators
            try:
                validate_password(new_password1, user_instance)
                # everything's ok - can change password
                # change user password
                user_instance.set_password(new_password1)
                user_instance.save()
                return render(request, 'users_app/password_reset_confirmation.html')
            except ValidationError as e:
                context = {
                    'form': form,
                    'password_help_text': password_validators_help_texts(),
                    'validations_errors': e.messages
                }
                return render(request, 'users_app/password_reset.html', context=context)
        else:
            print('Walidacja formularza nie przeszła', flush=True)
            context = {
                'form': form,
                'password_help_text': password_validators_help_texts()
            }
            return render(request, 'users_app/password_reset.html', context=context)

    if request.method == 'GET':
        form = PasswordResetForm()
        context = {
            'form': form,
            'password_help_text': password_validators_help_texts()
        }
        return render(request, 'users_app/password_reset.html', context=context)
