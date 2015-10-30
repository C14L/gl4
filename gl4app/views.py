# from django.conf import settings
from django.http import HttpResponse


def home(request):
    return HttpResponse('graniteland4 home')
