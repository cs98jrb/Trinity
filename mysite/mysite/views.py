from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views import generic
from django.core.mail import send_mail


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
        form = ContactForm(request,request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            subject = "Message from website"
            message = "FROM: "+form.cleaned_data['name']+"\n"+form.cleaned_data['message']
            sender = form.cleaned_data['email']

            recipients = ['james@pjshire.me.uk']

            form.save();

            send_mail(subject, message, sender, recipients)

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('thank you'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm(request)

    return render(request, 'mysite/contact.html', {
        'form': form,
        'event_list': event_list,
    })

def contact_thanks(request):
    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]
    return render(request, 'mysite/contact_thanks.html', {
        'event_list': event_list,
    })