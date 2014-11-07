from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views import generic

from events.models import Event
from mysite.forms import ContactForm


class IndexView(generic.ListView):
    template_name = 'mysite/index.html'

    def get_queryset(self):
        return Event.objects.filter(
            event_time__gte=timezone.now()
        )[:5]


def coming_soon(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    return render(request, 'mysite/coming_soon.html', {
        'event_list': event_list,
    })


def contact(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    return render(request, 'mysite/contact.html', {
        'event_list': event_list,
    })


def get_contact(request):

    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('home page'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'mysite/contact.html', {
        'form': form,
        'event_list': event_list,
    })
