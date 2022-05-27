from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import CategoryModel, InstitutionModel, DonationModel
from .forms import DonationForm


@login_required
def add_donation_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST or None)
        if form.is_valid():
            print('FORMULARZ ZWALIDOWANY!!!!!!!!!!', flush=True)
            categories = request.POST.getlist('categories')
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

            print(categories, type(categories), flush=True)
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
            # donation.user = request.user
            donation.save()
        else:
            print('FORMULARZ NIEZWALIDOWANY!!!!!!!!!!', flush=True)
            # get categories from database
            categories = CategoryModel.objects.all().order_by('id')
            # get institutions from database
            institutions = InstitutionModel.objects.all().order_by('id')
            context = {'form': form,
                       'categories': categories,
                       'institutions': institutions,
                       }
            return render(request, 'donation_app/form.html', context=context)
            # return redirect('donation_app:donation_view')

        return render(request, 'donation_app/form_confirmation.html')

    if request.method == 'GET':
        # get categories from database
        categories = CategoryModel.objects.all().order_by('id')

        # get institutions from database
        institutions = InstitutionModel.objects.all().order_by('id')

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
