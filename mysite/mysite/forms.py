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

    def __init__(self, *args, **kwargs):

        if kwargs.get('instance'):
            email = kwargs['instance'].email
            kwargs.setdefault('initial', {})['confirm_email'] = email

        return super(ContactForm, self).__init__(*args, **kwargs)