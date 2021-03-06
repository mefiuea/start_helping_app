import threading
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from .forms import RegistrationForm, LoginForm, ProfileEditForm, PasswordResetForm, PasswordEmailForm, \
    PasswordResetByEmailForm
from donation_app.models import DonationModel
from .utils import generate_token


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, to):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to = to
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(subject=self.subject, body=self.body, from_email=self.from_email, to=self.to)
        msg.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Aktywuj swoje konto w aplikacji do pomagania!'
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    }
    email_body = render_to_string('users_app/activate_email.html', context=context)

    # send email synchronous
    # email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER, to=[user.email])
    # email.send()

    # send email asynchronous
    EmailThread(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER, to=(user.email,)).start()


def send_password_reset_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Link do zresetowania has??a w aplikacji do pomagania!'
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    }
    email_body = render_to_string('users_app/password_reset_email_link.html', context=context)

    # send email asynchronous
    EmailThread(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER, to=(user.email,)).start()


def register_view(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_email_verified = False
            user.save()
            print('PRINT: U??ytkownik utworzony!!!!', user, flush=True)

            send_activation_email(user, request)

            context = {
                'form': form,
                'email_sent': 'Na Tw??j adres email zosta?? wys??any mail z linkiem aktywacyjnym.'
            }
            return render(request, 'users_app/register.html', context=context)
        else:
            print('Walidacja formularza nie przesz??a', flush=True)
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

            if not user.is_email_verified:
                context = {
                    'user_is_not_active': 'Twoje konto nie jest zweryfikowane przez email.',
                }
                return render(request, 'users_app/login.html', context=context)

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
            print('Walidacja formularza nie przesz??a', flush=True)
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
                    'wrong_password': 'Niepoprawne has??o',
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
                        'email_repeat': 'Taki email istnieje ju?? w bazie danych',
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
            print('Walidacja formularza nie przesz??a', flush=True)
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
                    'wrong_old_password': 'Niepoprawne aktualne has??o',
                }
                return render(request, 'users_app/password_reset.html', context=context)
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1 and new_password2 and new_password1 != new_password2:
                context = {
                    'form': form,
                    'password_help_text': password_validators_help_texts(),
                    'passwords_dont_match': 'Nowe has??a nie pasuj?? do siebie'
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
            print('Walidacja formularza nie przesz??a', flush=True)
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


def activate_user_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)

    except ObjectDoesNotExist:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        # context = {
        #     'user_is_active_now': 'Twoje konto jest ju?? aktywne.',
        # }
        # return render(request, 'users_app/login.html', context=context)
        return redirect('users_app:login_view')
    else:
        context = {
            'user': user,
        }
        return render(request, 'users_app/activate_failed.html', context=context)


def password_reset_by_email(request):
    if request.method == 'POST':
        form = PasswordEmailForm(request.POST or None)
        if form.is_valid():
            user_instance = request.user
            email = form.cleaned_data.get('email')
            current_user_model = get_user_model()
            # check if email exists in database
            try:
                user = current_user_model.objects.get(email=email)
                print('Taki mail jest w bazie danych', flush=True)

                user.is_email_verified = False
                user.save()
                send_password_reset_email(user, request)

                context = {
                    'form': form,
                    'email_sent': 'Na Tw??j adres email zosta?? wys??any mail z linkiem do formularza zmiany has??a.'
                }

                return render(request, 'users_app/password_reset_email.html', context=context)
            except ObjectDoesNotExist:
                print('Takiego maila nie ma w bazie danych', flush=True)
                context = {
                    'email_does_not_exist_in_db': 'Taki email nie istnieje w bazie danych.'
                }
                return render(request, 'users_app/password_reset_email.html', context=context)
        else:
            print('Walidacja formularza nie przesz??a', flush=True)
            context = {'form': form, }
            return render(request, 'users_app/password_reset_email.html', context=context)

    if request.method == 'GET':
        return render(request, 'users_app/password_reset_email.html')


def password_reset_by_email_changing_form_view(request, uidb64, token):
    if request.method == 'POST':
        form = PasswordResetByEmailForm(request.POST or None)
        if form.is_valid():
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1 and new_password2 and new_password1 != new_password2:
                context = {
                    'form': form,
                    'password_help_text': password_validators_help_texts(),
                    'passwords_dont_match': 'Nowe has??a nie pasuj?? do siebie'
                }
                return render(request, 'users_app/password_reset_by_email_form.html', context=context)
            # django validators
            try:
                validate_password(new_password1, user)
                # everything's ok - can change password
                # change user password
                user.set_password(new_password1)
                user.save()
                return render(request, 'users_app/password_reset_by_email_form_confirmation.html')
            except ValidationError as e:
                context = {
                    'form': form,
                    'password_help_text': password_validators_help_texts(),
                    'validations_errors': e.messages
                }
                return render(request, 'users_app/password_reset_by_email_form.html', context=context)

        else:
            print('Walidacja formularza nie przesz??a', flush=True)
            context = {
                'form': form,
                'password_help_text': password_validators_help_texts()
            }
            return render(request, 'users_app/password_reset_by_email_form.html', context=context)

    if request.method == 'GET':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            # print('UID: ', uid, flush=True)
            user = get_user_model().objects.get(pk=uid)
            # print('USER: ', user, flush=True)
            print('LINIA 385 CHECK TOKEN2 w TRY: ', generate_token.check_token(user, token), flush=True)

        except ObjectDoesNotExist:
            user = None

        if user and generate_token.check_token(user, token):
            # ok
            user.is_email_verified = True
            user.save()
            print('LINIA 395 WEWNATRZ IF: ', flush=True)
            context = {
                'password_help_text': password_validators_help_texts()
            }

            return render(request, 'users_app/password_reset_by_email_form.html', context=context)
        else:
            print('LINIA 402 WEWNATRZ ELSE: ', flush=True)
            print('LINIA 403 CHECK TOKEN2: ', generate_token.check_token(user, token), flush=True)
            context = {
                'user': user,
            }
            return render(request, 'users_app/password_reset_by_email_form_failed.html', context=context)
