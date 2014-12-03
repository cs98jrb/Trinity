from django.db import models

from datetime import datetime

from orders.models import Order


class PaymentType(models.Model):
    name = models.CharField(max_length=50)
    accounting = models.BooleanField(default=False)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.name)


class Payment(models.Model):
    order = models.ForeignKey(Order)
    type = models.ForeignKey(PaymentType)
    date = models.DateField()
    payed = models.BooleanField(default=False)
    payment_ref = models.CharField(max_length=150, null=True, blank=True)
    value_exc = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    value_inc = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __unicode__(self):
        if self.payed:
            return "Paid "+str(self.value_inc)+" on "+self.date.strftime('%d/%m/%Y')
        elif self.date > datetime.now():
            return "Due "+str(self.value_inc)+" on "+self.date.strftime('%d/%m/%Y')
        else:
            return "Over due "+str(self.value_inc)+" from "+self.date.strftime('%d/%m/%Y')