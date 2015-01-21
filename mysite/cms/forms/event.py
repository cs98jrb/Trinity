__author__ = 'james'
from django.utils.translation import ugettext as _
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from events.models import Booking, Event

from orders.models import Order, OrderItem


class UpdateEvent(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'
    event_time = forms.DateTimeField(widget=forms.SplitDateTimeWidget)
    book_from = forms.DateTimeField(widget=forms.SplitDateTimeWidget)
    last_booking = forms.DateTimeField(widget=forms.SplitDateTimeWidget)

    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'venue',
            'capacity',
            'event_time',
            'book_from',
            'last_booking',
            ]

    def clean(self):
        return self.cleaned_data