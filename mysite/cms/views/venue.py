import string
import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy

from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

from accounts.models import AuthUser

from events.models import Venue

from cms.forms import UpdateVenue

@permission_required('events.change_venue', login_url=reverse_lazy('cms:login'))
def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)

    if 'status_form_event' in request.session:
        status = request.session['status_form_event']
        del request.session['status_form_event']
    else:
        status = False

    if request.POST:
        form = UpdateVenue(request.POST, instance=venue)
        if form.is_valid():
            form.save()

            # If the save was successful, redirect to another page
            request.session['status_form_event'] = 'Updated'
            redirect_url = reverse('cms:venue_detail', kwargs={
                'venue_id': venue_id
            })
            return HttpResponseRedirect(redirect_url)

        else:
            status = "Update Failed check the form."

    else:
        form = UpdateVenue(instance=venue)

    return render(request, 'cms/venue_detail.html', {
        'status': status,
        'venue': venue,
        'request': request,
        'form': form,
    })


@permission_required('events.change_venue', login_url=reverse_lazy('cms:login'))
def venue_add(request):
    if 'status_form_event' in request.session:
        status = request.session['status_form_event']
        del request.session['status_form_event']
    else:
        status = False

    if request.POST:
        form = UpdateVenue(request.POST)
        if form.is_valid():
            venue = form.save()

            # If the save was successful, redirect to another page
            request.session['status_form_event'] = 'Updated'
            redirect_url = reverse('cms:venue_detail', kwargs={
                'venue_id': venue.pk
            })
            return HttpResponseRedirect(redirect_url)

        else:
            status = "Update Failed check the form."

    else:
        form = UpdateVenue()

    return render(request, 'cms/venue_detail.html', {
        'status': status,
        'venue': False,
        'request': request,
        'form': form,
    })