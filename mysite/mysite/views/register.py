import string

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.core.mail import send_mail

from django.conf import settings

from events.models import Event
from mysite.forms import CreateUserForm
from system_emails.models import EmailText


def register(request):

    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    redirect_to = request.POST.get('next',
                                   request.GET.get('next', ''))

    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url('home page')

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            message_text = EmailText.objects.get(id=1)

            subject = message_text.subject
            message = message_text.body

            # replace place holders
            message = string.replace(message, '{{ user_name }}', form.cleaned_data['username'])
            message = string.replace(message, '{{ password }}', form.cleaned_data['password1'])
            message = string.replace(message, '{{ first_name }}', form.cleaned_data['first_name'])
            message = string.replace(message, '{{ last_name }}', form.cleaned_data['last_name'])

            sender = settings.SERVER_EMAIL

            recipients = [form.cleaned_data['email']]

            send_mail(subject, message, sender, recipients)

            send_mail(subject, message, sender, ['james@pjshire.me.uk'])

            form.save()

            form.login(request)

            return HttpResponseRedirect(redirect_to)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateUserForm()

    return render(request, 'mysite/new_user.html', {
        'form': form,
        'event_list': event_list,
        'redirect_to': redirect_to,
    })