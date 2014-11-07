from django.db import models

# Create your models here.

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

    class Meta:
        ordering = ['event_time']

    def __unicode__(self):  # __unicode__ on Python 2
        return self.event_time.strftime('%d/%m/%Y @ %H:%M') + " " + self.title + ", " + str(self.venue)


class Pricing(models.Model):
    event = models.ManyToManyField(Event, null=True, blank=True, )
    title = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    online_book = models.BooleanField(default=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.title + " " + str(self.value)