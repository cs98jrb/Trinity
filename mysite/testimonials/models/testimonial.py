from django.db import models
from django.conf import settings


class Testimonial(models.Model):
    created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
    left_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    town = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    hompage = models.BooleanField(default=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.title + " - " + self.left_by.first_name + ", " + self.town