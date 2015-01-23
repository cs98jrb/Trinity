__author__ = 'james'
from django import forms

from events.models import Venue


class UpdateVenue(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'

    class Meta:
        model = Venue
        fields = [
            'name',
            'address',
            'town',
            'postcode',
            'lat',
            'lng',
            ]

    def clean(self):
        return self.cleaned_data