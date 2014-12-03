from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from events.models import Event


def index(request):
    Event.capacity = 1
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    return render(request, 'events/index.html', {
        'event_list': event_list,
    })


def detail(request, event_id):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    event = get_object_or_404(Event, pk=event_id)
    if event.pricing_set.all().filter(online_book=True):
        booking = True
    else:
        booking = False

    return render(request, 'events/detail.html', {
        'event_list': event_list,
        'event': event,
        'bookable': booking,
    })

@login_required
def book(request, event_id):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    event = get_object_or_404(Event, pk=event_id)
    pricing_set = event.pricing_set
    online_pricing = event.pricing_set.all().filter(online_book=True)

    return render(request, 'events/book.html', {
        'event_list': event_list,
        'event': event,
        'pricing_set': pricing_set,
        'online_pricing': online_pricing,
    })