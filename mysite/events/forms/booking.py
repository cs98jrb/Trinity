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
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Making first_name required
        self.fields['quantity'].label = "Number of people"

    # def __init__(self, request, *args, **kwargs):
    #    super(BookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = ['quantity', ]

    def save(self, event_id, price, commit=True, login=True):
        # Hash the password
        booking = super(BookingForm, self).save(commit=False)
        booking.event_id = event_id
        booking.price = price

        if commit:
            booking.save()

        return booking

    def clean(self):
        return self.cleaned_data