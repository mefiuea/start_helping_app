from django.shortcuts import render


def add_donation_view(request):
    if request.method == 'GET':
        return render(request, 'donation_app/form.html')
