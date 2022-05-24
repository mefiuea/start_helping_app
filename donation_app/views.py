from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import CategoryModel, InstitutionModel


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
    type_ids = request.GET.getlist('type_ids')
    print('PRINT:', type_ids, flush=True)
    if type_ids is not None:
        institutions = InstitutionModel.objects.filter(categories__in=type_ids).distinct()
    else:
        institutions = InstitutionModel.objects.all()

    context = {
        'institutions': institutions,
    }

    return render(request, 'donation_app/institutions.html', context=context)
