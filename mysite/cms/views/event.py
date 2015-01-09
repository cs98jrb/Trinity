import string
import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

from accounts.models import AuthUser

from events.models import Event

from events.forms import BookingForm


def index(request):
    return render(request, 'cms/index.html')


def events(request):
    event_list = Event.objects.all()

    return render(request, 'cms/events.html', {
        'event_list': event_list,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.pricing_set.all().filter(online_book=True)\
            and not event.fully_booked:
        booking = True
    else:
        booking = False

    return render(request, 'events/detail.html', {
        'event': event,
        'bookable': booking,
        'request': request,
        'form': BookingForm(request),
    })