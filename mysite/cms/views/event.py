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

from cms.forms  import UpdateEvent


def index(request):
    return render(request, 'cms/index.html')


def events(request):
    event_list = Event.objects.all()

    return render(request, 'cms/events.html', {
        'event_list': event_list,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.POST:
        form = UpdateEvent(request.POST, instance=event)
        if form.is_valid():
            form.save()

            # If the save was successful, redirect to another page
            redirect_url = reverse('cms:event_detail', kwargs={'event_id': event_id})
            return HttpResponseRedirect(redirect_url)

    else:
        form = UpdateEvent(instance=event)

    return render(request, 'cms/event_detail.html', {
        'event': event,
        'request': request,
        'form': form,
    })