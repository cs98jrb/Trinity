from django.db import models
from django.conf import settings


class Vat(models.Model):
    valid_from = models.DateField()
    name = models.CharField(max_length=25)
    # The tax rate expressed as a decimal fraction
    # E.g. 20% is 0.2 and 5% is 0.05
    rate = models.DecimalField(default=0, max_digits=5, decimal_places=4)

    def _get_used_rate(self):
        if not settings.VAT_REGISTERED:
            return 0
        return self.rate

    used_rate = property(_get_used_rate)

    def rate_pc(self):
        if not settings.VAT_REGISTERED:
            return 0
        return self.rate * 100

    def __unicode__(self):
        return self.name + " " + str(round(self.rate*100, 2)) + "%"