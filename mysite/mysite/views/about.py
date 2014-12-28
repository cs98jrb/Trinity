from django.utils import timezone
from django.views import generic

from django.shortcuts import render

from events.models import Event

def about(request):
    return render(request, 'mysite/about.html', {
    })