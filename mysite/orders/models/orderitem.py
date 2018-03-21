# -*- coding: UTF-8 -*-
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
        return self.value * (1 + self.vat.used_rate)

    def pre_delete(self):
        print self.content_object
        self.content_object.delete()

    def __unicode__(self):  # __unicode__ on Python 2
        # return self.description + " &pound;" + '%.2f' % self.value
        return u"%s £%.2f" % (self.description, self.value)


from django.shortcuts import get_object_or_404


# setup delete related objects
def del_content_object(sender, instance, *args, **kwargs):
    print(instance.content_object)
    ob_type = instance.content_type.model_class()
    ob_id = instance.object_id
    get_object_or_404(ob_type, pk=ob_id).delete()

models.signals.pre_delete.connect(del_content_object, sender=OrderItem)