from django.utils import timezone
from django.views import generic
from django.http import HttpResponse

from django.shortcuts import render

from events.models import Event


def press(request):

    return render(request, 'mysite/press.html', )
