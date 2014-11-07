from django import forms
from django.core.exceptions import ValidationError

from mysite.models import EmailInf


class ContactForm(forms.ModelForm):
    confirm_email = forms.EmailField(
        label="Confirm email",
        required=True,
    )

    class Meta:
        model = EmailInf
        fields = ['name', 'email', 'confirm_email', 'message', ]

    def clean(self):

        if (self.cleaned_data.get('email') !=
            self.cleaned_data.get('confirm_email')):

            raise ValidationError(
                "Email addresses must match."
            )

        return self.cleaned_data