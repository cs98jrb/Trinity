from django.db import models
from django.db.models import Sum
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class OrderManager(models.Manager):
    def get_queryset(self):
        qs = super(OrderManager, self).get_queryset()
        return qs.annotate(total_ex=Sum('orderitem__value'))


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    open = models.BooleanField(default=True)
    objects = OrderManager()

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.pk) + " " + self.date.strftime('%d/%m/%Y')


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    description = models.CharField(max_length=150)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    vat = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def value_inc(self):
        return float(self.value) * (1 + (self.vat / 100.0))

    def __unicode__(self):  # __unicode__ on Python 2
        return self.description + " " + str(self.value)


class Payment(models.Model):
    order = models.ForeignKey(Order)
    date = models.DateField()
    payed = models.BooleanField(default=False)
    payment_ref = models.CharField(max_length=150, null=True, blank=True)
    value_exc = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    value_inc = models.DecimalField(default=0, max_digits=6, decimal_places=2)