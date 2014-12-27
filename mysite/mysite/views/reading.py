from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives

from django.conf import settings

from events.models import Event
from mysite.forms import ReadingForm
from mysite.models import EmailInf


def reading(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        subject = "Trinity Website 'Request a reading'"

        email_inf = EmailInf(subject=subject)
        form = ReadingForm(request, request.POST, instance=email_inf)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            message = "FROM: "+form.cleaned_data['name'] + "\n" +\
                      "Date: "+form.cleaned_data['requested_date'].strftime("%d/%m/%Y") + "\n" +\
                      "Time: "+form.cleaned_data['requested_date'].strftime("%H:%M") + "\n" +\
                      form.cleaned_data['message']
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
        form = ReadingForm(request)

    return render(request, 'mysite/request.html', {
        'form': form,
    })
