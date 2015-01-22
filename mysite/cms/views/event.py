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

from cms.forms import UpdateEvent


def index(request):
    return render(request, 'cms/index.html')


def events(request):
    event_list = Event.objects.all()

    return render(request, 'cms/events.html', {
        'event_list': event_list,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if 'status_form_event' in request.session:
        status = request.session['status_form_event']
        del request.session['status_form_event']
    else:
        status = False

    if request.POST:
        form = UpdateEvent(request.POST, instance=event)
        if form.is_valid():
            form.save()

            # If the save was successful, redirect to another page
            request.session['status_form_event'] = 'Updated'
            redirect_url = reverse('cms:event_detail', kwargs={
                'event_id': event_id
            })
            return HttpResponseRedirect(redirect_url)

        else:
            status = "Update Failed check the form."

    else:
        form = UpdateEvent(instance=event)

    return render(request, 'cms/event_detail.html', {
        'status': status,
        'event': event,
        'request': request,
        'form': form,
    })

def event_add(request):
    if 'status_form_event' in request.session:
        status = request.session['status_form_event']
        del request.session['status_form_event']
    else:
        status = False

    if request.POST:
        form = UpdateEvent(request.POST)
        if form.is_valid():
            event = form.save()

            # If the save was successful, redirect to another page
            request.session['status_form_event'] = 'Updated'
            redirect_url = reverse('cms:event_detail', kwargs={
                'event_id': event.pk
            })
            return HttpResponseRedirect(redirect_url)

        else:
            status = "Update Failed check the form."

    else:
        form = UpdateEvent()

    return render(request, 'cms/event_detail.html', {
        'status': status,
        'event': False,
        'request': request,
        'form': form,
    })