from rest_framework import viewsets
from django.http import HttpResponse


def index(request):
    return HttpResponse("Escreva alguma coisa para mostrar na página...")