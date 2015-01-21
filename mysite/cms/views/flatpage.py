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

from cms.forms import UpdateFlatPage

from django.contrib.flatpages.models import FlatPage


def flatpage_detail(request, page_url):
    event = get_object_or_404(FlatPage, url='/'+page_url+'/')

    if request.POST:
        form = UpdateFlatPage(request.POST, instance=event)
        if form.is_valid():
            form.save()

            # If the save was successful, redirect to another page
            redirect_url = reverse('cms:flatpage_detail', kwargs={'page_url': page_url})
            return HttpResponseRedirect(redirect_url)

    else:
        form = UpdateFlatPage(instance=event)

    return render(request, 'cms/event_detail.html', {
        'event': event,
        'request': request,
        'form': form,
    })