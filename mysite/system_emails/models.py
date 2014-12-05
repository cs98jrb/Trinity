from django.db import models


class EmailText(models.Model):
    subject = models.CharField(max_length=150)
    body = models.TextField(verbose_name='The content for the email')

    def __unicode__(self):  # __unicode__ on Python 2
        return self.subject