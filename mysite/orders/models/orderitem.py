from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from orders.models import Order, Vat

class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    description = models.CharField(max_length=150)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    vat = models.ForeignKey(Vat)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def value_inc(self):
        return float(self.value) * (1 + (self.vat / 100.0))

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description + " " + str(self.value)