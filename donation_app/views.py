from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import CategoryModel, InstitutionModel
from django.http import HttpRequest, HttpResponse


@login_required
def add_donation_view(request):
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
