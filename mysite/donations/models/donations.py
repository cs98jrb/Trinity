# -*- coding: UTF-8 -*-
__author__ = 'james'
import string
from django.db import models
from django.conf import settings
from django.core.mail import send_mail

from system_emails.models import EmailText

from orders.models import Vat


class Pricing(models.Model):
    title = models.CharField(max_length=50, default='Online donation')
    value = models.DecimalField(max_digits=7, decimal_places=2)
    online_book = models.BooleanField(default=True)
    vat = models.ForeignKey(Vat, related_name='donation', default=1)

    @property
    def value_inc(self):
        return self.value * (1 + self.vat.used_rate)

    def __unicode__(self):  # __unicode__ on Python 2
        return u"£%i %s" % (self.value_inc, self.title)


def send_email(donation):

    user = donation.booked_by
    message_text = EmailText.objects.get(id=4)

    subject = message_text.subject
    message = message_text.body

    # replace place holders
    message = string.replace(message, '{{ value }}', "%.2f" % donation.price.value_inc)

    sender = settings.SERVER_EMAIL

    recipients = [user.email]

    send_mail(subject, message, sender, recipients)

    send_mail(subject, message, sender, ['james@pjshire.me.uk'])

    # print(message)


class Donation(models.Model):

    ref = models.CharField(max_length=8, default='x')
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='donations')
    date = models.DateField('date booked', auto_now_add=True)
    price = models.ForeignKey(Pricing, null=True)
    quantity = models.IntegerField(default=1)
    confirmed = models.BooleanField(default=False)
    payment_pending = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Donation.objects.get(pk=self.pk)
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

        super(Donation, self).save(*args, **kwargs)

    def __unicode__(self):  # __unicode__ on Python 2
        # data = str(self.price)+ ' By '+str(self.booked_by.username)
        data = u"%s by %s" % (self.price, self.booked_by.username)
        info = (data[:40] + ' ...') if len(data) > 44 else data
        return u"%s" % info