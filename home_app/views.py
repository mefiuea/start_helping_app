from django.http import HttpResponse
from django.shortcuts import render

from donation_app.models import DonationModel, InstitutionModel


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
        foundations = InstitutionModel.objects.filter(type='F')

        # load non-governmental organizations from database
        organizations = InstitutionModel.objects.filter(type='OP')

        # load local collections from database
        local_collections = InstitutionModel.objects.filter(type='ZL')

        context = {
            'sum_of_bags': sum_quantity_bags,
            'number_of_institutions': number_of_institutions,
            'foundations': foundations,
            'organizations': organizations,
            'local_collections': local_collections,
        }

        return render(request, 'home_app/landing_page.html', context=context)
