__author__ = 'james'
from django.db import models
from orders.models import Order


class Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ref = models.CharField(max_length=50)
    related_order = models.ForeignKey(Order, related_name='paypal')
    value = models.DecimalField(max_digits=6, decimal_places=2)
    successful = models.DateTimeField(null=True, blank=True)