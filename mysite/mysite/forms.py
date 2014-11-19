from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from mysite.models import EmailInf


class ContactForm(forms.ModelForm):
    confirm_email = forms.EmailField(
        label="Confirm email",
        required=True,
    )

    def __init__(self,request, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        try:
            if not request.user.is_anonymous():
                self.fields['email'].initial = request.user.email
                self.fields['confirm_email'].initial = request.user.email
        except User.DoesNotExist:
            pass

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


class CreateUserForm(forms.ModelForm):
    confirm_email = forms.EmailField(
        label="Confirm email",
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):

        if (self.cleaned_data.get('email') !=
                self.cleaned_data.get('confirm_email')):

            raise ValidationError(
                "Email addresses must match."
            )

        return self.cleaned_data