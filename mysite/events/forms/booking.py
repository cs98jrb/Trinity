__author__ = 'james'
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from events.models import Booking

from orders.models import Order


class BookingForm(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'

    # def __init__(self, request, *args, **kwargs):
    #    super(BookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking

    def clean(self):
        return self.cleaned_data