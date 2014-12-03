from django.db import models


class Vat(models.Model):
    valid_from = models.DateField()
    name = models.CharField(max_length=25)
    # The tax rate expressed as a decimal fraction
    # E.g. 20% is 0.2 and 5% is 0.05
    rate = models.DecimalField(default=0, max_digits=5, decimal_places=4)

    def rate_pc(self):
        return self.rate * 100

    def __unicode__(self):
        return self.name + " " + str(round(self.rate*100, 2)) + "%"