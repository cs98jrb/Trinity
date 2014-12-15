from django.utils import timezone
from django.views import generic
from django.http import HttpResponse

from django.shortcuts import render

from events.models import Event


# home page
class IndexView(generic.ListView):
    template_name = 'mysite/index.html'

    def get_queryset(self):
        return Event.objects.filter(
            event_time__gte=timezone.now()
        )[:5]


# Holding page
def coming_soon(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    return render(request, 'mysite/coming_soon.html', {
        'event_list': event_list,
    })

# google
def google(request):
    return HttpResponse("google-site-verification: googlec35559684fb6219b.html")