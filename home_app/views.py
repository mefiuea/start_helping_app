from django.shortcuts import render
from donation_app.models import DonationModel, InstitutionModel
from django.core.paginator import Paginator

from donation_app.models import Type


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

        # setting Pagination for foundations
        paginator_instance = Paginator(foundations, 5)
        page = request.GET.get('page')
        foundations_paginator_instance = paginator_instance.get_page(page)

        # setting Pagination for non-governmental organizations
        paginator_instance2 = Paginator(organizations, 5)
        page2 = request.GET.get('page2')
        organizations_paginator_instance = paginator_instance2.get_page(page2)

        context = {
            'sum_of_bags': sum_quantity_bags,
            'number_of_institutions': number_of_institutions,
            'foundations': foundations_paginator_instance,
            'organizations': organizations_paginator_instance,
            'local_collections': local_collections,
        }

        return render(request, 'home_app/landing_page.html', context=context)
