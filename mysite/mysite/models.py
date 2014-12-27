from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.mail import send_mail
from django.core import validators
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils.crypto import get_random_string, salted_hmac
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib import auth
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)
from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


class EmailInf(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(
        max_length=128,
        default="Website 'Contact Us'"
    )
    message = models.TextField()
    sent_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )
    
    class Meta:
        ordering = ['sent_date']
        
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name + ", (" +str(self.sent_date)+")"