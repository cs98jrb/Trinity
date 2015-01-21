from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from datetime import datetime

from mysite.models import EmailInf


class ReadingForm(forms.ModelForm):
    # set the css of required fields
    required_css_class = 'required'

    confirm_email = forms.EmailField(
        max_length=254,
        label="Confirm email",
        required=True,
    )
    requested_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M', ],
        label="Preferred date and time",
        help_text="We will confirm the exact time and date in the response.",
        required=True
    )

    reading_type = forms.ChoiceField(
        choices=(('Telephone Reading', 'Telephone Reading'),
                 ('Group booking', 'Group booking'),
                 ('Visit Trinity', 'Visit Trinity')),
        required=True,
    )

    def __init__(self, request, *args, **kwargs):
        super(ReadingForm, self).__init__(*args, **kwargs)
        try:
            if not request.user.is_anonymous():
                self.fields['email'].initial = request.user.email
                self.fields['confirm_email'].initial = request.user.email

            self.fields['requested_date'].initial = datetime.now().strftime("%d/%m/%Y %H:%M")
        except User.DoesNotExist:
            pass

    class Meta:
        model = EmailInf
        fields = ['name', 'email', 'confirm_email', 'requested_date', 'reading_type', 'message', ]

    def clean(self):

        if (self.cleaned_data.get('email') !=
                self.cleaned_data.get('confirm_email')):

            raise ValidationError(
                "Email addresses must match."
            )

        return self.cleaned_data

    def clean_message(self):
        data = "FROM: "+self.cleaned_data['name']+" ("+self.cleaned_data['email']+")\n" + \
            "Date: "+self.cleaned_data['requested_date'].strftime("%d/%m/%Y") + "\n" +\
            "Time: "+self.cleaned_data['requested_date'].strftime("%H:%M") + "\n" +\
            "Type: "+self.cleaned_data['reading_type'] + "\n" +\
            self.cleaned_data['message']
        return data