from django.http import HttpResponse


def dashboard_home(request):
    return HttpResponse("Welcome to Skillvine Dashboard!")