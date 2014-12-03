from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from events.models import Booking


class BookingForm(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'

    def __init__(self,request, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        try:
            if not request.user.is_anonymous():
                self.fields['email'].initial = request.user.email
                self.fields['confirm_email'].initial = request.user.email
        except User.DoesNotExist:
            pass

    class Meta:
        model = Booking
        fields = ['name', 'email', 'confirm_email', 'message', ]

    def clean(self):

        if (self.cleaned_data.get('email') !=
                self.cleaned_data.get('confirm_email')):

            raise ValidationError(
                "Email addresses must match."
            )

        return self.cleaned_data