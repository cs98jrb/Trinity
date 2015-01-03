__author__ = 'james'
import string
from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db.models import Q

from orders.models import OrderItem
from system_emails.models import EmailText
from orders.models import Vat


class Pricing(models.Model):
    title = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    online_book = models.BooleanField(default=False)
    vat = models.ForeignKey(Vat,related_name='reading')

    @property
    def value_inc(self):
        return self.value * (1 + self.vat.used_rate)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.title


def send_email(booking):

    user = booking.booked_by
    message_text = EmailText.objects.get(id=3)

    subject = message_text.subject
    message = message_text.body

    ref = booking.ref

    # replace place holders
    message = string.replace(message, '{{ ref }}', ref)

    sender = settings.SERVER_EMAIL

    recipients = [user.email]

    send_mail(subject, message, sender, recipients)

    send_mail(subject, message, sender, ['james@pjshire.me.uk'])

    print(message)


class Booking(models.Model):

    ref = models.CharField(max_length=8, default='x')
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reading')
    booked = models.DateField('date booked', auto_now_add=True)
    price = models.ForeignKey(Pricing)
    quantity = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    payment_pending = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Booking.objects.get(pk=self.pk)
            if not old_instance.confirmed and self.confirmed:
                send_email(self)
        else:
            import pytz
            import datetime
            import random

            from django.utils import timezone
            rand = hex(random.SystemRandom().randint(0, 255))[2:]

            default_val = ("xxxxxxxx"+hex(int(
                (timezone.now() - pytz.utc.localize(datetime.datetime(2010, 1, 1))).total_seconds())
            )+ rand)[-8:]
            self.ref = default_val.upper()

        super(Booking, self).save(*args, **kwargs)

    def __unicode__(self):  # __unicode__ on Python 2
        data = str(self.booked_by.username)+' '+str(self.price.title)
        info = (data[:40] + ' ...') if len(data) > 44 else data
        return info