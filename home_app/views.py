from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from donation_app.models import DonationModel, InstitutionModel
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth import get_user_model

from donation_app.models import Type
from .forms import ContactForm
from users_app.views import EmailThread


def landing_page_view(request):
    if request.method == 'GET':
        # total number of bags from all donations
        sum_quantity_bags = 0
        donations_objects = DonationModel.objects.all()
        for donation in donations_objects:
            sum_quantity_bags += donation.quantity

        # number of supported organizations
        number_of_institutions = InstitutionModel.objects.all().count()

        # load institutions from database
        foundations = InstitutionModel.objects.filter(type=Type.F).order_by('id')

        # load non-governmental organizations from database
        organizations = InstitutionModel.objects.filter(type=Type.OP)

        # load local collections from database
        local_collections = InstitutionModel.objects.filter(type=Type.ZL)

        context = {
            'sum_of_bags': sum_quantity_bags,
            'number_of_institutions': number_of_institutions,
            'foundations': foundations[0:5],
            'organizations': organizations[0:5],
            'local_collections': local_collections[0:5],
        }

        return render(request, 'home_app/landing_page.html', context=context)


def send_email_from_user_contact_form(first_name, last_name, message):
    admins = get_user_model().objects.filter(is_admin=True, is_active=True, is_staff=True, is_superuser=True,
                                             is_email_verified=True)
    print('ADMINS: ', admins, flush=True)
    all_admins_mails = [admin.email for admin in admins]
    print('ADMINS MAILS LIST: ', all_admins_mails, flush=True)
    email_subject = 'Wiadomość od użytkownika!'
    email_body = f'Użytkownik {first_name} {last_name} napisał: {message}'

    # send email asynchronous
    EmailThread(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER,
                to=all_admins_mails).start()


def contact_form_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            message = form.cleaned_data['message']
            send_email_from_user_contact_form(first_name, last_name, message)

            return render(request, 'home_app/contact_form_message_sent_confirmation.html')

        else:
            context = {
                'form': form,
            }

            return render(request, 'home_app/contact_form_message_sent_fail.html', context=context)


def get_foundations_by_page(request):
    page_number = request.GET.get('page')
    print('PAGE NUMBER: ', page_number, flush=True)
    context = {
        'page_number': page_number,
    }

    return render(request, 'home_app/institutions.html', context=context)


def get_organizations_by_page(request):
    page_number = request.GET.get('page')
    print('PAGE NUMBER: ', page_number, flush=True)
    context = {
        'page_number': page_number,
    }

    return render(request, 'home_app/organizations.html', context=context)


def get_local_collections_by_page(request):
    page_number = request.GET.get('page')
    print('PAGE NUMBER: ', page_number, flush=True)
    context = {
        'page_number': page_number,
    }

    return render(request, 'home_app/local_collections.html', context=context)
