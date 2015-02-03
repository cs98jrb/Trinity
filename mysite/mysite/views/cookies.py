from django.utils import timezone
from django.views import generic
from django.http import HttpResponse
from cookie_consent import util

from django.shortcuts import render

from events.models import Event


# home page
class IndexView(generic.ListView):


    def get_queryset(self):
        return Event.objects.filter(
            event_time__gte=timezone.now()
        )[:5]


# Holding page
def accept_all_cookies(request):
    response = HttpResponse("ok", content_type="text/plain")
    util.accept_cookies(request, response, 'track')
    return response

# google
def google(request):
    return HttpResponse("google-site-verification: googlec35559684fb6219b.html")