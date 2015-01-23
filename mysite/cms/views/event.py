import string
import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError, ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

from accounts.models import AuthUser

from events.models import Event, Pricing

from events.forms import BookingForm

from cms.forms import UpdateEvent


def index(request):
    return render(request, 'cms/index.html')


def events(request):
    event_list = Event.objects.all()

    return render(request, 'cms/events.html', {
        'event_list': event_list,
    })


def event_report(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    bookings = event.booking_set.all()



    return render(request, 'cms/event_booking.html', {
        'event': event,
        'bookings': bookings,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    PriceInlineForm = inlineformset_factory(Event, Pricing.event.through, extra=1)

    if 'status_form_event' in request.session:
        status = request.session['status_form_event']
        del request.session['status_form_event']
    else:
        status = False

    if request.POST:
        formset = PriceInlineForm(request.POST, request.FILES, instance=event)
        form = UpdateEvent(request.POST, instance=event)
        if formset.is_valid():
            formset.save()
            if form.is_valid():
                form.save()
                formset.save()

                # If the save was successful, redirect to another page
                request.session['status_form_event'] = 'Updated'
                redirect_url = reverse('cms:event_detail', kwargs={
                    'event_id': event_id
                })
                return HttpResponseRedirect(redirect_url)

            else:
                status = "Update Failed check the form."
        else:
            status = "Payments Error."



    else:
        form = UpdateEvent(instance=event)
        formset = PriceInlineForm(instance=event)

    return render(request, 'cms/event_detail.html', {
        'status': status,
        'event': event,
        'request': request,
        'form': form,
        'priceing': formset,
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