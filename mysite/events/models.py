from django.db import models

from django.contrib.contenttypes.fields import GenericRelation
from orders.models import OrderItem

from orders.models import Vat

class Venue(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=50)
    postcode = models.CharField(max_length=8, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name + ", " + self.postcode


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
            bookings = self.booking_set.filter(confirmed=True).aggregate(total=models.Sum('quantity'))
            total = int(bookings['total'] or 0)

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


class Booking(models.Model):
    booked = models.DateField('date booked', auto_now_add=True)
    event = models.ForeignKey(Event)
    price = models.ForeignKey(Pricing)
    quantity = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    order_item = GenericRelation(OrderItem)

    def __unicode__(self):  # __unicode__ on Python 2
        data = str(self.event)
        info = (data[:40] + ' ...') if len(data) > 44 else data
        return info