__author__ = 'james'
from django.utils import timezone
from django.views import generic
from django.http import HttpResponse
from django.templatetags.static import static

from django.shortcuts import render

from events.models import Event


def tandc(request):
    with open('static/mysite/files/terms-and-conditions.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=terms-and-conditions.pdf'
        return response
    pdf.closed

def privacy_policy(request):
    with open('static/mysite/files/privacy-policy.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=terms-and-conditions.pdf'
        return response
    pdf.closed