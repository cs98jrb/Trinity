import string
import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage

# from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

from accounts.models import AuthUser

from readings.forms import BookingForm, ReadingForm

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

            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']

            # recipients = ['Trinityrosewilliams@outlook.com']
            recipients = ['james@pjshire.me.uk']
            # recipients = ['web-gktVTO@mail-tester.com']

            form.save()

            # send_mail(subject, message, sender, recipients)
            msg = EmailMessage(
                subject, message, settings.SERVER_EMAIL,
                settings.EMAIL_FORMS['readings'], [],
                headers={'Reply-To': sender}
            )

            msg.send()
            msg = None
            msg = EmailMessage(
                subject, message, settings.SERVER_EMAIL,
                ['james@pjshire.me.uk'], [],
                headers={'Reply-To': sender}
            )

            msg.send()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('readings:thankyou'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReadingForm(request)

    return render(request, 'readings/request.html', {
        'form': form,
    })


def book(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BookingForm(request, request.POST)
        # check whether it's valid:
        if form.is_valid():
            from orders.models import Order
            # process the data in form.cleaned_data as required

            user = None
            if request.user.is_authenticated():
                user = request.user

            else:
                try:
                    user = AuthUser.objects.get(username=form.cleaned_data['email'])
                except ObjectDoesNotExist:
                    pass_chars = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKMNOPQRSTUVWXYZ0123456789'
                    tmp_pass = ''.join(
                        random.SystemRandom().choice(
                            pass_chars
                        ) for _ in range(8)
                    )
                    try:
                        user = AuthUser.objects.create_user(
                            form.cleaned_data['email'],
                            form.cleaned_data['email'],
                            tmp_pass
                        )
                        user.save()

                    except Exception as e:
                        messages.error(request, "An Error Occured !"+e.message)

            if user:
                try:
                    form.save(user=user)
                    open_order = Order.objects.open_order(user)
                    request.session['order_id'] = open_order[0].id

                    # redirect to a new URL:
                    return HttpResponseRedirect(
                        reverse('orders:detail', kwargs={'order_id': open_order[0].id})
                    )
                except ValidationError as e:
                    form.add_error('quantity', e)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BookingForm(request)

    return render(request, 'readings/detail.html', {
        'request': request,
        'form': form,
    })


def thankyou(request):
    return render(request, 'readings/thankyou.html')