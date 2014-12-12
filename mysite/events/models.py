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

class Venue(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=50)
    postcode = models.CharField(max_length=8, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name + ", " + self.town


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    venue = models.ForeignKey(Venue)
    capacity = models.IntegerField(default=0)
    event_time = models.DateTimeField()
    book_from = models.DateTimeField(blank=True, null=True)
    last_booking = models.DateTimeField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    @property
    def fully_booked(self):
        if self.capacity > 0:
            bookings = self.booking_set.filter(confirmed=True).aggregate(total=models.Sum('quantity'))
            total = int(bookings['total'] or 0)

            if total < self.capacity:
                return False
            else:
                return True
        else:
            return False

    @property
    def num_spaces(self):
        if self.capacity > 0:
            bookings = self.booking_set.filter(
                Q(confirmed=True) |
                Q(payment_pending=True)
            ).aggregate(total=models.Sum('quantity'))
            total = int(bookings['total'] or 0)

            print(bookings)

            if total < self.capacity:
                return self.capacity - total
            else:
                return 0
        else:
            return 999

    class Meta:
        ordering = ['event_time']

    def __unicode__(self):  # __unicode__ on Python 2
        return self.event_time.strftime('%d/%m/%Y @ %H:%M') + " " + self.title + ", " + str(self.venue)


class Pricing(models.Model):
    event = models.ManyToManyField(Event, null=True, blank=True, )
    title = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    online_book = models.BooleanField(default=False)
    vat = models.ForeignKey(Vat)

    @property
    def value_inc(self):
        return self.value * (1 + self.vat.used_rate)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.title + " &pound;" + '%.2f' % self.value_inc


def send_email(booking):

    user = booking.booked_by
    message_text = EmailText.objects.get(id=2)

    subject = message_text.subject
    message = message_text.body

    ref = booking.ref
    quantity = booking.quantity
    venue = booking.event.venue
    date_time = booking.event.event_time

    # replace place holders
    message = string.replace(message, '{{ ref }}', ref)
    message = string.replace(message, '{{ quantity }}', '%.0f' % quantity)
    message = string.replace(message, '{{ venue }}', venue.name+', '+venue.town+' '+venue.postcode)
    message = string.replace(message, '{{ date_time }}', date_time.strftime('%a, %d %b %Y at %I:%M:%S %p'))

    sender = settings.SERVER_EMAIL

    recipients = [user.email]

    send_mail(subject, message, sender, recipients)

    send_mail(subject, message, sender, ['james@pjshire.me.uk'])

    print(message)

import random
class Booking(models.Model):

    ref = models.CharField(max_length=8, default='x')
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    booked = models.DateField('date booked', auto_now_add=True)
    event = models.ForeignKey(Event)
    price = models.ForeignKey(Pricing)
    quantity = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    payment_pending = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Booking.objects.get(pk=self.pk)
            if not old_instance.confirmed and (
                    self.confirmed or self.payment_pending
            ):
                if not old_instance.payment_pending and self.quantity > self.event.num_spaces:
                    # Not enough space
                    raise ValueError("Not enough spaces")
                elif self.confirmed:
                    send_email(self)
        else:
            import pytz, datetime
            from django.utils import timezone
            rand = hex(random.SystemRandom().randint(0, 255))[2:]

            default_val = ("xxxxxxxx"+hex(int(
                (timezone.now() - pytz.utc.localize(datetime.datetime(2010, 1, 1))).total_seconds())
            )+ rand)[-8:]
            self.ref = default_val.upper()

        super(Booking, self).save(*args, **kwargs)

    def __unicode__(self):  # __unicode__ on Python 2
        data = str(self.event)
        info = (data[:40] + ' ...') if len(data) > 44 else data
        return info