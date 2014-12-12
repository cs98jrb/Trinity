from django.db import models
from django.contrib.auth.models import User


class Testimonial(models.Model):
    created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
    left_by = models.ForeignKey(User)
    town = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    hompage = models.BooleanField(default=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.title + " - " + str(self.left_by) + ", " + self.town