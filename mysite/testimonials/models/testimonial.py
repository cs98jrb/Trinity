from django.db import models


class Testimonial(models.Model):
    created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
    left_by = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    hompage = models.BooleanField(default=True)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.name + ", " + self.postcode