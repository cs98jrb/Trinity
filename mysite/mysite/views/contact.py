from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives

from django.conf import settings

from events.models import Event
from mysite.forms import ContactForm, CreateUserForm


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
        form = ContactForm(request, request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            subject = "Message from website"
            message = "FROM: "+form.cleaned_data['name']+"\n"+form.cleaned_data['message']
            sender = form.cleaned_data['email']

            recipients = ['james@pjshire.me.uk']
            # recipients = ['web-gktVTO@mail-tester.com']

            form.save()

            print subject
            print message
            print sender
            print recipients


            # send_mail(subject, message, sender, recipients)
            msg = EmailMessage(
                subject, message, settings.SERVER_EMAIL,
                recipients, [],
                headers={'Reply-To': sender}
            )

            msg.send()
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


