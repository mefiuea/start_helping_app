from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import CategoryModel, InstitutionModel, DonationModel
from .forms import DonationForm


@login_required
def add_donation_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST or None)
        categories_list = request.POST.getlist('categories')
        categories_list_int = []
        institutions_list = []
        ic_id_list = []

        for cat in categories_list:
            categories_list_int.append(int(cat))

        institutions = InstitutionModel.objects.all()
        for institution in institutions:
            print(institution, flush=True)
            for ic in institution.categories.all():
                # print(ic.id, flush=True)
                ic_id_list.append(ic.id)
            print(ic_id_list, flush=True)

            check = all(item in ic_id_list for item in categories_list_int)
            if check is True:
                institutions_list.append(institution)

            ic_id_list = []
        print('LISTA PASUJĄCYCH INSTYTUCJI POST: ', institutions_list, flush=True)

        print(categories_list, type(categories_list), flush=True)

        organization_radio_button = request.POST.get('organization')
        print('organization_radio_button', organization_radio_button, type(organization_radio_button), flush=True)
        if form.is_valid():
            print('FORMULARZ ZWALIDOWANY!!!!!!!!!!', flush=True)
            bags = form.cleaned_data['bags']
            organization = form.cleaned_data['organization']
            organization_instance = InstitutionModel.objects.get(name=organization)
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            postcode = form.cleaned_data['postcode']
            phone = form.cleaned_data['phone']
            data = form.cleaned_data['data']
            time = form.cleaned_data['time']
            more_info = form.cleaned_data['more_info']

            print(bags, type(bags), flush=True)
            print(organization, type(organization), flush=True)
            print(organization_instance, type(organization_instance), flush=True)
            print(address, type(address), flush=True)
            print(city, type(city), flush=True)
            print(postcode, type(postcode), flush=True)
            print(phone, type(phone), flush=True)
            print(data, type(data), flush=True)
            print(time, type(time), flush=True)
            print(more_info, type(more_info), flush=True)

            # create Donation object
            donation = DonationModel(quantity=bags, institution=organization_instance, address=address,
                                     phone_number=phone, city=city, zip_code=postcode, pick_up_date=data,
                                     pick_up_time=time, pick_up_comment=more_info)
            donation.user_donator = request.user
            donation.save()
            # category list from html
            # create instances of selected categories
            categories_list_instances = []
            for category in categories_list:
                category_instance = CategoryModel.objects.get(pk=int(category))
                categories_list_instances.append(category_instance)
            # add categories to donation
            for category_instance in categories_list_instances:
                donation.categories.add(category_instance)

        else:
            print('FORMULARZ NIEZWALIDOWANY!!!!!!!!!!', flush=True)
            # get categories from database
            categories = CategoryModel.objects.all().order_by('id')
            # get institutions from database
            institutions = InstitutionModel.objects.all().order_by('id')
            context = {'form': form,
                       'categories': categories,
                       'institutions': institutions,
                       'categories_list_int': categories_list_int,
                       'institutions_list': institutions_list,
                       'organization_radio_button': organization_radio_button,
                       }
            return render(request, 'donation_app/form.html', context=context)
            # return redirect('donation_app:donation_view')

        return render(request, 'donation_app/form_confirmation.html')

    if request.method == 'GET':
        # get categories from database
        categories = CategoryModel.objects.all().order_by('id')

        # get institutions from database
        institutions = InstitutionModel.objects.all().order_by('id')
        print('INSTYTUCJE: ', institutions, flush=True)

        context = {
            'categories': categories,
            'institutions': institutions,
        }

        return render(request, 'donation_app/form.html', context=context)


def get_institutions_by_id(request):
    ic_id_list = []
    institutions_list = []
    type_ids_int = []
    type_ids = request.GET.getlist('type_ids')
    for element in type_ids:
        type_ids_int.append(int(element))
    print('PRINT:', type_ids, flush=True)
    if type_ids:
        # institutions = InstitutionModel.objects.filter(categories__in=type_ids).distinct()
        institutions = InstitutionModel.objects.all()
        for institution in institutions:
            print(institution, flush=True)
            for ic in institution.categories.all():
                # print(ic.id, flush=True)
                ic_id_list.append(ic.id)
            print(ic_id_list, flush=True)

            check = all(item in ic_id_list for item in type_ids_int)
            if check is True:
                institutions_list.append(institution)

            ic_id_list = []
        print('LISTA PASUJĄCYCH INSTYTUCJI: ', institutions_list, flush=True)

    else:
        institutions = InstitutionModel.objects.all()
        for institution in institutions:
            institutions_list.append(institution)

    context = {
        'institutions': institutions_list,
    }

    return render(request, 'donation_app/institutions.html', context=context)
