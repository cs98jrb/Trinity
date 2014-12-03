from django.db import models
from django.conf import settings


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    open = models.BooleanField(default=True)
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):  # __unicode__ on Python 2
        return str(self.pk) + " " + self.date.strftime('%d/%m/%Y')
