from django.db import models
from orders.models import Order


class Invoice(models.Model):
    order = models.OneToOneField(Order,primary_key=True)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return "Invoice "+str(self.pk)